# EVALUATION — Sport Cars Jeep (Reinvención Digital)

## Evaluación de mercado

### Industria
- Mercado automotriz argentino altamente competitivo, con fuerte presión por concesionarias oficiales y usados.
- Jeep y Ram son marcas premium-masivas con reconocimiento fuerte.
- La digitalización de concesionarias en Argentina está atrasada: la mayoría tiene sitios estáticos, WhatsApp suelto y poca automatización.

### Tamaño de oportunidad
- Sport Cars tiene 3 sucursales y empleados de ventas activos.
- Un sitio que capture leads de calidad puede generar valor medible en meses.
- Si el modelo SaaS a 300 USD/mes funciona, puede replicarse a otros concesionarios del grupo (Neostar, Motorville, Guini) usando la misma base de código.

### Competidores directos (sitios Jeep oficiales en Argentina)
- **Neostar Jeep** (jeep.neostar.com.ar) — mismo template estático
- **Motorville** (motorville.com.ar) — mismo template estático
- **Guini Jeep** (guinijeep.com.ar) — mismo template estático
- **Giama Jeep** (giamajeep.com.ar) — WordPress custom, mejor diseño pero sin chatbot ni integraciones visibles

Ninguno tiene chatbot con RAG, inventario sincronizado, ni integración de leads directa con CRM. Sport Cars puede ser pionero en el grupo.

### Diferenciadores
1. Chatbot con IA generativa + RAG (único en el segmento local)
2. Inventario de usados sincronizado con MeLi en tiempo real
3. Leads capturados y notificados automáticamente
4. Test drive agendable online
5. Propuesta comercial clara: sitio como servicio, no proyecto caro

## Evaluación técnica

### Viabilidad
- **Alta.** Stack probado por Gonzo (Next.js, Supabase, Vercel, Ollama/DeepSeek).
- Mercado Libre API pública elimina dependencia de credenciales.
- Pilot CRM se difer para Post-MVP, reduciendo complejidad inicial.
- Chatbot custom es técnicamente factible con Vercel AI SDK + Ollama.

### Complejidad
- **Media.** No hay algoritmos complejos ni infraestructura exótica.
- Lo más complejo es el chatbot (RAG + prompts + control de costo).
- La integración MeLi es lectura pública simple.
- El panel de leads es CRUD básico.

### Riesgos técnicos
| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| MeLi rate-limita o cambia API pública | Media | Alto | Cache + fallback |
| Costo de Ollama/DeepSeek se sale de 300 USD | Baja | Medio | Ollama local reduce costo a casi cero; DeepSeek es barato |
| No se consiguen credenciales Pilot nunca | Media | Medio | MVP funciona sin Pilot; panel de leads + export CSV |
| Guidelines de Stellantis restringen diseño | Baja | Medio | Mantener branding Jeep oficial en colores/logos |
| Tráfico bajo genera pocos leads | Alta | Bajo | El sitio también valida el modelo SaaS para otros concesionarios |

### Dependencias externas
- Nickname/seller_id de Sport Cars en MeLi (fácil de conseguir)
- Acceso al DNS de sportcarsjeep.com.ar (para reemplazo final)
- Contenido para knowledge base del chatbot (necesita input de la hermana/vendedores)

## Evaluación estratégica

### Fit con objetivos de Gonzo
- Proyecto real con cliente real → portfolio vivo.
- Usa stack opinado de Gonzo → no tecnología nueva que aprender.
- Posible productizable: si funciona para Sport Cars, puede venderse a otras concesionarias.
- Open source contributions potenciales: componentes de chatbot, integración MeLi, etc.

### Fit con el cliente (Sport Cars)
- Pagan 300 USD/mes y obtienen un sitio que trabaja 24/7.
- No tienen que cambiar de CRM ni de procesos.
- Los vendedores reciben leads con datos útiles.
- Diferenciación frente a otras concesionarias Jeep.

## Evaluación financiera

### Costos mensuales estimados (presupuesto ajustado a 300 USD)

| Ítem | Costo estimado USD/mes |
|---|---|
| Vercel Pro + Analytics | ~20 |
| Supabase Pro (si escala) | ~25 |
| Dominio + DNS (sportcarsjeep.com.ar) | ~2 |
| Ollama local / DeepSeek API | ~0-30 |
| Email/notificaciones (Resend/Postmark) | ~0-10 |
| WhatsApp Business API (Post-MVP) | ~0 |
| Buffer / reserva | ~200-240 |
| **Total** | **~250-300** |

Si usás Ollama local en tu propia infraestructura, el costo de LLM es casi cero y el margen mejora mucho.

### Ingresos
- 300 USD/mes recurrentes por Sport Cars.
- Potencial de expansión a otras concesionarias del grupo a 300 USD cada una.

### ROI estimado para el cliente
- Si el sitio genera 1 venta extra cada 2-3 meses, ya se paga solo.
- Un Jeep Compass o Renegade representa margen de concesionario suficiente para justificar 300 USD/mes.

## Evaluación de esfuerzo

### Estimación
- **6-7 semanas** de trabajo part-time para MVP (según ROADMAP.md)
- Fase más incierta: chatbot (RAG + prompts)
- Fase más crítica: inventario MeLi (define si el catálogo es real o estático)

### Recursos necesarios
- 1 desarrollador (Gonzo)
- 1 contacto comercial/operativo (la hermana) para contenido y feedback
- Acceso ocasional a un decisor de Sport Cars para aprobaciones finales

## Veredicto

**GO para MVP.**

La oportunidad es clara, el stack es viable, el riesgo es manejable y el modelo comercial es sostenible. La principal incertidumbre no es técnica sino comercial: que Sport Cars valore el servicio y que Gonzo pueda replicarlo. Pero el proyecto vale la pena incluso como caso de estudio/portfolio.

## Recomendaciones

1. **Mantener el MVP acotado.** No agregar CMS, financing simulator ni WhatsApp Business API hasta v1.1.
2. **Documentar todo.** Este proyecto puede convertirse en producto replicable.
3. **Medir desde el día 1.** Analytics de eventos en Supabase para demostrar valor.
4. **Preparar el pitch de venta.** "Primera concesionaria Jeep con sitio con IA" es un buen gancho.
5. **Tener plan B para Pilot.** Si nunca dan credenciales, el producto sigue funcionando con panel de leads + notificaciones.