# ADR-003: Matching por distancia coseno en Big Five

*Ejemplo real del proyecto quedamos. Muestra una decisión técnica con algoritmo detallado.*

## Estado
Aceptado

## Contexto
Necesitamos un algoritmo de matching que calcule compatibilidad entre usuarios. Opciones: distancia coseno en vectores Big Five, matching por reglas (misma actividad, misma edad, etc.), o ML supervisado.

## Decisión
Usamos distancia coseno entre vectores Big Five de 5 dimensiones como base, con ajustes por feedback histórico y actividades compartidas.

## Consecuencias

### Positivas
- Simple, interpretable, funciona desde el día 1 (sin datos históricos), fácil de ajustar.

### Negativas
- No captura matching complejo (química, humor, etc.), necesita feedback loop para refinar.

### Mitigaciones
- El feedback post-salida ajusta pesos de cada dimensión por usuario, mejorando con el tiempo.

## Detalle del algoritmo
1. Calcular distancia coseno entre vectores Big Five → score base 0-100%
2. Bonus por actividades compartidas: +5% por cada actividad en común (max +20%)
3. Ajuste por feedback histórico: si A y B interactuaron antes, el score se pondera con feedback previo
4. Score final = (score_base * 0.7) + (bonus_actividades * 0.15) + (feedback_historico * 0.15)

## Alternativas consideradas
1. **Matching por reglas (misma actividad, misma edad):** simple pero no captura compatibilidad de personalidad. Rechazado.
2. **ML supervisado con datos históricos:** más preciso a largo plazo pero no funciona desde el día 1. Rechazado para MVP.

## Referencias
DATA_MODEL.md, weekly-suggester edge function
