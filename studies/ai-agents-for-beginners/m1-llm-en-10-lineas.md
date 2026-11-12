# M1 - Práctica: explicar un LLM en 10 líneas

- **Curso:** AI Agents For Beginners – OpenClaw Case Study
- **Módulo:** 1 — Course Welcome & Architecture Fundamentals (00:00–07:54)
- **Fecha:** 2026-11-12
- **Consigna:** explicar qué es un LLM para alguien que nunca usó uno, y por qué puede inventar datos con seguridad. Sin jerga. Diez líneas.

## Versión modelo (10 líneas)

1. Un modelo de lenguaje, o LLM, es un programa que aprendió a continuar texto después de leer muchísimos ejemplos.
2. Le mostraron millones de frases y aprendió qué pedacito de texto suele venir después de cada pedacito.
3. No guarda una copia de esas frases: ajusta números internos que representan patrones.
4. Cuando le escribís, usa esos patrones para producir la continuación más probable, pedacito por pedacito.
5. No consulta una base de datos ni verifica si lo que dice es cierto.
6. Por eso puede responder con seguridad algo que suena bien pero es falso: elige la continuación plausible, no la verdadera.
7. Eso se llama alucinación, y no es un error raro: es el mismo mecanismo que lo hace útil.
8. Puede acertar mucho porque los patrones capturan regularidades del mundo y del lenguaje.
9. Pero cuando el dato falta, cambió o es ambiguo, rellena el hueco con lo que parece más probable.
10. Por eso, para usarlo en serio, hay que darle fuentes, herramientas de verificación o una persona que controle lo importante.

## Por qué esta explicación funciona

- **Empieza por el mecanismo, no por la marca.** No dice "es como ChatGPT"; dice qué hace el programa.
- **Distingue patrón de copia.** El modelo no tiene las frases guardadas; tiene números ajustados.
- **Distingue plausibilidad de verdad.** Esa es la clave de la alucinación.
- **No promete un "no sé".** El modelo no tiene un detector de ignorancia confiable; completa el hueco.
- **Cierra con la consecuencia práctica.** Si la verdad no está en el modelo, tiene que venir de afuera.

## Errores comunes al explicarlo

- Decir "el modelo busca en internet". No busca: genera. Si busca, es porque alguien le dio una tool de búsqueda.
- Decir "alucina porque está mal entrenado". No: alucina porque su objetivo es la continuación plausible, no la verdad.
- Decir "si tiene más parámetros, es más inteligente". Más parámetros no garantizan mejor calidad; importan datos, cómputo y post-entrenamiento.

## Tu versión (completar)

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## Criterios de corrección

- [ ] Se entiende sin saber qué es un token, un parámetro o un transformer.
- [ ] Explica el mecanismo (predecir la continuación), no solo el resultado ("inventa cosas").
- [ ] Distingue que suena plausible de que sea verdadero.
- [ ] Menciona que no consulta una base de datos ni verifica por su cuenta.
- [ ] Cierra con una consecuencia práctica: fuentes, tools o revisión humana.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
