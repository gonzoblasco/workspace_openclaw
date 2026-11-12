"""Modulo 1 - Anotaciones de tipo: la parte que el curso da por garantia y no lo es.

Corre: python3 m1_types.py
"""
from typing import TypedDict, Union, Optional, Any


# --- 1. TypedDict: la forma del estado, sin validacion en runtime ---
class Session(TypedDict):
    user: str
    minutes: int
    notes: str
    done: bool


# --- el ejercicio: instanciar con 'minutes' como string (dato invalido) ---
session: Session = {
    "user": "gonzo",
    "minutes": "treinta",      # <-- int declarado, string en runtime
    "notes": "modulo 1",
    "done": False,
}
print("[1] session instanciada con minutes como string:")
print("    ", session)
print("     TypeError? no. Python no valida TypedDict en runtime.")


# --- 2. La prueba dura: un checker SI lo detecta, y ahi esta el valor real ---
print("\n[2] el tipo no protege en runtime, pero si en el editor/checker.")
print("     mypy sobre este archivo debe fallar en la linea de 'minutes'.")


# --- 3. Union: acepta dos tipos, y falla por la operacion, no por la anotacion ---
def square(x: Union[int, float]) -> float:
    return x * x


print("\n[3] square(5) =", square(5), "| square(1.5) =", square(1.5))
try:
    print(square("I am a string"))  # type: ignore[arg-type]
except TypeError as e:
    print("     square('I am a string') -> TypeError:", e)
    print("     (falla por multiplicar, no por la anotacion)")


# --- 4. Optional[str] es exactamente Union[str, None] ---
def nice_message(name: Optional[str] = None) -> str:
    return f"hi there {name}" if name else "hey random person"


print("\n[4] nice_message('Bob') =", nice_message("Bob"))
print("     nice_message()      =", nice_message())
print("     Optional[str] == Union[str, None] ->", Optional[str] == Union[str, None])


# --- 5. Any: el agujero ---
def print_value(v: Any) -> None:
    print("     print_value ->", repr(v))


print("\n[5] Any acepta todo (y por eso no dice nada):")
for v in ("un string", 42, [1, 2], {"k": "v"}, None):
    print_value(v)


# --- 6. Lo que de verdad importa para el curso: el None que aparece solo ---
class GraphState(TypedDict):
    message: str
    final: str


partial: GraphState = {"message": "hi"}  # type: ignore[typeddict-item]
print("\n[6] clave no pasada en el estado:")
print("     ", partial)
print("     state.get('final') ->", partial.get("final"))
print("     'final' in state   ->", "final" in partial)
