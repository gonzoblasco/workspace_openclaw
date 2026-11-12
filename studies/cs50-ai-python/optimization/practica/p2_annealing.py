#!/usr/bin/env python3
"""Práctica 2 — simulated annealing: aceptar lo peor a propósito.

Hill climbing se traba en un máximo local porque nunca acepta un movimiento que
empeore. Simulated annealing lo hace, con una probabilidad que baja con el tiempo.

    P(aceptar un empeoramiento Δ) = exp(-Δ / T)

- T grande: acepta casi todo. Explora.
- T chica: acepta casi nada. Se parece a hill climbing.
- T → 0: se congela.

El algoritmo:
  T = T0
  mientras T > Tmin:
      vecino al azar
      si mejora: aceptar
      si empeora: aceptar con prob exp(-Δ/T)
      T = T * cooling

La práctica mide, sobre el MISMO paisaje de p1, cuántas corridas llega al global
con annealing contra hill climbing con reinicios, y muestra el trazado de
temperatura y de valor para ver por qué funciona.
"""
import math
import random
import sys

sys.path.insert(0, '.')
from p1_hill_climbing import hill_climbing, landscape


def simulated_annealing(start, t0=1.0, t_min=1e-4, cooling=0.995,
                        step=0.25, seed=0, trace=False):
    rng = random.Random(seed)
    x = start
    value = landscape(x)
    t = t0
    history = [(t, value)] if trace else None
    while t > t_min:
        delta_x = rng.uniform(-1, 1) * step
        nx = x + delta_x
        nv = landscape(nx)
        delta = nv - value
        if delta >= 0:
            x, value = nx, nv
        else:
            if rng.random() < math.exp(delta / t):
                x, value = nx, nv
        t *= cooling
        if trace:
            history.append((t, value))
    return x, value, history


def main():
    xs = [i * 0.05 - 12 for i in range(int(24 / 0.05))]
    global_v = max(landscape(x) for x in xs)
    global_x = max(xs, key=landscape)
    print(f'Mismo paisaje que p1. Global = {global_v:.4f} en x = {global_x:.2f}')
    print()

    # --- la probabilidad de aceptar lo peor -------------------------------
    print('=== P(aceptar un empeoramiento) = exp(-Δ/T) ===')
    print(f'  {"Δ (empeora)":<14} {"T=1.0":<10} {"T=0.5":<10} {"T=0.1":<10} {"T=0.01"}')
    print('-' * 56)
    for delta in (0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0):
        row = [math.exp(-delta / t) for t in (1.0, 0.5, 0.1, 0.01)]
        print(f'  {delta:<14.2f} ' + ' '.join(f'{p:<10.4f}' for p in row))
    print()
    print('  Con temperatura alta acepta casi todo; con temperatura baja, casi nada.')
    print('  El "casi nada" del final es lo que garantiza que termine en un pico')
    print('  y no vagando.')
    print()

    # --- annealing contra restarts, mismo presupuesto de corridas ---------
    rng = random.Random(11)
    trials = 200
    print('=== ¿Llega al global? 200 corridas desde puntos al azar ===')
    print(f'  {"método":<38} {"llega al global":<18} {"mejor valor medio"}')
    print('-' * 80)

    best_vals = []
    hits = 0
    for _ in range(trials):
        x0 = rng.uniform(-12, 12)
        _, v, _ = simulated_annealing(x0, seed=rng.randrange(10**6))
        best_vals.append(v)
        if v >= global_v - 1e-3:
            hits += 1
    print(f'  {"simulated annealing (1 corrida)":<38} {f"{hits / trials:.0%}":<18} '
          f'{sum(best_vals) / len(best_vals):.4f}')

    hill_vals = []
    hits_hc = 0
    for _ in range(trials):
        x0 = rng.uniform(-12, 12)
        _, v, _ = hill_climbing(x0)
        hill_vals.append(v)
        if v >= global_v - 1e-3:
            hits_hc += 1
    print(f'  {"hill climbing (1 corrida)":<38} {f"{hits_hc / trials:.0%}":<18} '
          f'{sum(hill_vals) / len(hill_vals):.4f}')
    print()

    # --- el trazado: por qué funciona -------------------------------------
    print('=== El trazado de una corrida de annealing ===')
    x0 = -1.0
    xf, vf, hist = simulated_annealing(x0, trace=True, seed=42)
    n = len(hist)
    print(f'  {"iteración":<12} {"T":<12} {"valor actual"}')
    for i in (0, n // 8, n // 4, n // 2, 3 * n // 4, n - 1):
        t, v = hist[i]
        print(f'  {i:<12} {t:<12.6f} {v:.4f}')
    print(f'  terminó en x={xf:.2f} con valor {vf:.4f} '
          f'({"global" if vf >= global_v - 1e-3 else "local"})')
    print()
    print('  En el comienzo, T alta: el valor BAJA varias veces, porque acepta')
    print('  empeorar. Ese es el trabajo que hill climbing no hace: salir del pozo')
    print('  antes de que se vuelva trampa. Al final, T baja y el valor se estanca')
    print('  en un pico.')

    print()
    print('=== La honestidad del método ===')
    print('  Simulated annealing NO garantiza el global. Es un método probabilístico:')
    print('  con mal parámetro (T0 demasiado baja) se comporta como hill climbing;')
    print('  con T0 demasiado alta y enfriamiento lento, termina igual pero tarda más.')
    print('  Lo que garantiza (annealing teórico, enfriamiento logarítmico) asume')
    print('  infinito tiempo. En la práctica se elige el presupuesto y se reza.')

    anneal_mean = sum(best_vals) / len(best_vals)
    hill_mean = sum(hill_vals) / len(hill_vals)
    print()
    ok = anneal_mean >= hill_mean and hits > hits_hc
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
