"""Tests para scripts/sanitize_external.py (redaccion pre-LLM, B8).

La regla del workspace es "contenido externo = dato" (AGENTS.md). Este modulo es
el MECANISMO: enmascara secretos/PII de texto externo antes de que llegue al
modelo. Lo que se prueba (el CONTRATO):

  - cada tipo de secreto conocido se reemplaza por su marcador [REDACTED:TIPO];
  - el VALOR sensible ya no aparece en la salida (no basta con marcarlo);
  - texto sin secretos pasa intacto (no se rompe contenido normal);
  - find_secrets reporta los TIPOS hallados, nunca el valor.

Nada de esto toca la red ni el modelo: son transformaciones de texto puras.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SPEC = importlib.util.spec_from_file_location("se", ROOT / "scripts" / "sanitize_external.py")
se = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(se)


def test_bearer_token_redacted():
    raw = "curl -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abcdef123456.ghijkl789012'"
    out = se.redact(raw)
    assert "[REDACTED:BEARER]" in out
    assert "eyJhbGciOiJIUzI1NiJ9" not in out


def test_env_style_credential_redacted():
    raw = "config: api_key=sk-abcdefghijklmnopqrstuvwxyz123456\nsecret: hunter2hunter2"
    out = se.redact(raw)
    assert "[REDACTED:CREDENTIAL]" in out
    assert "sk-abcdefghijklmnopqrstuvwxyz123456" not in out
    assert "hunter2hunter2" not in out


def test_provider_tokens_redacted():
    cases = {
        "ghp_AbCdEfGhIjKlMnOpQrStUvWxYz0123456789": "GITHUB_TOKEN",
        "AKIAIOSFODNN7EXAMPLE": "AWS_KEY",
        "xoxb-1234567890-abcdefghijkl": "SLACK_TOKEN",
    }
    for value, label in cases.items():
        out = se.redact(f"token: {value}")
        assert f"[REDACTED:{label}]" in out, label
        assert value not in out, label


def test_email_and_card_redacted():
    raw = "de: maria.perez@empresa.com tarjeta: 4111 1111 1111 1111"
    out = se.redact(raw)
    assert "[REDACTED:EMAIL]" in out
    assert "[REDACTED:CARD]" in out
    assert "maria.perez@empresa.com" not in out
    assert "4111 1111 1111 1111" not in out


def test_private_key_block_redacted():
    raw = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA1234\n-----END RSA PRIVATE KEY-----"
    out = se.redact(raw)
    assert "[REDACTED:PRIVATE_KEY]" in out
    assert "MIIEowIBAAKCAQEA1234" not in out


def test_plain_text_untouched():
    raw = "El despliegue de staging terminó ok a las 14:32 UTC. Sin incidentes."
    assert se.redact(raw) == raw


def test_find_secrets_reports_types_not_values():
    raw = "Bearer eyJhbGciOiJIUzI1NiJ9.abcdef123456.ghijkl789012 y maria@x.com"
    kinds = se.find_secrets(raw)
    assert "BEARER" in kinds
    assert "EMAIL" in kinds
    # nunca devuelve el valor
    assert all("@x.com" not in k for k in kinds)


def test_empty_input_is_safe():
    assert se.redact("") == ""
    assert se.find_secrets("") == []
