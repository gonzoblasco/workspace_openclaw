---
name: "anti-ai"
description: "Elimina modismos y estructuras que delatan texto de IA para que suene humano. Incluye la regla del guion comun. Usar antes de publicar posts, feedback o PRs."
metadata:
  category: "Content"
  tags:
    - escritura
    - humanizar
    - anti-ai
    - edicion
    - publicacion
user-invocable: true
---

# Workflow: Anti-AI

## Proposito

Eliminar el "olor a IA" de cualquier texto antes de que salga hacia afuera. No es reescribir el contenido: es quitar las marcas de fabrica que delatan que lo escribio un modelo, para que suene a persona real.

## Filosofia

> La IA no se nota por lo que dice, sino por como lo dice.

Un humano no escribe con transiciones perfectas, triadas forzadas ni cierres genericos. Este skill detecta esos patrones y los reemplaza por lenguaje natural.

## Regla base obligatoria: guion comun

**NUNCA usar guion largo (em dash U+2014) ni en dash (U+2013).** Siempre guion comun (-). Es la regla dura de Gonzo y el delator de IA mas clasico.

Mecanismo obligatorio: escanear el texto con `scripts/check_em_dash.py` antes de dar por terminada la edicion.

## Cuando usarlo

- Antes de publicar un post de LinkedIn (paso obligatorio del flujo, ver abajo)
- Antes de mandar feedback o comentarios en PRs/issues ajenos
- Antes de publicar cualquier texto hacia afuera (docs, issues, PRs, comments)
- Al revisar texto que suena "demasiado perfecto" o generico

## Categorias de deteccion

### 1. Muletillas de transicion
"Sin embargo", "es importante destacar", "cabe mencionar", "vale la pena senalar", "en conclusion", "por otro lado", "ademas" repetido.

**Fix:** eliminar o reemplazar por conexion natural. Un humano no anuncia cada giro.

### 2. Estructuras predecibles
- Aperturas tipo "En el mundo actual...", "En la era de...", "Hoy en dia..."
- Triadas forzadas (tres adjetivos o tres items perfectamente paralelos)
- Listados donde cada item tiene exactamente la misma longitud y ritmo

**Fix:** romper el paralelismo. Variar longitud de oraciones. Empezar directo, sin preambulo.

### 3. Adverbios y relleno
"Efectivamente", "ciertamente", "indudablemente", "de hecho" repetido, "realmente" sin aportar.

**Fix:** borrar. Si la oracion funciona sin el adverbio, el adverbio sobra.

### 4. Falsas precisiones
"Aproximadamente", "alrededor de", "casi" cuando no aportan dato real.

**Fix:** o dar el numero exacto o quitarlo. La falsa precision es marca de IA.

### 5. Cierre generico
"En resumen", "para concluir", "espero que esto ayude", "no dudes en contactarme".

**Fix:** terminar con la idea, no con el resumen. Un cierre humano corta cuando termina.

### 6. Guiones largos (U+2014 / U+2013)
Caso base. Escanear con `scripts/check_em_dash.py`.

**Fix:** reemplazar por guion comun (-) o reestructurar la oracion.

## Flujo de trabajo

1. **Escaneo mecanico:** correr `scripts/check_em_dash.py` sobre el texto (guiones largos).
2. **Pasada de patrones:** revisar cada categoria (1-5) y marcar instancias.
3. **Reescritura natural:** reemplazar cada instancia por lenguaje humano, preservando el mensaje.
4. **Verificacion:** releer en voz alta. Si suena a ensayo, sigue oliendo a IA.
5. **Regla de oro:** si no estas seguro si una frase es marca de IA, preguntate "lo diria un humano en una conversacion?" Si la respuesta es no, cambiala.

## Integracion con el flujo de posts de LinkedIn

**Paso obligatorio:** todo post de LinkedIn (guardado en `docs/linkedin/linkedin-*.md`) debe pasar por anti-ai antes de publicarse. El post se escribe, se pasa por anti-ai, y recien entonces se publica. Esto aplica a los posts de a11y y agentic del patron de branding.

## Outputs

- Texto editado sin marcas de IA
- Lista de instancias removidas (opcional, para aprendizaje)
- Confirmacion de que paso el escaneo de guiones largos

## Principios

- No cambiar el mensaje core; solo quitar el olor a IA
- Preservar la voz del autor
- Menos es mas: si dudas, corta
- La regla del guion comun es innegociable

## Related Skills

- [Copy Editing](../copy-editing): Para mejorar conversion de copy de marketing (complementario, se puede encadenar)
- [Skill Router](../skill-router): Para sugerir este skill cuando el contexto sea publicar texto hacia afuera
