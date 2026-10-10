# Actores típicos y motivaciones

| Actor | Motivación típica | Capacidad / nivel |
|-------|-------------------|-------------------|
| Usuario malintencionado | Robo de datos de sesión, escalada de privilegios | Bajo-medio (credenciales robadas, XSS)
| Automatizado (bots/scrapers) | Denegación de servicio, extracción de contenido | Medio (alta frecuencia, bajo costo)
| Insider (desarrollador con acceso) | Filtración de lógica de negocio, credenciales | Alto (conoce el código)
| Proveedor/dependencia | Ataque de cadena de suministro, código malicioso | Variable (depende de la dep)

## Justificación de capacidades
- Bajo-medio: requiere interacción o credenciales.
