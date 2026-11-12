"""Por que un nodo sin return no rompe: la mutacion se ve, el update no."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict):
    a: str
    b: str

def mutates_only(state):
    state["a"] = "mutado-en-sitio"
    # NO return
def mutates_and_returns(state):
    state["b"] = "mutado-y-devuelto"
    return state

# caso A: nodo unico sin return
g = StateGraph(S); g.add_node("n", mutates_only); g.add_edge(START,"n"); g.add_edge("n",END)
print("A) sin return, un nodo      ->", g.compile().invoke({"a":"a0","b":"b0"}))

# caso B: DOS nodos; el primero muta sin devolver, el segundo LE EL ESTADO
def second(state):
    state["b"] = "segundo vio: " + state["a"]
    return state

g2 = StateGraph(S)
g2.add_node("one", mutates_only)
g2.add_node("two", second)
g2.add_edge(START,"one"); g2.add_edge("one","two"); g2.add_edge("two",END)
print("B) sin return + nodo q lee  ->", g2.compile().invoke({"a":"a0","b":"b0"}))

# caso C: con valor devuelto y sin mutacion
def returns_new(state):
    return {"a": "devuelto-como-update"}
g3 = StateGraph(S); g3.add_node("n", returns_new); g3.add_edge(START,"n"); g3.add_edge("n",END)
print("C) return de update parcial ->", g3.compile().invoke({"a":"a0","b":"b0"}))
