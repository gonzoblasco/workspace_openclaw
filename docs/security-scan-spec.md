# Security Scan Engine (Kanam OS) 🌿

> **Estado: ADOPTADO (2026-10-06).** Cableado al pre-commit como `scripts/security-scan.py --staged` (gate sobre el código ejecutable que entra bajo un árbol de skills). Implementación: `scripts/security-scan.py`.

Este script es el primer "Gate" de la Etapa 2. Su función es analizar archivos de código o scripts antes de que sean integrados al workspace para prevenir vulnerabilidades críticas.

## 🛡️ Matriz de Detección

El motor busca patrones específicos divididos en 4 categorías de riesgo:

### 1. Inyección y Ejecución (Riesgo Alto)
- **Shell Injection:** Uso de `eval()`, `os.system()`, `subprocess.Popen(shell=True)` con variables no sanitizadas.
- **Path Traversal:** Uso de `../` en rutas dinámicas, acceso a `/etc/passwd` o archivos sensibles del sistema.
- **Obfuscación:** Detecta el uso de `base64.b64decode()`, `exec()` de strings dinámicos o caracteres Unicode invisibles (Trojan Source).

### 2. Exfiltración de Datos (Riesgo Alto)
- **Network Leaks:** Llamadas a `curl`, `wget` o `requests.post` hacia dominios desconocidos o IPs sospechosas.
- **Secret Leaks:** Búsqueda de patrones de API Keys, Tokens o contraseñas hardcodeadas.

### 3. Prompt Overrides (Riesgo Medio)
- **Instrucciones Ocultas:** Búsqueda de frases como "ignore previous instructions", "you are now an admin", o "system prompt override" dentro de archivos de configuración o prompts.
- **Indirect Injection:** Análisis de archivos que cargan contenido externo y lo pasan directamente a un LLM sin filtrado.

### 4. Dependencias Sospechosas (Riesgo Medio)
- **Typosquatting:** Comparación de dependencias contra una lista de paquetes comunes para detectar errores ortográficos malintencionados.
- **Post-install Hooks:** Alerta sobre scripts de `npm install` que ejecuten binarios no verificados.

---

## 🚦 Flujo de Decisión

| Resultado | Estado | Acción Obligatoria |
| :--- | :--- | :--- |
| **Limpio** | ✅ PASS | Integración permitida. |
| **Sospechoso** | ⚠️ WARN | Requiere revisión manual del Core y aprobación de Gonzo. |
| **Peligroso** | ❌ FAIL | Bloqueo inmediato. El archivo debe ser eliminado o saneado. |

---

*Actualizado el 2026-10-01. Parte del Sprint 2.1 - Ciclo de Vida de la Skill.*
