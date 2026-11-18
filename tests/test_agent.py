import json
from unittest import mock

from src.agent import agent as ag


def fake_hybrid_search(conn, query, top_k=8):
    # return list of (id, text)
    return [(1, "Este es un texto de chunk con la frase clave."), (2, "Otro chunk sin coincidencia.")]


def fake_ollama_chat(*, model, messages, format):
    # Return a valid JSON with a citation that matches first chunk
    return {
        "message": {
            "content": json.dumps({
                "answer": "Respuesta ficticia",
                "citations": [{"chunk_id": 1, "quote": "frase clave"}],
                "confidence": 0.9,
            })
        }
    }


@mock.patch("src.agent.agent.hybrid_search", side_effect=fake_hybrid_search)
@mock.patch("ollama.chat", side_effect=fake_ollama_chat)
def test_answer_question_valid(mock_chat, mock_search):
    result = ag.answer_question(None, "pregunta?")
    assert result["answer"] == "Respuesta ficticia"
    assert len(result["citations"]) == 1


def fake_ollama_chat_invalid(*, model, messages, format):
    return {
        "message": {"content": json.dumps({"answer": "bad", "citations": [{"chunk_id": 2, "quote": "no coincide"}], "confidence": 0.5})}
    }


@mock.patch("src.agent.agent.hybrid_search", side_effect=fake_hybrid_search)
@mock.patch("ollama.chat", side_effect=fake_ollama_chat_invalid)
def test_answer_question_refusal(mock_chat, mock_search):
    result = ag.answer_question(None, "pregunta?")
    assert result["answer"].startswith("I cannot provide")
