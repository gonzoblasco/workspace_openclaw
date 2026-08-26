# Nivel 3 - Containing Cascading Failures (Cap 3)

Badge: 🧱 Bulkhead | Recursos: libro Cap 3 + repo OpenClaw live + workspace real

## Subnivel 3.1 - Anatomía y contención

### Topic: Anatomía del cascade failure

**Teoría (vocabulario con nombre):**
- **Cascade failure**: un fallo local (plugin, channel, memory leak del agent runtime) que se propaga por todo el sistema si no hay boundaries entre componentes. Uno de los failure modes más dañinos en sistemas distribuidos.
- **Tres fases donde aparece el riesgo**: plugin load, plugin register, plugin runtime. Cada una con sus failure modes y estrategia de recovery.
- **Plugin load phase** (src/plugins/loader.ts): lee el código, resuelve deps, crea el module object. Failure modes: dep faltante, syntax error, path traversal attack (cargar código fuera del root del plugin).
- **Plugin register phase**: llama register() y registra hooks/tools/services con el Gateway. Failure modes: hook handler que lanza, tool que no inicializa, service que no conecta a su backend.
- **Plugin runtime phase**: ejecuta hooks y tools cuando llegan mensajes. Failure modes: hook handler que crashea, tool que cuelga indefinidamente, service sin memoria.
- **loadOpenClawPlugins()** (src/plugins/loader.ts): orquestador defensivo - cada module eval en try/catch, la excepción se registra como diagnostic, no crashea el Gateway.
- **recordPluginError()**: la clave. Setea status="error", registra el mensaje, agrega entry a registry.diagnostics. El Gateway sigue arrancando aunque un plugin falle.
- **runVoidHook() / runModifyingHook()** (src/plugins/hooks.ts): orquestan la fase runtime. Ejecutan todos los handlers registrados para un hook name, capturando excepciones por handler. handleHookError() loguea sin crashear.
- **Path de propagación**: un fault recorre load -> register -> runtime, y en CADA una el try/catch lo convierte en diagnostic en vez de crash. Las defensas posteriores son interrupciones deliberadas de este path.

**Verificación (mock interview):** ¿Qué es un cascade failure y en qué 3 fases aparece en OpenClaw?
**Esperada:** un fallo local que se propaga por el sistema. En OpenClaw, en las fases de plugin load, register y runtime, cada una con su propio failure mode y recovery.

### Topic: Bulkhead pattern

**Teoría:**
- **Bulkhead pattern**: aísla componentes en compartimentos separados - como los compartimentos estancos de un barco: si uno se inunda, los otros quedan secos y el barco sigue flotando.
- **OJO - distinción crucial del cap**: en OpenClaw el Bulkhead es **isolation lógica via try/catch boundaries alrededor de las fases del lifecycle**, NO per-dependency thread pools (como en el bulkhead clásico de resilience). OpenClaw sigue siendo single-process - un handler CPU-bound runaway puede stallear sus siblings de Promise.all. **El valor aquí es containment, no paralelismo.**
- **4 niveles de Bulkhead:**
  1. **Plugin lifecycle phases**: aísla load, register, start, run. Un fallo en una fase no afecta a las otras.
  2. **Plugin execution context**: aísla hooks/tools/services de cada plugin. Un fallo en un plugin no afecta a otros.
  3. **Channel adapter**: aísla webhook handlers, message processors, delivery de cada canal. Un fallo en un canal no afecta a otros.
  4. **Agent runtime**: aísla session state, memory, tool execution de cada agente. Un fallo en un agente no afecta a otros.
- **runVoidHook** usa Promise.all pero cada handler en su propio try/catch - uno que tira no aborta a los siblings.
- **runModifyingHook** (secuencial, con mergeResults): cada handler en su propio scope guardado.
- **startGatewaySidecars** (src/gateway/server-startup.ts): cada channel en su propio try/catch. OPENCLAW_SKIP_CHANNELS=1 / OPENCLAW_SKIP_PROVIDERS=1 skipea channels.
- **getReplyFromConfig** (agent runtime bulkhead): el path de reply de cada agente confinado - un fallo manejando un mensaje no rompe a otros. (El catch-and-default es pseudocódigo ilustrativo, no literal.)

**Verificación:** ¿Cuál es la distinción clave del Bulkhead en OpenClaw vs el bulkhead clásico?
- OpenClaw es single-process: usa isolation lógica via try/catch por fase de lifecycle, no per-dependency thread pools. Un handler CPU-bound puede stallear siblings, así que el valor es CONTAINMENT, no paralelismo.

## Subnivel 3.2 - Degradación y signaling

### Topic: Graceful degradation ladder

**Teoría:**
- **Graceful degradation ladder**: niveles de funcionalidad cuando componentes fallan. Full operation -> core-only -> read-only diagnostics -> offline.
- **Full operation**: todos los plugins, canales y agentes operativos. (loadOpenClawPlugins carga todo.)
- **Core-only mode**: solo built-in plugins, control channel y main agent. En el pinned commit se produce por plugin enablement resolution (resolveEnableState en config-state.ts) actuando en allow/deny lists y slot bindings. applyTestPluginDefaults es test-only (early-exits salvo VITEST).
- **Read-only diagnostics**: el Gateway responde health y /diagnose pero no procesa mensajes de usuario. El health request handler (src/gateway/server-methods/health.ts) sigue sirviendo. En el pinned commit, los comandos diagnósticos ricos son aspiración, no set fijo.
- **Offline mode**: responde health checks pero no procesa mensajes ni ejecuta tools. (startGatewaySidecars degrada a offline logueando sidecar failures.)
- **Insight del cap**: NO son modos que el código conmuta entre ellos - son **estados observables** en los que el Gateway se asienta a medida que plugins/canales/sidecars fallan. **Reconocer en qué rung estás convierte un outage vago en señal accionable.**

**Verificación:** ¿Los niveles de degradación son modos conmutables o estados observables?
- Son estados observables en los que el sistema se asienta mientras componentes fallan. Reconocer el rung actual transforma un outage vago en señal accionable.

### Topic: Cross-layer error signaling

**Teoría:**
- **Cross-layer error signaling**: preserva el contexto diagnóstico mientras los errores suben por las capas. Cada capa agrega su contexto: plugin ID + hook name + error message + stack trace.
- **Plugin layer** (recordPluginError): registry.diagnostics entry { level, pluginId, source, message }. También detecta API deprecada (api.registerHttpHandler -> usar registerHttpRoute).
- **Hook layer** (handleHookError): preserva hook name + pluginId + error. Tiene flag catchErrors (default true): producción loguea y continúa; tests pasan catchErrors: false para assert el throw.
- **Channel layer** (startGatewaySidecars): loguea "channel startup failed: ..." - el string que los operators grepean.
- **Agent layer** (getReplyFromConfig): preserva agent ID + session key + error message.
- **Common thread**: cada capa **graba antes de recuperar** (record-then-continue), así un operador siempre puede reconstruir qué falló y dónde.

**Verificación:** ¿Cuál es el "common thread" del cross-layer error signaling?
- Cada capa **registra antes de recuperarse** (record-then-continue), preservando el contexto (plugin ID, hook name, source, error) para que un operador reconstruya qué falló y dónde.

## Subnivel 3.3 - Sandboxing y containment

### Topic: Plugin failure isolation

**Teoría:**
- **Plugin failure isolation**: cada fase del plugin (load, register, start, run) está aislada del core del Gateway.
- **Load isolation**: try/catch en getJiti()(safeSource); fallo -> recordPluginError + continue.
- **Register isolation**: register(api) en try/catch; si devuelve una promise se registra diagnostic warn "async registration is ignored" (register debe ser síncrono).
- **Start isolation** (src/plugins/services.ts): startPluginServices envuelve cada service.start en try/catch. Solo los que arrancaron exitosamente se trackean para shutdown posterior (running.toReversed()).
- **Run isolation** (runVoidHook/runModifyingHook): cada hook handler en su propio try/catch.
- **Record-and-skip discipline**: en cada fase, un fallo = diagnostic + skip, nunca halt del Gateway.

### Topic: Sandboxing como ultimate cascade stopper

**Teoría:**
- **Sandboxing**: la última línea de defensa. Es un **fail-closed guard**: configuraciones peligrosas se rechazan ANTES de que arranque el container, no se recuperan después. Aísla el tool execution de plugins en Docker containers con red, filesystem y syscalls restringidos.
- **validateSandboxSecurity()** (src/agents/sandbox/validate-sandbox-security.ts): valida config Docker - binds, network, seccomp, apparmor, dangerouslyAllowContainerNamespaceJoin.
- **Network isolation** (validateNetworkMode): bloquea host (bypasea container network isolation) y container namespace join (container:*). "Use bridge or none". container_namespace_join requiere dangerouslyAllowContainerNamespaceJoin=true solo si confiás el runtime.
- **File system isolation (validateBindMounts)**: rechaza binds que apuntan o cubren rutas bloqueadas del host. BLOCKED_HOST_PATHS: /etc, /proc, /sys, /dev, /root, /boot, /run, /var/run, docker.sock (varias variantes). getBlockedBindReason clasifica non_absolute vs covers vs targets.
- **System call isolation (validateSeccompProfile / validateApparmorProfile)**: rechaza profiles "unconfined" (remover seccomp/AppArmor debilita el sandbox). fail-closed con error descriptivo.
- **Containment en el edge de infraestructura**: última línea antes de que el código alcance el host.

**Verificación:** ¿Qué significa "fail-closed guard" en el sandboxing?
- Las configuraciones peligrosas se **rechazan antes** de que el container arranque, no se detectan/recuperan después. Si no está explícitamente permitido, se bloquea.

### Topic: Per-layer bounded-work containment

**Teoría:**
- **Per-layer backoff budget**: NO es un mecanismo de scheduled-retry ni timeout-budget en el pinned commit. Es **catch-and-continue isolation**: un fallo se captura, se registra UNA vez, y la fase se skipea. "Budget" = "bounded, attempt-once policy".
- **Importancia**: evita que un componente fallando se amplifique en un **retry storm** (recuperación que se vuelve su propia outage).
- **Cada fase** (load, register, start, run, Gateway startup) practica catch-and-continue. Un load/register fallido es un **permanent code fault** que se registra una vez y se skipea, no se reintenta.
- La clarificación del cap: los "budgets" NO son retry con backoff - son attempt-once. La única diferencia es que un service failed en start se loguea pero solo los exitosos se trackan.

## Cierre del nivel

- **Self-review (rúbrica):**
  - Qué salió bien: la distinción Bulkhead lógico (try/catch) vs thread pools es un insight que separa al que lee de memoria del que entiende la arquitectura. El fail-closed del sandbox y la degradation ladder como "estados observables" son conceptos senior.
  - Qué faltó: hands-on de 3 plugins fallidos (requeriría crear plugins de test; complejidad media). Verificar modeSource pendiente (caps 1-2).
- **Pendiente del nivel:** hands-on de failure isolation (3 plugins fallidos) si queremos profundizar en segunda pasada.
- **Badge:** 🧱 Bulkhead (nivel 3 mapeado en primera pasada; XP pendiente de segunda pasada).
