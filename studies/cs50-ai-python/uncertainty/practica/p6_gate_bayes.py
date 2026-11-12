#!/usr/bin/env python3
"""Práctica 6 — la probabilidad condicional aplicada a un gate.

Todas las prácticas anteriores resolvieron redes de juguete. Esta aplica el
mismo aparato a la decisión que se toma cien veces por sesión: cuando un gate
da verde, ¿qué se sigue?

Un gate es un test con dos errores posibles:
  - falso negativo: el código está mal y el gate pasa  (el que duele)
  - falso positivo: el código está bien y el gate falla  (ruido)

El módulo 5 del curso insiste en una cosa que acá es central: la probabilidad
de "el código está bien dado que el gate pasó" NO es la sensibilidad del gate.
Es Bayes, y depende de la TASA BASE de cambios rotos.

  P(bien | pasa) = P(pasa | bien) · P(bien) / P(pasa)

Un gate perfectamente sensible sigue dando resultados malos si casi todos los
cambios están rotos, o al revés: un gate flojo da buenas noticias si casi nada
se rompe. Es el mismo error de base rate de P(R|W) en la práctica 1.
"""
import sys


def posterior_good(sensitivity, specificity, prior_good):
    """P(bien | pasa).

    sensitivity = P(pasa | bien)    (1 - falso negativo)
    specificity = P(falla | mal)    (1 - falso positivo)
    prior_good  = P(bien)           la tasa base de cambios correctos
    """
    prior_bad = 1 - prior_good
    p_pass = sensitivity * prior_good + (1 - specificity) * prior_bad
    return sensitivity * prior_good / p_pass


def posterior_bad_given_fail(sensitivity, specificity, prior_good):
    prior_bad = 1 - prior_good
    p_fail = (1 - sensitivity) * prior_good + specificity * prior_bad
    return specificity * prior_bad / p_fail


def main():
    print('=== El gate que "pasa siempre" ===')
    print('  Sensibilidad 0.90 (atrapa el 90% de los cambios rotos)')
    print('  Especificidad 0.95 (deja pasar el 95% de los cambios buenos)')
    print()
    print(f'  {"tasa base de cambios bien":<30} {"P(bien | pasa)":<16} {"P(mal | falla)"}')
    print('-' * 76)
    rows = []
    for prior in (0.99, 0.90, 0.70, 0.50, 0.20, 0.05, 0.01):
        pg = posterior_good(0.90, 0.95, prior)
        pb = posterior_bad_given_fail(0.90, 0.95, prior)
        rows.append((prior, pg, pb))
        print(f'  {prior:<30.2f} {pg:<16.4f} {pb:.4f}')

    print()
    print('  El gate es el MISMO en las siete filas. Lo que cambia es cuánto')
    print('  significa que haya pasado.')
    print()
    lo = rows[-1]
    hi = rows[0]
    print(f'  Con casi todo roto (prior 0.01): pasa el gate y aun así P(bien) = {lo[1]:.3f}.')
    print(f'    El gate no está probando nada: está diciendo lo que ya sabíamos.')
    print(f'  Con casi todo bien (prior 0.99): pasa y P(bien) = {hi[1]:.4f}.')
    print(f'    El mismo test vale como promesa.')
    print()

    print('=== El caso que importa: un gate nuevo, sin historial ===')
    print('  Un check recién escrito no tiene tasa base medida. Si lo corrés sobre')
    print('  un repo donde nunca falló, la tasa base es 1.0 y el posterior es 1.0')
    print('  POR CONSTRUCCIÓN. Ese 100% no es evidencia: es la definición de no')
    print('  haber corrido nunca el caso que lo rompe.')
    print()
    print('  Ese es el error que el Módulo 1 encontró en la reapertura y que el')
    print('  workspace ya documentó: una verificación que da verde sin haber')
    print('  verificado. Con probabilidad condicional se ve por qué: la tasa base')
    print('  del caso roto es 0, así que P(bien | pasa) no se movió.')
    print()

    print('=== Cuánto aporta cada corrida correcta ===')
    print('  Cuánto mueve un verde el log-odds de "está bien":')
    print(f'  {"tasa base bien":<18} {"verde aporta"}')
    print('-' * 40)
    import math
    for prior in (0.99, 0.90, 0.70, 0.50, 0.20, 0.05):
        pg = posterior_good(0.90, 0.95, prior)
        odds_before = prior / (1 - prior)
        odds_after = pg / (1 - pg)
        info = math.log(odds_after / odds_before)
        print(f'  {prior:<18.2f} {info:+.3f}')

    print()
    print('  El mismo +2.89 en todas las filas, y eso es correcto: la evidencia de')
    print('  un evento es independiente del prior. Lo que cambia es de dónde se')
    print('  parte. Con prior 0.05, +2.89 de log-odds deja P(bien)≈0.49: seguís')
    print('  sin poder afirmar que está bien. Con prior 0.99, sale de 4.6 a 7.5 y')
    print('  ya no había duda que mover.')
    print()
    print('  La lección operativa: un gate nuevo del que nunca se vio un rojo no')
    print('  mueve nada. Su verde no es información, es un prior sin corregir.')
    print()

    ok = abs(posterior_good(0.90, 0.95, 0.50) - 0.9474) < 0.001
    ok = ok and rows[-1][1] < 0.20
    print('RESULTADO: PASA' if ok else 'RESULTADO: FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
