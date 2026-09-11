# Plantilla: respuesta ADHD-friendly

## Base

```
<accion concreta, imperativa, primera linea>

<contexto minimo, solo si cambia la accion - max 2 lineas>

1. <paso>
2. <paso>
3. <paso>

Next: <una accion, la mas chica y verificable>
```

## Con estado (sesion larga)

```
<accion concreta>

Estado: <que corre> | <que falta> | <que cambio>
<estimado: N minutos>

1. <paso>
2. <paso>

Next: <accion>
```

## Con error

```
<que fallo, en una linea, con codigo y ubicacion>

Causa: <una linea>

1. <paso de diagnostico>
2. <paso de fix>

Next: <que pegar / que correr>
```

## Con decision

```
<recomendacion, primera linea, con el motivo en una frase>

Opciones:
| Opcion | Costo | Cuando conviene |
|---|---|---|
| A | ... | ... |
| B | ... | ... |

Next: <accion para arrancar con la recomendada>
```

## Checklist de salida

- [ ] Primera linea es una accion, no contexto
- [ ] Multi-paso va numerado
- [ ] Termina en un next step ejecutable
- [ ] Time estimates en minutos si aplica
- [ ] Listas de max 5 items (o tabla si la lista es el entregable)
- [ ] Sin "Gran pregunta", "Espero que ayude", "Avisame si..."
- [ ] Guion comun (-), nunca em dash
- [ ] Errores sin drama ni disculpas largas
