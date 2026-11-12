"""Las tres trampas del Modulo 3, reproducidas."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    message: str

# --- TRAMPA 1: nodo que NO devuelve el estado ---
def no_return(state):
    state["message"] = "mutado pero no devuelto"
    # falta: return state

b = StateGraph(AgentState)
b.add_node("x", no_return)
b.add_edge(START, "x")
b.add_edge("x", END)
try:
    print("[1] sin return ->", b.compile().invoke({"message": "hola"}))
except Exception as e:
    print("[1] sin return ->", type(e).__name__, ":", e)

# --- TRAMPA 2: invoke sobre el builder sin compilar ---
b2 = StateGraph(AgentState)
b2.add_node("g", lambda s: s)
try:
    b2.invoke({"message": "x"})
except Exception as e:
    print("[2] invoke sin compile ->", type(e).__name__, ":", str(e)[:80])

# --- TRAMPA 3: clave NO declarada en el TypedDict ---
def writes_undeclared(state):
    state["extra"] = "no declarada"
    return state
b3 = StateGraph(AgentState)
b3.add_node("w", writes_undeclared)
b3.add_edge(START, "w")
b3.add_edge("w", END)
out = b3.compile().invoke({"message": "x"})
print("[3] clave no declarada ->", out)
print("    'extra' viaja igual?", "extra" in out)
