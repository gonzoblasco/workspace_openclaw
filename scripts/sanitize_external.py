#!/usr/bin/env python3
"""
sanitize-external.py - Redacta secretos y PII de contenido externo ANTES de que
llegue al modelo (B8).

Contexto (2026-10-12): la regla del workspace es "contenido externo = dato"
(AGENTS.md, secc. Conducta), pero teniamos la REGLA sin un MECANISMO. Este modulo
es ese mecanismo: toma texto que entro del mundo exterior (un email, un webhook,
un issue, una pagina) y enmascara credenciales/PII antes de inyectarlo en
cualquier prompt.

No es un detector de riesgo (eso es scripts/security-scan.py, que REPORTAla
presencia de patrones peligrosos en CODIGO). Esto es un REDACTOR: reemplaza el
valor sensible por un marcador estable, de modo que el contenido sigue siendo
utilizable por el modelo sin filtrar secretos.

Uso:
    from sanitize_external import redact
    safe = redact(raw_external_text)          # -> texto con [REDACTED:...]

    CLI:  sanitize-external.py < archivo   (o  ... <file>)
"""

import re
import sys

# Patrones de secretos/PII. El orden importa: los mas especificos primero.
# Los marcadores son estables ([REDACTED:TIPO]) para que el modelo entienda que
# hubo un dato sensible sin verlo.
PATTERNS = [
    # Tokens con prefijo conocido (Bearer y esquemas comunes).
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"), "Bearer [REDACTED:BEARER]"),
    # Claves AWS.
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED:AWS_KEY]"),
    # Tokens de proveedor comunes (GitHub, Slack, Stripe, OpenAI, Google).
    # Van ANTES del patron generico de credential: un `token: ghp_...` debe
    # llevar la etiqueta especifica, no la generica (descubierto en test).
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[REDACTED:GITHUB_TOKEN]"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "[REDACTED:SLACK_TOKEN]"),
    (re.compile(r"\b(sk|pk)_(live|test)_[A-Za-z0-9]{16,}\b"), "[REDACTED:STRIPE_KEY]"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "[REDACTED:OPENAI_KEY]"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "[REDACTED:GOOGLE_KEY]"),
    # Bloques PEM (claves privadas).
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
     "[REDACTED:PRIVATE_KEY]"),
    # JWT (tres segmentos base64url).
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
     "[REDACTED:JWT]"),
    # Claves tipo KEY=valor (env, config, logs) - generico, va DESPUES de los
    # proveedores especificos para no robarles la etiqueta.
    (re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|token|access[_-]?key)"
                r"(\s*[:=]\s*)(['\"]?)([A-Za-z0-9._~+/=-]{8,})(['\"]?)"),
     r"\1\2\3[REDACTED:CREDENTIAL]\5"),
    # Email.
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED:EMAIL]"),
    # Numero de tarjeta (13-16 digitos, con separadores opcionales).
    (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[REDACTED:CARD]"),
]


def redact(text: str) -> str:
    """Enmascara secretos/PII en `text`. Devuelve el texto saneado."""
    if not text:
        return text
    out = text
    for pattern, replacement in PATTERNS:
        out = pattern.sub(replacement, out)
    return out


def find_secrets(text: str):
    """Devuelve la lista de TIPOS de dato sensible hallados (sin el valor).

    Util para metricas/auditoria: "cuantos y de que tipo", nunca el contenido.
    """
    if not text:
        return []
    found = []
    for pattern, replacement in PATTERNS:
        marker = re.search(r"\[REDACTED:([A-Z_]+)\]", replacement)
        label = marker.group(1) if marker else "SECRET"
        if pattern.search(text):
            found.append(label)
    return found


def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ("-",):
        raw = open(sys.argv[1], encoding="utf-8").read()
    else:
        raw = sys.stdin.read()
    sys.stdout.write(redact(raw))


if __name__ == "__main__":
    main()
