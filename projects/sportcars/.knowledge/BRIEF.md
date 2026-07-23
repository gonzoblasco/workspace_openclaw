# BRIEF — Sport Cars Jeep (Reinvención Digital)

## Contexto

**Sport Cars** es un concesionario oficial Jeep y Ram con 3 sucursales (Quilmes, La Plata, CABA Belgrano). Actualmente tiene un sitio web (sportcarsjeep.com.ar) que usa un template genérico compartido por otros concesionarios del grupo (Neostar, Motorville, Guini — todos con la misma estructura). El sitio es estático, sin inventario real, sin integración con CRM, sin chatbot, y con links a WhatsApp como única interacción.

**Gonzo** tiene un contacto directo (su hermana trabaja en el local) que puede facilitar entrada comercial y acceso a información interna (credenciales Pilot, proceso de ventas, necesidades del personal).

## Problema en una frase

> El sitio actual de Sport Cars es una brochure estática que no convierte visitantes en leads ni facilita el trabajo comercial del concesionario.

## Situación actual (relevamiento)

### Sitio actual — sportcarsjeep.com.ar
- Template WordPress compartido por múltiples concesionarios Jeep (Stellantis Argentina)
- Secciones: Vehículos (catálogo estático), Sucursales, Contacto, Cotizador de Usados, Test Drive
- Sin inventario real de 0km ni usados
- Sin integración con Pilot CRM (el CRM que ya usan internamente)
- Sin chatbot ni sistema de consultas automatizado
- Links sueltos a WhatsApp como único canal de contacto
- Sin integración con Mercado Libre (a pesar de que Pilot está certificado por MeLi)
- 3 sucursales con horarios, teléfonos y WhatsApp listados manualmente

### Pilot CRM (pilotsolution.net)
- CRM líder en industria automotriz Argentina, 300+ cuentas integradas
- **Certificado por Mercado Libre Argentina** — integrador líder del vertical Motors
- API con autenticación JWT (`/api_pilot/auth/login` → token bearer)
- Webhook para creación de leads (`/pilot/leadcreation/webhook`)
- Integración vía app token + código de sub origen (visible en módulo Admin de Pilot)
- Tiene módulo de micrositio con stock, geolocalización y WhatsApp 24/7
- Bot de WhatsApp con IA generativa integrado (base de conocimiento personalizada)
- Integraciones plug & play + Powerflow para flujos custom
- App móvil para vendedores

### Competidores (mismo template)
- Neostar (Rosario), Motorville, Guini — todos usan el mismo sitio plantilla
- Ninguno parece tener integración profunda con CRM o chatbot inteligente
- Oportunidad: Sport Cars puede diferenciarse siendo el primero en romper el molde

## Stakeholders

- **Gonzo** — desarrollador/diseñador del nuevo sitio
- **Hermana de Gonzo** — empleada del concesionario, contacto comercial e información interna
- **Sport Cars (el concesionario)** — cliente final, debe ver valor comercial real
- **Vendedores del concesionario** — usuarios indirectos del CRM, beneficiarios de mejores leads

## Premisas y restricciones

### Lo que sabemos
- Pilot CRM ya está en uso interno → no hay que convencer de adoptar un CRM nuevo
- Pilot tiene API + integración con MeLi → la infraestructura existe
- El acceso a credenciales (app token, sub origen) se puede obtener vía la hermana
- El template actual es shared/white-label → probablemente no se puede modificar profundaente sin romper la relación con Stellantis

### Lo que NO sabemos (preguntas abiertas para 0.2)
- ¿El sitio nuevo reemplaza al actual o convive? (¿subdominio? ¿dominio nuevo?)
- ¿Qué nivel de acceso nos da Pilot API? ¿Solo lead creation o también stock/inventario?
- ¿Sport Cars publica en MeLi directamente o vía Pilot? ¿Qué permisos necesitamos?
- ¿El concesionario quiere mantener el template Stellantis o está abierto a algo custom?
- ¿Hay branding guidelines de Jeep/Stellantis que respetar?
- ¿Presupuesto para hosting/servicios (dominio, Vercel/ hosting, LLM para chatbot)?

## Técnica de brainstorming aplicada

### SCAMPER
- **S**ubstitute: Reemplazar el sitio brochure por una plataforma de conversión + integración CRM
- **C**ombine: Unificar inventario MeLi + Pilot + sitio web en un solo flujo
- **A**dapt: Adaptar el chatbot con base de conocimiento del concesionario (stock, financiación, test drive)
- **M**odify: Modificar el modelo de "catálogo estático" a "catálogo dinámico con consulta en tiempo real"
- **P**ut to other use: Usar la hermana como insider para entender el flujo real de ventas
- **E**liminate: Eliminar fricción — el usuario no debería tener que salir del sitio para preguntar algo
- **R**everse: En lugar de "el usuario busca y contacta", "el chatbot guía al usuario según su intención y deriva a humano cuando hace falta"

### Inversión
En lugar de "¿cómo hacemos un sitio más lindo?", preguntar: **¿qué haría que un vendedor de Sport Cars diga "esto me ahorra 2 horas por día"?**

Respuesta: leads pre-calificados con datos ya en Pilot, consultas de stock respondidas sin llamar, citas de test drive agendadas sin intermediario.

### Primeros principios
1. El sitio existe para **generar leads** y **facilitar ventas**, no para ser lindo
2. El CRM (Pilot) ya es la fuente de verdad interna → el sitio debe hablar con él
3. MeLi es donde están los compradores → integrar, no solo linkear
4. Un chatbot bien entrenado reduce barreras de entrada vs. "envianos un WhatsApp"
5. La hermana es el puente — su input del día a día vale más que cualquier spec externa

## Propuesta de valor

**Sport Cars Digital**: la primera concesionaria Jeep de Argentina con un sitio que realmente trabaja para el vendedor — inventario sincronizado, consultas automatizadas, leads directos al CRM, e integración con Mercado Libre. No una brochure online, un vendedor digital 24/7.

## Diferenciación vs. competencia

| Aspecto | Sitios actuales (Neostar, Guini, Motorville) | Sport Cars reinventado |
|---|---|---|
| Inventario | Catálogo estático de modelos | Stock real sincronizado (Pilot/MeLi) |
| Consultas | WhatsApp link suelto | Chatbot con base de conocimiento + derivación a humano |
| CRM | Sin integración | Leads automáticos a Pilot via API |
| MeLi | Sin integración | Publicaciones sincronizadas / consulta desde sitio |
| UX | Template genérico | Diseño propio, optimizado para conversión |
| Test Drive | Formulario que no sabemos a dónde va | Agendamiento integrado con Pilot |
| Usados | "Cotizador" genérico | Evaluación + inventario de usados real |

## Modelos de monetización / relación comercial

Esto necesita definirse con Gonzo:

1. **Proyecto a fondo perdido / portfolio**: Gonzo lo hace como caso de estudio real, la hermana le abre la puerta, Sport Cars no paga
2. **Servicio pagado**: Gonzo cobra por el desarrollo/mantenimiento
3. **Revenue share**: Gonzo cobra una parte por cada lead que cierre vía el sitio
4. **Híbrido**: Desarrollo gratis, mantenimiento mensual pagado

## Próximos pasos (post-0.1)

1. Gonzo valida la propuesta de valor y define el modelo comercial
2. La hermana consigue: credenciales Pilot (app token, sub origen), info de cómo publican en MeLi, si hay guidelines de Stellantis
3. Fase 0.2: arquitectura técnica (stack, integraciones, diagrama C4, ADRs)
4. Validar si Pilot API da acceso a stock o solo a lead creation