# Mitigaciones por riesgo priorizado

| Riesgo | Mitigación propuesta | Tipo | Esfuerzo | Owner |
|--------|----------------------|------|----------|-------|
| API de salud: DoS | Rate limiter por IP (middleware) | Arquitectónico | M | Equipo backend |
| API de salud: EoP | Validar sesión + scope en cada endpoint | De código | M | Equipo backend |
| API de datos: Info Disclosure | Filtrar campos sensibles antes de responder | De código | M | Equipo backend |
| API de datos: DoS | Rate limiter + paginación por defecto | Arquitectónico | M | Equipo backend |
| API de datos: EoP | Validar sesión + verificar propiedad del recurso | De código | M | Equipo backend |

## Próximos steps (backlog)
- [ ] Implementar rate limiter en  y 
- [ ] Agregar validación de sesión a todos los endpoints API
- [ ] Revisar respuestas API para eliminar campos no necesarios (p. ej. contraseñas hasheadas, tokens internos)
