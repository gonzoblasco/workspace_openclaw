#!/usr/bin/env python3
"""Práctica 2 — regresión lineal por descenso de gradiente: el ajuste que falla.

Ajustar una recta a datos es un problema de optimización (Módulo 4): minimizar
el error cuadrático. El descenso de gradiente lo hace iterativamente:

    w ← w - α · ∂L/∂w

donde α es la tasa de aprendizaje.

La práctica mide las tres cosas que dependen de α, y las tres se ven:

  1. α chica      → converge, lento.
  2. α razonable  → converge, rápido.
  3. α grande     → diverge (el error CRECE con las iteraciones).

Y después mide algo que no es de la tasa: cuánto se ajusta la recta a un
conjunto y cuánto a otro que no vio. Eso es la antesala del overfitting.
"""
import random
import sys


def make_data(n=60, noise=2.0, seed=2):
    rng = random.Random(seed)
    pts = []
    for _ in range(n):
        x = rng.uniform(0, 10)
        y = 2.0 * x + 3.0 + rng.gauss(0, noise)
        pts.append((x, y))
    return pts


def loss(pts, w, b):
    return sum((w * x + b - y) ** 2 for x, y in pts) / len(pts)


def gradient(pts, w, b):
    n = len(pts)
    dw = sum(2 * (w * x + b - y) * x for x, y in pts) / n
    db = sum(2 * (w * x + b - y) for x, y in pts) / n
    return dw, db


def gradient_descent(pts, alpha=0.01, iters=200, w=0.0, b=0.0):
    history = [loss(pts, w, b)]
    for _ in range(iters):
        dw, db = gradient(pts, w, b)
        w -= alpha * dw
        b -= alpha * db
        history.append(loss(pts, w, b))
        if not (abs(w) < 1e12 and abs(b) < 1e12):
            return w, b, history, 'divergió'
    return w, b, history, 'convergió'


def main():
    # Datos normalizados a [-1, 1]: con x en 0..10 el gradiente explota para
    # cualquier α razonable, porque x^2 llega a 100. Normalizar es parte del
    # algoritmo, no un detalle de los datos.
    raw = make_data()
    pts = [((x - 5) / 5.0, (y - 13) / 10.0) for x, y in raw]
    print(f'Datos normalizados: y ≈ 2x + 3 + ruido, mapeados a [-1, 1]  ({len(pts)} puntos)')
    print()

    print('=== El efecto de la tasa de aprendizaje ===')
    print(f'  {"α":<10} {"loss inicial":<16} {"loss final":<16} {"iteraciones al mínimo":<22} estado')
    print('-' * 92)
    rows = []
    for alpha in (0.001, 0.01, 0.05, 0.1, 0.5, 1.0):
        w, b, hist, state = gradient_descent(pts, alpha=alpha, iters=300)
        # iteraciones hasta quedar a 1% del final
        final = hist[-1]
        reached = next((i for i, l in enumerate(hist)
                         if abs(l - final) <= 0.01 * abs(final) + 1e-9), len(hist))
        rows.append((alpha, hist[0], final, reached, state, w, b))
        print(f'  {alpha:<10} {hist[0]:<16.3f} {final:<16.4f} {reached:<22} {state}')
    print()
    print('  La tasa no cambia la respuesta cuando converge: cambia si llegás.')
    print('  Y hay un techo duro: con α=1.0 el error no converge, oscila y queda')
    print('  altísimo. Sin normalizar los datos ese techo llegaba a α ≈ 0.02, y')
    print('  parecía que "el descenso de gradiente no funciona". Normalizar no es')
    print('  cosmético: es parte del algoritmo.')
    print()

    # el mejor
    best = min((r for r in rows if r[4] == 'convergió' and r[2] < 1.0),
               key=lambda r: r[3])
    print(f'  Mejor α acá: {best[0]}  →  w={best[5]:.3f}  b={best[6]:.3f}')
    print(f'  (en unidades normalizadas; el óptimo se compara en loss, no contra la')
    print(f'   recta verdadera, que está en las coordenadas originales)')
    print()

    # --- la divergencia, mostrada ----------------------------------------
    print('=== α demasiado grande: el error CRECE ===')
    for alpha_big in (1.0, 2.0, 3.0):
        w, b, hist, state = gradient_descent(pts, alpha=alpha_big, iters=30)
        print(f'  α={alpha_big}: loss inicial {hist[0]:.3f} → final {hist[-1]:.3e} '
              f'({state})')
    print()
    print('  Con α grande el error no baja: rebota. El descenso de gradiente se mueve')
    print('  en la dirección del gradiente, y si el paso es demasiado largo se pasa')
    print('  del mínimo y sube por el otro lado. No hay garantía de bajar.')
    print()

    # --- sobreajuste: pocos datos, y lo que pasa en un set que no vio -----
    print('\n=== Overfitting: 8 puntos, polinomio de grado alto ===')
    few = make_data(n=8, noise=0.4, seed=9)
    test = make_data(n=40, noise=0.4, seed=10)

    def poly_fit(pts, degree):
        """Ajuste por mínimos cuadrados con eliminación gaussiana."""
        n = degree + 1
        A = [[sum(x ** (i + j) for x, _ in pts) for j in range(n)] for i in range(n)]
        rhs = [sum(y * x ** i for x, y in pts) for i in range(n)]
        # gauss
        for i in range(n):
            piv = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[piv] = A[piv], A[i]
            rhs[i], rhs[piv] = rhs[piv], rhs[i]
            if abs(A[i][i]) < 1e-12:
                return None
            for r in range(i + 1, n):
                f = A[r][i] / A[i][i]
                for c in range(i, n):
                    A[r][c] -= f * A[i][c]
                rhs[r] -= f * rhs[i]
        coef = [0.0] * n
        for i in range(n - 1, -1, -1):
            coef[i] = (rhs[i] - sum(A[i][c] * coef[c] for c in range(i + 1, n))) / A[i][i]
        return coef

    def poly_eval(coef, x):
        return sum(c * x ** i for i, c in enumerate(coef))

    print(f'  {"grado":<8} {"error en train":<18} {"error en test":<18} veredicto')
    print('-' * 64)
    of_rows = []
    for degree in (1, 2, 3, 7):
        coef = poly_fit(few, degree)
        if coef is None:
            print(f'  {degree:<8} singular')
            continue
        tr = sum((poly_eval(coef, x) - y) ** 2 for x, y in few) / len(few)
        te = sum((poly_eval(coef, x) - y) ** 2 for x, y in test) / len(test)
        verdict = ''
        # El veredicto NO puede ser "test > 10x train": eso es la métrica que el
        # propio overfit manipula. El criterio es relativo al modelo sano: si el
        # test empeora respecto del modelo simple, hay overfitting.
        if of_rows and te > of_rows[0][2] * 2:
            verdict = 'OVERFIT (peor que el modelo simple en test)'
        of_rows.append((degree, tr, te, verdict))
        print(f'  {degree:<8} {tr:<18.2f} {te:<18.2f} {verdict}')
    print()
    print('  El polinomio de grado 7 ajusta los 8 puntos casi perfecto y explota en')
    print('  test. El de grado 1 tiene más error en train y MENOS en test.')
    print('  **Un modelo mejor en los datos que vio puede ser peor en los que no vio.**')
    print('  Es la definición de overfitting, y la razón por la que existe el held-out.')

    print()
    deg7 = next((r for r in of_rows if r[0] == 7), None)
    ok = deg7 is not None and deg7[2] > deg7[1] * 3
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
