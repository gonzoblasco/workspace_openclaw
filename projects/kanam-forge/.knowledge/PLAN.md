# Kanam Forge — PLAN

**Sueño:** Un Lovable cloud + AI self-hosted que construya proyectos completos con el pipeline de Gonzo (stack opinado, memoria persistente, a11y integrada, multi-agente). No un generador de landings - un creador de proyectos completos estilo soporteml v1, pero con estándar superior.

**MVP actual:** Local con Docker, para uso personal. Fork de Adorable (freestyle-sh/Adorable, MIT) con el sandbox Freestyle cloud reemplazado por Docker local + Supabase self-hosted + Ollama local.

**Decisiones clave (2026-08-17):**
- **Supabase self-hosted** (no cloud) - decisión de Gonzo. Opción A: stack central compartido, schema por app. Ya hay experiencia previa (sportcars, kanam/daily-ink).
- **LLM = Ollama local** como router (Lovable AI analógico). Vercel AI SDK soporta Ollama. Cero costo, privacidad.
- **Docker local** como sandbox (reemplaza Freestyle cloud).

---

## 1. Qué es Adorable (hallazgo del análisis)

Repositorio MIT de freestyle.sh. Es un **orquestador de app-building conversacional**:

- Next.js 16, React 19, assistant-ui, Vercel AI SDK (OpenAI + Anthropic)
- Chat que habla con un agente que escribe/edita/ejecuta código
- Preview en vivo (iframe), terminales embebidas (ttyd), publish con un clic
- 13 tools de agente: bash, read/write/list/search/replace/append file, mkdir/mv/rm, commit+push, checkApp (verifica que la app no esté rota), devServerLogs
- Persistencia: cada proyecto es un repo git con metadata + conversaciones

**Clave:** las 13 tools usan SOLO la interfaz `vm.exec()` + `vm.fs.*`. Son agnósticas del backend.

## 2. El acoplamiento a Freestyle (lo que hay que reemplazar)

**Mapa real (8 archivos):**

| Archivo | Uso de Freestyle | Reemplazo |
|---|---|---|
| `lib/adorable-vm.ts` | `freestyle.vms.create()` - crea VM cloud | Docker container local por proyecto |
| `lib/create-tools.ts` | `vm.exec()`, `vm.fs.*` | Adaptador Docker con la MISMA interfaz |
| `lib/repo-storage.ts` | `freestyle.git.repos` - persiste metadata/conversaciones | git local en disco (fs) |
| `lib/identity-session.ts` | auth de Freestyle | Eliminar (local, sin auth) |
| `lib/deployment-status.ts` | `freestyle.serverless.deployments` | Stub/descartar (sin serverless en MVP) |
| `app/api/repos/route.ts` | lista/crea repos git de Freestyle | Descubrimiento de proyectos locales (fs) |
| `app/api/chat/route.ts` | `freestyle.vms.ref()` - reconectar VM | Referencia a container Docker local |
| `app/api/repos/[repoId]/promote/route.ts` | deploy serverless | Stub/descartar (sin deploy en MVP) |

**La UI es agnóstica** - consume `previewUrl`, `devCommandTerminalUrl`, `additionalTerminalsUrl` como URLs. Para Docker local apuntan a puertos del container.

## 2b. Modelo de proyecto local (reemplazo del wrapper repo)

Cada proyecto es una carpeta en disco (`~/.kanam-forge/projects/<id>/`):

```
<id>/
├── workspace/        # código del proyecto (git propio, donde escribe el agente)
│   ├── package.json
│   ├── app/...
│   └── .git/
├── metadata.json     # RepoMetadata (vm, conversaciones, deployments)
└── conversations/    # historial por conversacion
```

Simplifica el modelo de Adorable (source repo + wrapper repo separados) a uno directo. Es el estilo de Gonzo.

## 3. Arquitectura del MVP (Docker local + Supabase self-hosted + Ollama)

```
┌────────────────────────────────────────────────────────────┐
│  App Next.js (Kanam Forge) - localhost:3000               │
│  chat + preview iframe + terminales                       │
└───────────────┬───────────────────────┬───────────────────┘
                │ docker exec / API     │
        ┌───────▼──────────┐   ┌────────▼───────────┐
        │ Docker container │   │ Ollama local       │
        │ (por proyecto)   │   │ (router LLM)       │
        │ Node+Next+git+   │   └────────────────────┘
        │  ttyd            │
        │ p3000 preview    │   ┌────────────────────┐
        │ p3010 ttyd dev   │   │ Supabase self-host │
        │ p3020 ttyd extra │   │ (stack central)    │
        └──────────────────┘   │ schema por app     │
                               └────────────────────┘
```

**Adaptador `docker-vm.ts`:** implementa la interfaz `{ exec(command), fs: { readTextFile, writeTextFile, readFile } }` usando `docker exec` + volumen montado. Las 13 tools de `create-tools.ts` NO se tocan.

## 4. Decisiones tomadas (2026-08-17)

- **Imagen Docker:** A - Node + Next.js base + git (MVP rápido). Biome/create-stack en Fase 2.
- **Persistencia:** A - volumen local por proyecto (`~/.kanam-forge/projects/<id>/`). Doble git con `.knowledge/` como evolución.
- **Agente:** único en MVP. Multi-agente en Fase 3.
- **Nombre:** Kanam Forge.

## 5. Fases de ejecución

### Fase 0 - Fundamentos ✅ (2026-08-17)
- [x] Proyecto con .knowledge/ (BRIEF, STATUS, PLAN)
- [x] Fork → gonzoblasco/kanam-forge, upstream freestyle-sh/Adorable
- [x] npm install + build baseline (fix TS en attachment.tsx)
- [x] .env.example + ApiKeyGate de la UI

### Fase 1 - Desacoplar Freestyle → Docker local (núcleo)
- [ ] Definir arquitectura local + actualizar PLAN (EN CURSO)
- [ ] docker-vm.ts (interfaz exec/fs via Docker)
- [ ] Dockerfile base (Node + Next.js + git + ttyd)
- [ ] Reemplazar repo-storage.ts + identity-session.ts → git local en disco
- [ ] Reemplazar adorable-vm.ts + api/repos/route.ts + api/chat/route.ts → Docker local
- [ ] Stub deployment-status.ts + promote (sin serverless en MVP)
- [ ] **HITO:** loop completo local (chat → código → dev server → preview → checkApp → commit)
- [ ] Supabase central compartido + integración de backend en apps generadas

### Fase 2 - Pipeline Gonzo + Ollama local
- [ ] Sistema prompt con stack opinado (Biome, pre-commit, ADRs, a11y)
- [ ] LLM provider Ollama local (reemplaza OpenAI/Anthropic cloud)
- [ ] Template create-stack-next + hooks
- [ ] Memoria de proyecto persistente (.knowledge/)

### Fase 3 - Multi-agente (visión)
- [ ] Agente A escribe → Agente B revisa (cross-review a11y + calidad)
- [ ] Escalamiento a proyectos completos tipo soporteml

### Fase 4 - Cloud (sueño final)
- [ ] Servidor propio de VMs Docker + dominio
- [ ] Publish multi-tenant
- [ ] Producto

## 6. Riesgos / a considerar

- **Preview del iframe:** el dev server de Next necesita bind a `0.0.0.0` dentro del container (no `localhost`) para que el host lo vea.
- **ttyd:** incluir en la imagen Docker (o alternativa). Es lo que da los terminales web.
- **Hot reload a través de volúmenes:** el bind mount puede ralentizar el HMR de Next.js. Evaluar volumen nombrado vs bind mount.
- **Multi-proyecto:** cada proyecto = un container. Para MVP con pocos proyectos va bien; para muchos, evaluar un solo container multi-workdir o docker compose.

## 7. Stack técnico del MVP

- Fork Adorable: Next.js 16, React 19, assistant-ui, Vercel AI SDK
- LLM: OpenAI (gpt-5.2-codex / gpt-5-mini) o Anthropic (claude-sonnet) - configurable via `.env`
- Docker: container por proyecto con Node LTS + Next.js + git + ttyd
- Orquestación: Docker CLI / dockerode (SDK Node para manejar containers)
