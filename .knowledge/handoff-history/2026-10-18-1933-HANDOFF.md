# HANDOFF - workspace

**Fecha:** 2026-10-14 13:23 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-14). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-14.md`.

---

## Que se hizo en esta sesion

Consulta de Gonzo sobre un curso de n8n de Instituto Linux (Automatizaciones con n8n, vibe code e IA, 12 clases/21h, miercoles y viernes 20:15-22:00, 23/10 al 02/12/2026, certifica UTN-FRD Res. 430/26). Precio lista $500.000; promo alumnos/exalumnos $250.000 hasta el viernes 16/10. Leimos la pagina completa (curl) y evaluamos el match contra el perfil real de Gonzo: el curso apunta a 'sysadmins que no vienen de la programacion', Gonzo ya domina Docker, Postgres, agentes y flujos con IA, por lo que el Bloque A (80% ya sabido) y el Bloque B (vibe coding, ya lo hace mejor con OpenClaw) aportan poco; el valor real es (a) n8n como herramienta nueva y (b) el certificado UTN-FRD. Se le advirtio que el descuento de exalumno es una CONDICION a validar (hizo un curso devops sin terminar) y debe preguntarlo por WhatsApp ANTES del 16/10; inscripcion por link /inscripcion-alumnos/. Punto de metodo: al delegar/ser asistido, los JSON de los workflows los debe entender el, no recibirlos hechos (si hace el integrador evaluado, no puede delegar el entendimiento). Roadmap: se confirmo que roadmap.sh NO tiene track dedicado de n8n (su /n8n da 404; n8n aparece solo mencionado dentro de otros roadmaps); Gonzo aporto un PDF del roadmap de n8n que SI existe como ruta de aprendizaje. Se acordo dejar el material en INGLES (la herramienta, doc y UI estan en ingles) con un glosario ES->EN al costado. Se diseno un plan de estudio propio derivado del roadmap, en 5 fases + proyecto integrador (webhook -> DB -> IA -> reporte -> Telegram), con entregable por fase (flujo real + JSON exportado), a construir en el workspace (carpeta n8n/) cuando Gonzo lo dispare. IDEA EVALUADA: montar n8n local en Docker en la Mac Mini a la par de OpenClaw (capa visual de scripts determinista, complemento del orquestador); n8n expone MCP, asi que OpenClaw podria llamar workflows como herramienta. SEGUNDA IDEA (descartada): correr OpenClaw en Docker para usarlo indistintamente en la Mac Air y la Mini. Se aclaro el malentendido: DOCKER NO SINCRONIZA - un contenedor es aislado y efimero en una sola maquina; replicar la imagen copia software, no estado (DB/sesiones/credenciales). Sincronizar estado es otra capa. OpenClaw tiene un gateway activo por vez (dos se pisan), estado vivo persistente (~/.openclaw) y canales atados a identidad (duplicacion). Segun ADR-073 el gateway vive en la Mini por diseno: la Air debe ACCEDER a la Mini (Control UI/webchat/SSH/nodo pareado), no replicarla. Quedo abierta la decision A (cliente vs gateway) vs C (estado compartido real, failover manual, riesgo de corrupcion de DB si ambas encendidas) pendiente de que Gonzo aclare uso real y frecuencia de la Air. DECISION DE GONZO: olvidar Docker para OpenClaw, cerrar el tema del curso n8n en esta conversacion, guardar sesion y no seguir por aca ('esta se borra') - el material de n8n se retomara por otro lado.

## Estado actual

Tema cerrado a pedido de Gonzo. Pendientes fuera de esta conversacion: (1) WhatsApp al Instituto Linux para confirmar si el descuento de exalumno aplica pese a no haber terminado el curso devops, antes del viernes 16/10; (2) decidir el viernes si paga el curso con el roadmap + Fase 1 ya hecha; (3) arrancar el plan de estudio n8n/ (plan + n8n en Docker + Fase 1) cuando Gonzo lo dispare por otro lado.

## Proximos pasos

1. Retomar n8n por otro lado: extraer el roadmap (PDF) a plan de estudio en el workspace, levantar n8n en Docker en la Mini y hacer la Fase 1 (primer flujo real). No delegar el armado de JSON en un curso evaluado.

## Decisiones y contexto que no debe perderse

- Docker no sincroniza estado: descartado para OpenClaw en dos Macs (ADR-073: un gateway en la Mini, la Air accede). Material de n8n en ingles + glosario ES->EN. Roadmap.sh no tiene track de n8n. El valor del curso = certificado UTN-FRD (convenio, no carrera) + herramienta nueva, no el temario.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-14.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
