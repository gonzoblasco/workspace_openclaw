# Learnings - evaluacion

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## PR-Agent: el review automatico no alcanza el nivel de la revision humana (medido con verdad de base y juez)

PR-Agent (The-PR-Agent/pr-agent) en modo review automatico NO alcanza el nivel de la
revision humana. Medido el 2026-10-20 contra PRs publicos con revisiones humans
reales como verdad de base, con juez independiente.

Caso encode/httpx#3769 (2 revisores humans apuntan al mismo bug central: dentro
del bloque finally, el for sobre self._mounts no tiene try/finally por transporte,
asi que si un mount lanza al cerrar los siguientes quedan ABIERTOS):
- review (--pr_url, gpt-oss): 0 hallazgos
- review (plain-diff, gpt-oss): 1 hallazgo ("Exception Masking") = adyacente, NO
  el bug real
- ask (plain-diff): 5 falsos positivos, veredicto 0/10
- server A2A en Docker: "No major issues detected", veredicto 0/10
- otros 2 modelos cloud (kimi-k2.6, deepseek-v4-pro): 0 hallazgos
- modelo local gemma4:12b-mlx: se cuelga (ctx 262k deja la RAM al 14%, swap 7.8GB)

Caso pydantic/pydantic#13953: 0 hallazgos, los 3 revisores humans lo encontraron.

Veredictos de los jueces (deepseek-v4-pro / kimi-k2.6): 1/10, 0/10, 0/10.

Conclusion: sirve como generador de borradores (describe, improve, primer pase de
ask) y como reviewer de segunda opinion, NO como detector de bugs. La causa no es
la integracion: es la calidad del modelo sobre este tipo de codigo, y el prompt de
pr_reviewer produce salida estructurada pero sin el acierto.

Metodologia que sirvio: usar PRs publicos que YA tienen revisiones humans como
verdad de base, y un juez con modelo DISTINTO al que genero el output. Cuidado
metodologico: el juez hay que darle la verdad de base SOLO del PR evaluado (si se
le mezclan dos PRs, penaliza hallazgos que no correspondian).

---

