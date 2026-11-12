# Práctica — Módulo 1

Cada ejercicio es un script que corre de verdad. No hay respuestas "a ojo".

```
practica/m1/
├── ejercicio-8.1.py            tabla de crecimiento + corrector
├── respuestas-8.1.txt          respuesta de ejemplo (corregida OK)
├── java/
│   ├── Busqueda.java           8.3 — lineal vs binaria, con JIT y sin JIT
│   ├── Bloques.java            8.2 — los cinco bloques, medidos
│   └── Duplicado.java          8.4 — la pregunta de entrevista, tres soluciones
└── RESULTADOS.md               qué se midió y qué significa
```

## Java

El sistema no traía JDK. Se instaló con Homebrew (`brew install openjdk`, 27.0.1).
El `java` de macOS es solo un stub, así que hay que exportar el JAVA_HOME:

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk
export PATH="$JAVA_HOME/bin:$PATH"
```

## Cómo correr cada uno

```bash
# 8.1 — tabla y corrección
python3 ejercicio-8.1.py
python3 ejercicio-8.1.py --check respuestas-8.1.txt

# 8.2 — los cinco bloques (tarda ~1 s)
cd java && javac Bloques.java && java Bloques

# 8.3 — lineal vs binaria (2 s), y con intérprete para ver la forma
cd java && javac Busqueda.java && java Busqueda
cd java && java -Xint Busqueda

# 8.4 — la pregunta de entrevista (~20 s: la fuerza bruta a 200k tarda 3 s)
cd java && javac Duplicado.java && java Duplicado
```

Los `.class` se borran después de correr; no se commitean.

## Lo que importa

Leer `RESULTADOS.md` **después** de correr, no antes. Los números que más enseñan
son los que contradicen la teoría ingenua: la lineal que parece O(1) por el JIT,
el `sort` que le gana al hashset, y Fibonacci que crece 1,6× y no 2×.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
