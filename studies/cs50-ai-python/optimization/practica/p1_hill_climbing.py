#!/usr/bin/env python3
"""Práctica 1 — hill climbing: subir hasta que no se pueda más, y quedarse ahí.

La idea mínima de optimización: no importa cómo llegaste, importa qué tan buena
es la configuración actual. Se cambia un poquito, y si mejora, se adopta.

Hill climbing es exactamente eso.
  - elegir un vecino al azar
  - si mejora, moverte
  - si no mejora, quedarte (o probar otro)

**Y el problema:** el paisaje tiene máximos locales, mesetas y crestas. Hill
climbing no los distingue de un máximo global: sube, se planta, y desde adentro
no hay nada que diga "estoy trabado".

Esta práctica construye un paisaje con máximos locales conocidos, corre hill
climbing desde muchos puntos de partida, y mide con qué frecuencia queda atrapado.
"""
import random
import sys


def landscape(x):
    """Un paisaje 1D con UN global y tres locales bien separados.

    Tres gaussianas de altura y ancho distintos, más una cuarta colina baja.
    La separación es lo que importa: si los picos están cerca, hill climbing
    con paso chico los distingue por accidente y la práctica no enseña nada.
    """
    import math
    peaks = [(-8.0, 0.55, 2.2), (-1.0, 0.80, 1.6), (4.5, 1.30, 1.8), (9.5, 0.70, 2.5)]
    return sum(h * math.exp(-((x - c) ** 2) / (2 * w * w)) for c, h, w in peaks)


def neighbors(x, step=0.25):
    return [x - step, x + step]


def hill_climbing(start, step=0.25, max_iters=500):
    """Sube al primer vecino que mejore. Devuelve (x_final, valor, iteraciones)."""
    x = start
    value = landscape(x)
    for i in range(max_iters):
        improved = False
        for nx in neighbors(x, step):
            nv = landscape(nx)
            if nv > value + 1e-12:
                x, value = nx, nv
                improved = True
                break
        if not improved:
            return x, value, i
    return x, value, max_iters


def steepest_ascent(start, step=0.25, max_iters=500):
    """Sube al MEJOR vecino, no al primero que mejore."""
    x = start
    value = landscape(x)
    for i in range(max_iters):
        best_x, best_v = x, value
        for nx in neighbors(x, step):
            nv = landscape(nx)
            if nv > best_v + 1e-12:
                best_x, best_v = nx, nv
        if best_x == x:
            return x, value, i
        x, value = best_x, best_v
    return x, value, max_iters


def main():
    # explorar el paisaje para conocer los óptimos
    xs = [i * 0.05 - 12 for i in range(int(24 / 0.05))]
    vals = [(landscape(x), x) for x in xs]
    vals.sort(reverse=True)
    global_v, global_x = vals[0]
    print(f'Paisaje: máximo global = {global_v:.4f} en x = {global_x:.2f}')
    print()

    # identificar los máximos locales (puntos más altos que sus dos vecinos)
    local = []
    for i in range(1, len(xs) - 1):
        if landscape(xs[i]) > landscape(xs[i - 1]) and landscape(xs[i]) > landscape(xs[i + 1]):
            local.append((xs[i], landscape(xs[i])))
    print('Máximos locales encontrados:')
    for x, v in sorted(local, key=lambda t: -t[1]):
        tag = 'GLOBAL' if v >= global_v - 1e-3 else 'local'
        print(f'  x={x:>7.2f}  valor={v:.4f}  {tag}')
    print()

    print('=== Hill climbing desde 200 puntos de partida ===')
    rng = random.Random(3)
    results = {}
    for _ in range(200):
        x, v, it = hill_climbing(rng.uniform(-12, 12))
        key = round(x, 1)
        results[key] = results.get(key, 0) + 1

    atrapados = sum(n for k, n in results.items()
                    if landscape(k) < global_v - 1e-3)
    total = sum(results.values())
    print(f'  termina en el global: {total - atrapados}/{total} '
          f'({(total - atrapados) / total:.0%})')
    print(f'  ATASCADO en un máximo local: {atrapados}/{total} '
          f'({atrapados / total:.0%})')
    print()
    print('  Dónde termina y cuántas veces:')
    for x in sorted(results, key=lambda k: -results[k]):
        v = landscape(x)
        tag = 'global' if v >= global_v - 1e-3 else 'LOCAL'
        print(f'    x={x:>7.1f}  valor={v:.4f}  {results[x]:>3} veces  {tag}')

    print()
    print(f'=== {atrapados / total:.0%} de las corridas queda atrapada ===')
    print('  Y lo peor: hill climbing no puede saberlo. Desde adentro, un máximo')
    print('  local es indistinguible del global: no hay vecino que mejore en ninguno')
    print('  de los dos. Se detiene en ambos con el mismo criterio.')
    print()

    # --- random restart ---------------------------------------------------
    print('=== Random restart: la solución sin entender el paisaje ===')
    print('  Repetir desde muchos lugares al azar sube la probabilidad de tocar el global.')
    for k in (1, 3, 5, 10, 20):
        hits = 0
        trials = 200
        for _ in range(trials):
            best = max(hill_climbing(rng.uniform(-12, 12))[1] for _ in range(k))
            if best >= global_v - 1e-3:
                hits += 1
        print(f'  {k:>2} reinicios: {hits / trials:.0%} de las corridas llega al global')

    print()
    print('  No necesitás entender el paisaje para mejorar tus chances: necesitás')
    print('  más puntos de partida. Pero TAMPOCO garantiza llegar al global: reiniciar')
    print('  desde un punto al azar puede caer siempre en el mismo pozo. Sólo cambia')
    print('  la probabilidad, y eso es justo el punto de simulated annealing: escapar')
    print('  del pozo sin reiniciar.')

    print()
    ok = atrapados > 0 and atrapados < total
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA (el paisaje no tiene locales)')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
