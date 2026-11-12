# Lab M1 — el loop, por dentro

Tres piezas que se pueden correr en orden. Nada acá es del curso: es la prueba de la tesis del módulo 1 (que el agente es el harness, no el modelo).

## 1. `agente-minimo.sh` — el loop sin modelo
Corre un comando, lee el exit code, repite 3 veces. Muestra que **tener el loop no alcanza**: el agente mínimo no sabe qué hacer con la señal.

```bash
./agente-minimo.sh "arregla el test" "node fixture/test-inicial.mjs"
```

Bug encontrado al escribirlo: `OUT=$("$CMD")` parte el comando por espacios y devuelve **exit 127**. Un loop que corre pero no ejecuta lo que cree ejecutar. Fix: `eval "$CMD"`.

## 2. `loop-con-modelo.py` — el loop con modelo, sin tool de escritura
El modelo decide ("arreglar" / "esperar") pero **no puede escribir el archivo**. Resultado: 3 vueltas, 3 veces "arreglar", cero cambios. *Decidir que hay que arreglar no es arreglar.*

Segundo bug: la señal que le llegaba era `splitlines()[-1]` = `Node.js v26.13.0`, el cierre del stack, no el `AssertionError`. El modelo decidía sobre basura.

## 3. `loop-completo.py` — las tres tools
Lee, ejecuta, escribe. Es el mínimo para que un agente sea agente.

### Lo que demostró, en el orden en que pasó

1. **Primera corrida:** el modelo aplicó IVA correctamente en `caja.mjs` y el test **siguió rojo**. El test tenía su propia copia duplicada de la lógica: arreglar el archivo no cambiaba nada. → *El harness le dio un archivo cuando necesitaba el repo.*
2. **Test reescrito** para ejecutar `caja.mjs` real. Loop roto por otra razón: el modelo cambió `console.log("total:", total)` por `console.log(total)` y el parseo falló.
3. **Test tolerante + 1 vuelta más:** el loop cerró con `1512.5`.

### Hallazgo de proveedor
`gpt-oss:120b-cloud` devolvió **HTTP 429 Too Many Requests** a mitad de la corrida y hubo que cambiar a `deepseek-v4.1-flash:cloud`. Un loop de agente depende de la cuota del proveedor: el 429 no es una excepción, es parte del diseño (backoff, fallback de modelo, o reintento). El harness lo tiene que manejar; el modelo no puede.

## Los tres archivos del estado final

- `fixture/test-inicial.mjs` — el test que ejecuta el código real (versión tolerante)
- `fixture/caja-resuelta.mjs` — lo que escribió el agente: `IVA = 21`, `total += PRECIO * cantidad * (1 + IVA/100)`
- Verificación: `node fixture/test-inicial.mjs` → exit 0

## Lo que hay que llevarse

| Concepto | Evidencia de este lab |
|---|---|
| Agente = harness + modelo | Mismo modelo, dos loops, dos resultados |
| Loop sin tool de escribir es teatro | `loop-con-modelo.py`: 3 decisiones, 0 cambios |
| Señal de mala calidad = decisión de mala calidad | `splitlines()[-1]` le dio al modelo una línea vacía |
| Contexto insuficiente ≠ modelo tonto | Arregló el archivo correcto; el test estaba duplicado |
| El proveedor es parte del sistema | 429 de Ollama a mitad de loop |

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
