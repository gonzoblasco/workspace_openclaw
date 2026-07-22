---
name: "moderno-access-reset"
description: "Reset completo para Moderno-Access-Virtual-Plate: seguridad, testing, docs y cleanup"
---

# Reset: Moderno-Access-Virtual-Plate

## Contexto

Simulador de placa TNG PRO S201 para desarrollo de integraciones con Moderno Access. Proyecto de un amigo que necesita ayuda para llevarlo a un estado más robusto y usable.

## Problemas detectados

1. **Seguridad débil**: Auth Basic opcional (`MODE=unauthorized`), CORS abierto, credenciales hardcodeadas en `.env`
2. **Vulnerabilidades npm**: 6 CVEs (axios, multer, body-parser, morgan, form-data, qs)
3. **Endpoints incompletos**: `/status.cgi` y `/if.cgi` devuelven solo `OK` sin datos reales
4. **Sin tests**: Cero cobertura, difícil validar cambios
5. **Docs insuficientes**: README básico, sin guía de contribución ni arquitectura
6. **Configuración frágil**: `config.json` grande (1200+ líneas) sin validación de schema
7. **Cloud sync falla silenciosamente**: Error `Invalid URL` sin fallback ni retry
8. **Logs sin rotación**: Acumula indefinidamente en `config.json`

## Plan de Reset

### Fase 1: Seguridad y Salud del Proyecto (Prioridad #1)

```bash
# 1. Fix vulnerabilidades
npm audit fix --force
npm audit # verificar clean

# 2. Crear .env.example seguro (sin creds reales)
cp .env .env.example
# Editar: BOARD_PASS=<generar>, WEBHOOK_URL=http://localhost:3000/api/webhook

# 3. Forzar auth por defecto
# server.js: cambiar MODE=unauthorized como default, no al revés

# 4. Rate limiting básico
npm install express-rate-limit
# Añadir middleware: 100 req/min por IP
```

**Archivos nuevos:**
- `.env.example` (template seguro)
- `.gitignore` actualizado (excluir `.env`, `scratch/uploads/*`)
- `SECURITY.md` (políticas: auth requerida, credenciales por env, no exponer a internet)

### Fase 2: Endpoints Completos + Validación

**Estado actual:**
- `/status.htm` ✅ HTML completo
- `/status.cgi` ⚠️ Solo `OK`
- `/man.cgi?door_on` ✅ Funcional
- `/if.cgi?type=go_user_page` ⚠️ Solo `OK`
- `/if.cgi?type=go_log_page` ⚠️ Solo `OK`

**Implementar:**

```javascript
// /status.cgi -> JSON real
app.get('/status.cgi', authMiddleware, (req, res) => {
    const config = getConfig();
    res.type('text/plain').send(`
var ver="${config.board.version}"
var mac="${config.board.mac}"
var ip="${config.network.ip}"
var uptime="${process.uptime()}"
var users=${config.users.length}
var logs=${config.logs.length}
    `.trim());
});

// /if.cgi?type=go_log_page -> HTML table real
app.get('/if.cgi', authMiddleware, (req, res) => {
    const { type, page = 0 } = req.query;
    const config = getConfig();
    
    if (type === 'go_log_page') {
        const PAGE_SIZE = 20;
        const logs = config.logs.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
        // Renderizar tabla HTML con logs
    }
    
    if (type === 'go_user_page') {
        const PAGE_SIZE = 20;
        const users = config.users.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
        // Renderizar tabla HTML con usuarios
    }
    
    res.send('OK'); // fallback
});
```

**Validación de schema:**
```bash
npm install zod
# Validar config.json al startup y al saveConfig()
```

### Fase 3: Testing (Jest + Supertest)

**Estructura:**
```
tests/
├── setup.js
├── endpoints.test.js   # /status.htm, /status.cgi, /man.cgi, /if.cgi
├── auth.test.js        # Auth Basic, MODE switching
├── cloud-sync.test.js  # syncWithCloud, reportEventToCloud
└── fixtures/
    └── config.test.json
```

**Tests mínimos:**
```javascript
// endpoints.test.js
describe('GET /status.htm', () => {
    it('returns HTML with device info', async () => {
        const res = await request(app).get('/status.htm');
        expect(res.status).toBe(200);
        expect(res.text).toContain('System Status');
        expect(res.text).toContain('TNG PRO');
    });
});

describe('GET /man.cgi?door_on', () => {
    it('opens relay and logs event', async () => {
        const res = await request(app)
            .get('/man.cgi?type=door_on&securitystate=10000000')
            .auth('admin', 'admin');
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
        expect(res.body.relay).toBe(1);
    });
    
    it('rejects without auth', async () => {
        const res = await request(app)
            .get('/man.cgi?type=door_on&securitystate=10000000');
        expect(res.status).toBe(401);
    });
});
```

**Scripts:**
```json
{
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "test:endpoints": "jest endpoints.test.js"
}
```

### Fase 4: Documentación Completa

**Nuevos archivos:**
- `docs/ARCHITECTURE.md` (diagrama de flujo, componentes, state management)
- `docs/API_REFERENCE.md` (todos los endpoints con ejemplos curl)
- `docs/SETUP.md` (instalación paso a paso, troubleshooting)
- `CONTRIBUTING.md` (cómo contribuir, PR template)
- `CHANGELOG.md` (versiones, cambios)

**README.md mejorado:**
- Badge de tests, vulnerabilities, license
- Quick start (3 comandos)
- Tabla de endpoints
- Ejemplo de integración (Node.js + Python)
- FAQ (¿cómo simular latencia?, ¿cómo resetear logs?)

### Fase 5: Cleanup y Organización

**Eliminar:**
- `node_modules/` (si existe en git)
- `scratch/uploads/*` (archivos temporales)
- `backup_modern_ui/` (¿necesario?)
- `firmware_web/`, `firmware_web_extracted/` (¿documentación o binarios?)
- `real_plate_clone/` (¿reverse engineering? documentar o archivar)
- `TNG PRO *.bin`, `*.web` (firmware binaries → ¿licencia?)

**Mover:**
- `API_INTEGRATION.md` → `docs/API_REFERENCE.md`
- Assets estáticos → `public/` consolidado

**config.json:**
- Separar en `config.default.json` (schema completo) y `config.local.json` (overrides)
- Opción: migrar a SQLite para logs/users (más escalable que JSON file)

### Fase 6: Mejoras Opcionales (Post-Reset)

1. **Web UI moderna**: React/Vue dashboard en lugar de HTML legacy
2. **WebSocket**: Push de eventos en tiempo real al dashboard
3. **Dockerfile**: Contenedor para deploy fácil
4. **GitHub Actions**: CI con tests + audit en cada PR
5. **Mock modes**: Simular fallas de red, placa offline, auth inválida
6. **CLI tool**: `moderno-sim open-door 1`, `moderno-sim add-user`, etc.

## Deliverables

- [ ] `npm audit` limpio (0 vulnerabilities)
- [ ] Auth habilitada por defecto
- [ ] Todos los endpoints devuelven datos reales
- [ ] Tests passing (>80% coverage en server.js)
- [ ] Docs completas (README, API_REF, ARCHITECTURE, SETUP)
- [ ] `.env.example` seguro
- [ ] CHANGELOG.md inicial
- [ ] Cleanup de archivos innecesarios

## Riesgos

- **Firmware/binaries**: Verificar licencia antes de redistribuir
- **Cloud sync**: No romper compatibilidad con Moderno real
- **Endpoints CGI**: Mantener compatibilidad exacta con hardware original (alguien puede depender del formato)

## Timeline estimado

- Fase 1-2: 1 sesión (4-6h)
- Fase 3: 1 sesión (3-4h)
- Fase 4: 1 sesión (2-3h)
- Fase 5: 1 sesión (2h)

**Total:** 3-4 sesiones de trabajo enfocado
