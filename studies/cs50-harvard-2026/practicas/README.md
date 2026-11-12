# Prácticas — CS50 2026

Scripts ejecutables por unidad. **No son respuestas en papel**: corren, verifican y fallan cuando deben.

## U0 — Scratch: el modelo mental

```bash
cd studies/cs50-harvard-2026/practicas/u00
python3 e1_binario.py    # decimal -> binario, a mano vs máquina
python3 e2_ascii.py      # ASCII a mano + el bit que separa caja
python3 e3_cartas.py --shuffle-seed 42   # el algoritmo de 8 cartas, ejecutado
python3 e4_bytes.py      # "todo es bytes", medido en esta máquina
python3 test_practicas.py                # la suite: 18 checks
```

| Script | Qué prueba |
|---|---|
| `e1_binario.py` | 1, 7, 65, 128, 255 a mano; por qué 255 y no 256 |
| `e2_ascii.py` | `HI!`/`hi!` decodificado; mayúscula = minúscula + 1 bit |
| `e3_cartas.py` | El pseudocódigo del outline, ejecutado. Selección de la menor por vuelta; 28 comparaciones = n(n-1)/2 |
| `e4_bytes.py` | `'á'` son 2 bytes en UTF-8 y 1 en Latin-1; `'canción'` 7 caracteres / 8 bytes |
| `test_practicas.py` | **El algoritmo roto tiene que fallar.** Si el test solo corre en el caso feliz, no prueba nada |

### La regla del test honesto

`test_practicas.py` tiene una implementación **rota a propósito** (una sola pasada, no ordena) y exige que falle. Si algún día el "roto" ordena, el test se rompe y avisa: significa que dejó de distinguir bueno de malo.

Esto sale del repo, no del curso: en el cierre de E0 de Reinos de la Frontera, un test imprimía `DAY1_OK` **después** de fallar. CS50 no enseña testing; este workspace sí.

---

_Sesión 2026-11-11. Python 3.9+._

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
