#!/usr/bin/env python3
"""Práctica 5 — HMM y filtrado: el estado real está oculto.

Hasta acá el mundo era visible: se preguntaba por una variable de una red. Con
estado dinámico, el estado cambia con el tiempo y sólo se observan emisiones.
El modelo de la clase es la cadena de Markov oculta (HMM):

  - estados ocultos S1, S2, ... (¿está lloviendo hoy?)
  - transiciones P(S_t | S_{t-1})       la suposición de Markov: sólo importa ayer
  - emisiones   P(E_t | S_t)            sólo se ve la emisión

Filtrado: P(S_t | E_1..E_t). Se actualiza recursivamente:

  predicción:   P(S_t) = Σ P(S_t | S_{t-1}) P(S_{t-1} | E_1..E_{t-1})
  actualización: P(S_t | E_t) ∝ P(E_t | S_t) · P(S_t)

Eso es todo. La práctica lo implementa y lo contrasta contra el método de
fuerza bruta (enumerar todas las historias) para verificar que coincide.
"""
import itertools
import sys


STATES = ['sol', 'lluvia']
EMISSIONS = ['paraguas', 'sin']

# Transición: ¿el clima de mañana dado el de hoy? (el curso usa el clima de la
# ciudad vecina, pero acá es el mismo día siguiente)
TRANS = {
    'sol': {'sol': 0.90, 'lluvia': 0.10},
    'lluvia': {'sol': 0.30, 'lluvia': 0.70},
}
# Emisión: la misma evidencia (paraguas) tiene que ser MUCHO más probable con
# lluvia que con sol, si queremos que filtrar aprenda algo.
EMIT = {
    'sol': {'paraguas': 0.10, 'sin': 0.90},
    'lluvia': {'paraguas': 0.90, 'sin': 0.10},
}
PRIOR = {'sol': 0.80, 'lluvia': 0.20}


def normalize(d):
    z = sum(d.values())
    return {k: v / z for k, v in d.items()}


def forward_filter(evidence):
    """Filtrado recursivo, con la emisión ANTES de la transición.

    El orden importa y es la fuente del bug de la primera versión:
      paso t: primero se emite la evidencia del estado, después se transiciona.
    Así, para la evidencia e1..eT, el estado del día t explica la emisión t
    como MÁXIMO hasta e_{t-1}, porque la emisión t ocurre después de la
    transición. La variante "transición primero" contesta otra pregunta.
    """
    dist = dict(PRIOR)
    history = []
    for t, e in enumerate(evidence):
        # 1) P(S_t | e_1..e_t) ∝ P(e_t | S_t) * P(S_t)
        post = normalize({s: EMIT[s][e] * dist[s] for s in STATES})
        # 2) pasar al día siguiente: P(S_{t+1}) = Σ P(S_{t+1}|S_t) P(S_t)
        dist = {cur: sum(post[prev] * TRANS[prev][cur] for prev in STATES)
                for cur in STATES}
        history.append(post)
    return history


def brute_force_filter(evidence, t):
    """Enumerar todas las historias de t estados y las t emisiones. Es el oráculo."""
    total = {s: 0.0 for s in STATES}
    for hist in itertools.product(STATES, repeat=t):
        p = PRIOR[hist[0]]
        for i in range(1, t):
            p *= TRANS[hist[i - 1]][hist[i]]
        for i in range(t):
            p *= EMIT[hist[i]][evidence[i]]
        total[hist[-1]] += p
    return normalize(total)


def main():
    evidence = ['paraguas', 'paraguas', 'paraguas']
    print('Estados: sol / lluvia     Emisiones: paraguas / sin')
    print('Transición:   sol -> sol 0.90, lluvia 0.10')
    print('              lluvia -> sol 0.30, lluvia 0.70')
    print('Emisión:      sol -> paraguas 0.10   lluvia -> paraguas 0.90')
    print()
    print(f'Evidencia: {" ".join(evidence)}')
    print()

    history = forward_filter(evidence)

    print('=== Filtrado paso a paso ===')
    print(f'  prior       P(sol)={PRIOR["sol"]:.4f}  P(lluvia)={PRIOR["lluvia"]:.4f}')
    print()
    print(f'  {"t":<4} {"evidencia":<12} {"P(sol)":<10} {"P(lluvia)"}')
    print('-' * 44)
    for t, (e, d) in enumerate(zip(evidence, history), start=1):
        print(f'  {t:<4} {e:<12} {d["sol"]:<10.4f} {d["lluvia"]:.4f}')
    print()

    print('=== Lo que muestran los números ===')
    for t, d in enumerate(history, start=1):
        print(f'  Día {t}: P(lluvia) = {d["lluvia"]:.4f}')
    print()
    print('  La evidencia se ACUMULA sin guardar la historia: el filtrado lleva')
    print('  sólo la distribución del día anterior. Eso es la suposición de Markov')
    print('  haciendo su trabajo.')
    print()

    print('=== Verificación contra fuerza bruta ===')
    print(f'  {"t":<4} {"filtrado":<12} {"fuerza bruta":<14} {"coincide"}')
    print('-' * 48)
    ok = True
    for t in (1, 2, 3):
        bf = brute_force_filter(evidence, t)
        fw = history[t - 1]
        same = abs(fw['lluvia'] - bf['lluvia']) < 1e-12
        ok = ok and same
        print(f'  {t:<4} {fw["lluvia"]:<12.4f} {bf["lluvia"]:<14.4f} {"sí" if same else "NO"}')
    print()

    print('=== El límite de la suposición ===')
    print('  El filtrado asume que sólo importa el estado anterior. Si el clima')
    print('  tuviera memoria de tres días (por ejemplo, un patrón que se repite),')
    print('  la cadena de Markov de un paso daría probabilidades incorrectas y la')
    print('  recursión no tendría forma de darse cuenta: sigue sumando 1 y se ve')
    print('  perfectamente sana desde adentro.')
    print('  Es el mismo problema de la heurística no admisible del Módulo 1:')
    print('  una suposición falsa no rompe el cálculo, rompe la garantía.')

    print()
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
