# ADR-023 — Patrón de Controlled Components con Single Change Handler

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns — Chapter 5 (Understanding and implementing forms)
**Scope:** Global — aplica a cualquier proyecto React con formularios

## Context

Los formularios en React pueden implementarse de dos formas:

1. **Uncontrolled components:** el DOM maneja el estado interno. Se accede al valor via `onChange` + `useState` o `ref`.
2. **Controlled components:** React controla el valor via `value` + `onChange`. El estado es la única fuente de verdad.

Para formularios con múltiples campos, crear un handler por campo no escala. El libro propone usar `event.target.name` para un solo handler.

## Decision

Usar **controlled components con un solo change handler** para formularios con 2+ campos. El handler usa `event.target.name` como key del estado.

### Patrón estándar

```tsx
type FormValues = Record<string, string>

const useForm = (initialValues: FormValues) => {
  const [values, setValues] = useState<FormValues>(initialValues)

  const handleChange = useCallback(
    ({ target: { name, value } }: ChangeEvent<HTMLInputElement>) => {
      setValues(prev => ({ ...prev, [name]: value }))
    },
    []
  )

  const reset = useCallback(() => setValues(initialValues), [initialValues])

  return { values, handleChange, reset }
}
```

### Uso

```tsx
const MyForm = () => {
  const { values, handleChange } = useForm({
    firstName: '',
    lastName: '',
    email: ''
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    console.log(values)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="firstName" value={values.firstName} onChange={handleChange} />
      <input name="lastName" value={values.lastName} onChange={handleChange} />
      <input name="email" value={values.email} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Rationale

1. **Escalabilidad:** un handler para N campos. Agregar un campo es agregar una entrada en `initialValues` y un `<input name="...">`.
2. **TypeScript:** el `name` del input se usa como key del objeto. Con `Record<string, string>` es flexible pero se puede tipar con tipos específicos.
3. **Callback form:** `setValues(prev => ...)` evita race conditions con React 18+ batching automático.
4. **Reusable:** el hook `useForm` se puede extraer a una librería o compartir entre formularios.

## Consequence

- Menos boilerplate que handlers individuales
- Un solo lugar para lógica de cambio de formulario
- Fácil de extender (validación, transformación de valores)
- Para formularios muy grandes (>20 campos), considerar librerías especializadas (React Hook Form, Formik)

## Referencias

- React docs — Controlled inputs: https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable
- React Hook Form: https://react-hook-form.com/
- React 18 Automatic Batching: https://react.dev/blog/2022/03/29/react-v18#new-feature-automatic-batching
