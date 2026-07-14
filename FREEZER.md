# FREEZER.md — Ideas congeladas

> Productos y servicios que ideamos pero que no es momento de arrancar. Cada uno tiene su contexto, por qué surgió, y qué tendría que pasar para descongelarlo.

---

## Marketplace de servicios domésticos

**Estado:** Idea. Esqueleto creado (Next.js 15 + Drizzle + SQLite), sin funcionalidad real.
**Repo local:** `projects/mucamas-online/` (nombre provisional, hay que cambiarlo)

### Origen
Una amiga que trabaja en bienes raices le comentó a Gonzo que hay mucha demanda de servicios domésticos entre inquilinos y que muchas veces no saben dónde buscar. Esqueleto creado el 12/07, agregado al workspace el 13/07.

### La propuesta
Marketplace tipo clasificados donde prestadores publican servicios domésticos (limpieza, cuidado, cocina, plomería, electricidad, etc.) y contratantes los buscan por zona/categoría/precio.

### Modelo de monetización
Estilo Mercado Libre: publicar es gratis, pero pagar para estar bien posicionado en los resultados (boost/destacado). Suscripción para prestadores que quieren prioridad. Reviews de la comunidad como motor de confianza (tipo Airbnb).

### Cómo encajaría en Kanam
Hoy los 3 productos SaaS son "retención" (recuperar relaciones perdidas). Este sería "marketplace" (crear relaciones nuevas). La frase paraguas de Kanam sería: **IA que facilita conexiones humanas que de otro modo no pasarían** — sea recuperándolas o creándolas.

KanamAI tendría que ampliarse para abarcar no solo generación (pre/post venta, copiloto) sino también ranking, matching y scoring. Es una extensión natural pero real.

### Momentos de KanamAI (definición ampliada, no solo retención)
- **Pre-venta:** SoporteML (consultas MeLi)
- **Post-venta:** SoporteML (sueño: mail/WhatsApp), ReActiva (pacientes inactivos)
- **Copiloto/durante:** UmbraWriter (escritor amateur)
- **Marketplace/matching:** este proyecto (futuro)

### Qué tendría que pasar para descongelarlo
1. SoporteML con billing funcionando y estable
2. UmbraWriter con PoC completado
3. ReActiva con primeros clientes o descartada
4. Capacidad de mantener 4 productos en paralelo sin dispersar

### Notas técnicas
- Creado con create-stack-next (estructura, AGENTS.md, ROADMAP, ADRs)
- Schema inicial: users (contratante/prestador) + services (categorías)
- Auth con JWT + jose
- ROADMAP en 3 fases, todo sin implementar
- Categorías actuales: limpieza, cuidado, cocina, reparaciones, jardinería, lavandería, otros

---