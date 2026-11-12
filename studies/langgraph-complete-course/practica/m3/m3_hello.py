"""Modulo 3 - Grafo minimo: START -> nodo -> END.

Corre:  ../../../../projects/oss-post-graph/venv/bin/python m3_hello.py
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """Nodo simple que agrega un saludo al estado."""
    state["message"] = "hey " + state["message"] + ", how is your day going?"
    return state


builder = StateGraph(AgentState)
builder.add_node("greeter", greeting_node)
builder.add_edge(START, "greeter")
builder.add_edge("greeter", END)

app = builder.compile()          # <- el grafo NO corre hasta aca no mas
result = app.invoke({"message": "gonzo"})
print("salida:", result)
print("tipo  :", type(result).__name__)
