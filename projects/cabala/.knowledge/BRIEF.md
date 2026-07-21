# BRIEF — Cábala

## En una frase

App mobile de bitácora visual: 3 fotos por día, organizadas por ubicación y tiempo, con notas de voz, tags, y un modo "cábala" para replicar fotos del pasado.

## Problema

Las apps de fotos/diario existentes son pesadas, requieren suscripción, nube, o están diseñadas para contenido curado. No existe una app simple, offline-first, que te invite a capturar tu día en 3 fotos sin presión.

## Usuario target

Gonzo (y gente como él): alguien que quiere llevar un registro visual de su vida cotidiana sin la fricción de las apps tradicionales. Fotógrafos casuales, viajeros, gente que quiere "acordarse de cómo era su vida" sin tener que curar un feed.

## Diferenciación

- **3 fotos por día** — límite deliberado, no es galería infinita
- **Offline-first** — SQLite, sin cuenta, sin nube
- **Compresión automática** — calidad justa para pantalla de celular
- **Modo Cábala** — "hace un mes sacaste esta foto acá, ¿querés replicarla?"
- **Notas de voz** — además de texto
- **Mapa + calendario + tags** — organización sin esfuerzo

## Stack propuesto

- React Native / Expo
- SQLite (expo-sqlite o similar)
- Local notificaciones
- Cámara nativa
- Geolocalización
- Sin backend (MVP)

## Estado

En definición. Próximo paso: EVALUATION.md
