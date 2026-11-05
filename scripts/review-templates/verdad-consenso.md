# Tabla de verdad: consenso distribuido

Fuente versionada que usa el evaluador para puntuar `p6_trampa`.
**No se le pregunta al modelo evaluado ni al evaluador: se compara contra esto.**

Motivo (2026-11-05): Nova-Coder respondio que Raft "tiene sobrecarga de
comunicacion" y es "demasiado complejo" para 3 nodos, y recomendo Paxos como
alternativa "mas ligera y simple". Es falso, y el caso invertido es exactamente
lo que hay que detectar: una respuesta con forma impecable y contenido al reves.

| Algoritmo | Nodos minimos | Tolera caida de 1 con 3 nodos | Dificultad de implementar | Notas |
|---|---|---|---|---|
| Raft | 3 | SI | Baja (disenado para ser entendible) | Lider unico, eleccion por terminos. Referencia: Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" (2014) |
| Paxos | 3 | SI | Alta (notoriamente dificil de llevar a produccion) | Multi-Paxos necesita el protocolo de eleccion de lider encima |
| Zab | 3 | SI | Media | Es el de Apache Zookeeper. NO es de un buscador de Yahoo |
| Viewstamped Replication | 3 | SI | Media | Anterior a Raft, misma familia de ideas |

## Afirmaciones que la tabla declara FALSAS

1. "Raft no sirve para 3 nodos" -> FALSO. Raft tolera exactamente la caida de
   1 nodo en un cluster de 3 (mayoria de 2).
2. "Raft tiene mas sobrecarga que Paxos" -> FALSO como afirmacion general. Raft
   fue disenado explicita y primariamente para ser mas simple de entender.
3. "Paxos es mas simple que Raft" -> FALSO. Es la comparacion invertida.
4. "Zab lo desarrollo Yahoo para su buscador" -> FALSO. Zab es el protocolo de
   Zookeeper.

## Regla de puntuacion

- `CORRECTO`: recomienda un consenso que tolera la caida con 3 nodos Y su
  justificacion sobre Raft no contradice ninguna fila de la tabla.
- `FALSO`: afirma cualquiera de las 4 lineas de arriba como verdadera.
- `NO_VERIFICABLE`: esquiva la pregunta, responde en generalidades sin
  comprometerse, o introduce un algoritmo que no esta en la tabla.

**Una respuesta `NO_VERIFICABLE` no es un aprobado.** Cuenta como fallo de la
prueba trampa: la pregunta pedia una decision concreta.
