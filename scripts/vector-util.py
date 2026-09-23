#!/usr/bin/env python3
"""
vector-util.py - Codificacion de embeddings para memory.db.

Antes: los vectores se guardaban como JSON de texto (1024 floats -> ~22 KB).
Ahora: BLOB de float32 little-endian (1024 floats -> 4096 bytes). Ahorro: ~82%.

Por que importa: el 77% de memory.db eran vectores en JSON. Con ~168 vectores
nuevos por mes, el JSON crecia a ~3.6 MB/mes. En BLOB, ~0.66 MB/mes.

Compatibilidad: `decode` acepta AMBOS formatos (BLOB nuevo, JSON legacy), asi
que la migracion puede correr por partes sin romper nada y los scripts viejos
siguen leyendo. `encode` siempre escribe BLOB.

Uso:
    from vector_util import encode, decode, is_json
    blob = encode([0.1, 0.2, ...])      # -> bytes
    vec  = decode(row[0])                # <- list[float], acepta bytes o str
"""
import json
import struct

FMT = "<%df"  # little-endian float32 (formato NATIVO de sqlite-vec y la mayoria de los stacks)

# LIMITACION CONOCIDA: no hay forma de distinguir un BLOB float32 de un
# byte-string arbitrario cuyo largo sea multiplo de 4 - ambos decodifican a
# una lista de floats. En memory.db la columna contiene UNA de las dos cosas
# (JSON legacy o BLOB nuevo), garantizado por migrate-vectors.py, asi que la
# ambiguedad no se presenta. Si alguna vez una columna pudiera tener otra
# cosa, haria falta una marca explicita de formato (una columna `format`).


def encode(vec) -> bytes:
    """list[float] -> BLOB float32. Lanza si no es una secuencia numerica."""
    if isinstance(vec, (bytes, bytearray)):
        return bytes(vec)
    if isinstance(vec, str):
        vec = json.loads(vec)
    return struct.pack(FMT % len(vec), *vec)


def decode(value):
    """BLOB o JSON-text -> list[float]. Acepta ambos por compatibilidad.

    Orden de intentos para bytes: primero JSON solo si el contenido ARRANCA
    como JSON y parsea; si no, float32. Chequear solo el primer byte no sirve:
    el byte inicial de un float32 puede ser 0x5B ('[') por azar. El parseo
    fallido sobre binario es lo que da la certeza.
    """
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray, memoryview)):
        raw = bytes(value)
        if raw.lstrip()[:1] in (b"[", b"{"):
            try:
                return json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass  # era binario que empezaba con '[': seguir a float32
        if len(raw) % 4 == 0:
            return list(struct.unpack(FMT % (len(raw) // 4), raw))
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return None


def is_json(value) -> bool:
    """True si el valor esta en el formato viejo (texto JSON), no en BLOB."""
    if isinstance(value, str):
        return True
    if isinstance(value, (bytes, bytearray, memoryview)):
        raw = bytes(value)
        if raw.lstrip()[:1] in (b"[", b"{"):
            try:
                json.loads(raw.decode("utf-8"))
                return True
            except (UnicodeDecodeError, json.JSONDecodeError):
                return False
        return False
    return False


def dims(value):
    """Dimensiones del vector, o None si no se puede decodificar."""
    v = decode(value)
    return len(v) if v is not None else None


def cosine(a, b):
    """Similitud coseno. Acepta BLOB o JSON en cualquiera de los dos lados."""
    va, vb = decode(a), decode(b)
    if not va or not vb or len(va) != len(vb):
        return 0.0
    dot = sum(x * y for x, y in zip(va, vb))
    na = sum(x * x for x in va) ** 0.5
    nb = sum(x * x for x in vb) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


if __name__ == "__main__":
    import sys

    vec = [0.5, -0.25, 1.0]
    blob = encode(vec)
    assert decode(blob) == vec, "roundtrip BLOB fallo"
    assert decode(json.dumps(vec)) == vec, "decode de JSON fallo"
    assert is_json(json.dumps(vec)) and not is_json(blob)
    assert dims(blob) == 3 and dims(json.dumps(vec)) == 3
    assert abs(cosine(blob, json.dumps(vec)) - 1.0) < 1e-6
    print("vector-util: OK (roundtrip, compat JSON, dims, coseno)")
    sys.exit(0)
