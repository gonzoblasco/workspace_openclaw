# Monad — Evaluación

## Viabilidad técnica

### SwiftUI + SwiftData
- **Riesgo:** Bajo. Gonzo no tiene experiencia en SwiftUI pero tiene 9+ años de React. La transferencia es directa: componentes, estado, navegación.
- **Mitigación:** Arrancar con tutoriales dirigidos + pair programming conmigo.

### CoreML + Gemma 4 2B
- **Riesgo:** Medio. Gemma 4 2B en dispositivo requiere optimización (cuantización, tamaño de modelo). iPhone 14 Pro tiene Neural Engine pero no es 15 Pro.
- **Mitigación:** Probar con modelo cuantizado (Q4). Si no corre fluido, usar modelo más chico (Gemma 4 0.5B o similar) o diferir IA a Edge Function.

### Supabase sync
- **Riesgo:** Bajo. Stack conocido. Sync offline-first con SwiftData + Supabase es un patrón documentado.

### Sincronización con workspace git
- **Riesgo:** Medio. Requiere diseño cuidadoso para no corromper archivos. Las daily notes y fotos son el caso de uso principal.
- **Mitigación:** Arrancar con sync unidireccional (app → workspace). Bidireccional después.

## Competencia / Alternativas

| App | Qué hace | Diferencia con Monad |
|---|---|---|
| Notion | Notas + proyectos | No es mobile-first, no tiene IA local, no trackea salud |
| Day One | Diario personal | Solo diario, sin proyectos ni IA |
| Bear | Notas | Solo notas, sin métricas |
| Streaks | Hábitos | Solo hábitos, sin integración con código |
| GitHub mobile | Proyectos | Solo código, sin vida personal |

**Ninguna app existente unifica proyectos + vida + escritura + fotos + IA local en un solo lugar.** Monad no compite con ninguna, las integra.

## Fit estratégico

- ✅ Usa stack conocido (Supabase, Edge Functions, TS)
- ✅ Fuerza a aprender SwiftUI (skill valiosa)
- ✅ Producto que Gonzo usaría todos los días
- ✅ Privacidad real (IA local, datos en dispositivo)
- ✅ Portfolio vivo: muestra SwiftUI + CoreML + arquitectura offline-first
- ⚠️ Tiempo de desarrollo: estimado 3-4 meses para MVP completo

## Riesgos clave

1. **CoreML + Gemma 4 en iPhone 14 Pro** — puede no correr. Plan B: Edge Function con modelo remoto o modelo más chico.
2. **SwiftUI learning curve** — real pero superable. React dev → SwiftUI es de las transiciones más suaves.
3. **Scope creep** — riesgo alto. Es tentador agregar módulos. MVP estricto es crítico.
4. **Abandono** — riesgo real. Muchos proyectos personales mueren. La clave: que Gonzo lo use a diario desde el día 1.

## Veredicto

**GO.** Viabilidad alta, riesgo manejable, fit estratégico perfecto. El mayor riesgo no es técnico sino de scope y constancia.
