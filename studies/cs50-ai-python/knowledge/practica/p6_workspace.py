#!/usr/bin/env python3
"""Práctica 6 — la KB del propio workspace: qué se DERIVA de AGENTS.md.

Hasta acá la lógica se aplicó a Harry, a Hogwarts y a Clue. Esta práctica la
aplica a las reglas que nos gobiernan: cada regla dura de AGENTS.md es un
axioma, y la pregunta del módulo es qué otras cosas se siguen de ellas — cosas
que nadie escribió, pero que son obligatorias si las escritas son verdad.

Es la práctica que importa para lo que viene: cuando escribamos gates y skills,
un gate es una regla de inferencia, y la diferencia entre `KB ⊨ α` y `KB ⊬ α`
es la diferencia entre un check que prueba algo y uno que sólo lo sugiere.

La conclusión interesante no es la que se deriva: es la que NO se deriva.
"""
import sys

sys.path.insert(0, '.')
from p2_model_checking import AND, IMP, NOT, OR, entails, sym


def S(n):
    return sym(n)


def main():
    # Axiomas: reglas duras reales de AGENTS.md, en forma de implicación.
    PUSH_SIN_OK = S('push_sin_ok')
    OPERACION_EXTERNA = S('operacion_externa')
    GIT_ADD_A = S('git_add_A')
    MULTI_SESION = S('multi_sesion')
    COMMIT_FIRMA_AJENA = S('commit_firma_ajena')
    RESTART_GATEWAY = S('restart_gateway')
    INFRA = S('infra')

    KB = [
        IMP(OPERACION_EXTERNA, PUSH_SIN_OK),          # toda operación externa es push sin OK
        IMP(AND(GIT_ADD_A, MULTI_SESION), COMMIT_FIRMA_AJENA),
        IMP(INFRA, RESTART_GATEWAY),                   # infra -> puede requerir restart
    ]

    casos = [
        ('git add -A con otra sesión viva implica commit que firma trabajo ajeno',
         AND(GIT_ADD_A, MULTI_SESION), COMMIT_FIRMA_AJENA, True),
        ('git add -A solo (sin otra sesión) implica commit que firma trabajo ajeno',
         GIT_ADD_A, COMMIT_FIRMA_AJENA, False),
        ('una operación externa implica push sin OK',
         OPERACION_EXTERNA, PUSH_SIN_OK, True),
        ('un push sin OK implica que hubo operación externa',
         PUSH_SIN_OK, OPERACION_EXTERNA, False),
        ('infra implica restart de gateway',
         INFRA, RESTART_GATEWAY, True),
        ('un restart de gateway implica que había infra',
         RESTART_GATEWAY, INFRA, False),
    ]

    print('KB (axiomas de AGENTS.md, formalizados):')
    print('  A1  operacion_externa -> push_sin_ok')
    print('  A2  (git_add_A and multi_sesion) -> commit_firma_ajena')
    print('  A3  infra -> restart_gateway')
    print()
    print(f'{"afirmación":<66} {"deriva":<8} {"correcto"}')
    print('-' * 90)

    ok_all = True
    for nombre, hipotesis, tesis, esperado in casos:
        # La consistencia NO es una precondición del entailment: de una KB
        # inconsistente se sigue cualquier cosa (ex falso quodlibet), y eso es
        # justo lo que no queremos. Lo que importa es el entailment liso:
        # KB ∪ {hipótesis} ⊨ tesis.
        deriva, _, _ = entails(KB + [hipotesis], tesis)
        correcto = deriva == esperado
        ok_all = ok_all and correcto
        print(f'{nombre:<66} {"sí" if deriva else "no":<8} {"OK" if correcto else "FALLA"}')

    print()
    print('  (nota: ex falso quodlibet — de una KB contradictoria TODO se sigue,')
    print('   por eso la consistencia no se usa como filtro: se mira el entailment.)')
    print()
    print('=== Lo que hace útil esta práctica ===')
    print()
    print('  Las tres afirmaciones de la columna "deriva" salen de combinar axiomas,')
    print('  no de leerlos. Pero la mitad de la tabla es "no deriva": el error que')
    print('  más se comete con lógica de primer grado es leer una implicación al revés.')
    print()
    print('  "operacion_externa -> push_sin_ok" NO dice que todo push sin OK sea una')
    print('  operación externa. Afirmar el consecuente es exactamente la regla')
    print('  inválida de la práctica 3. Si un gate verificara "hay push sin OK,')
    print('  entonces hubo operación externa", daría por buena una causa que la')
    print('  regla no sostiene.')
    print()
    print('  A2 sí tiene la forma que se usa para gatear: la conjunción es necesaria.')
    print('  "git add -A" solo no implica nada: la regla sólo aplica con otra sesión')
    print('  viva. Un check que se dispare con una sola de las dos condiciones está')
    print('  afirmando una regla que no existe.')

    print()
    print('RESULTADO: PASA' if ok_all else 'RESULTADO: FALLA')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
