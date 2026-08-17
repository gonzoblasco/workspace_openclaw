# ADR-028 - bcrypt para Password Hashing (No SHA1)

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns - Chapter 13 (Authentication functions)
**Scope:** Global - aplica a cualquier proyecto con autenticacion

## Context

El libro usa `@contentpi/lib` con `encrypt()` que implementa SHA1 para hashing de passwords:

```tsx
import { encrypt } from '@contentpi/lib'
// ...
beforeCreate: (user) => {
  user.password = encrypt(user.password)
}
```

SHA1 es un algoritmo de hashing criptograficamente debil. No debe usarse para almacenar passwords. Ademas, `@contentpi/lib` es una libreria del autor que no tiene mantenimiento activo.

## Decision

Usar **bcrypt** para hashing de passwords. bcrypt es un algoritmo de hashing adaptativo, disenado especificamente para almacenar passwords de forma segura.

```tsx
import bcrypt from 'bcrypt'

const SALT_ROUNDS = 12

// Hash
const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS)

// Verify
const isMatch = await bcrypt.compare(password, hashedPassword)
```

### En Sequelize (como el libro):

```tsx
import bcrypt from 'bcrypt'

const User = sequelize.define('User', {
  // ... fields
}, {
  hooks: {
    beforeCreate: async (user) => {
      user.password = await bcrypt.hash(user.password, 12)
    }
  }
})
```

### En Drizzle ORM (recomendado 2026):

```tsx
import { pgTable, uuid, varchar, boolean } from 'drizzle-orm/pg-core'
import { sql } from 'drizzle-orm'

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  username: varchar('username', { length: 255 }).notNull().unique(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  password: varchar('password', { length: 255 }).notNull(),
  role: varchar('role', { length: 50 }).notNull().default('user'),
  active: boolean('active').notNull().default(false),
})
```

## Rationale

1. **SHA1 es inseguro:** ataques de colision y rainbow tables hacen SHA1 inadecuado para passwords
2. **bcrypt es adaptativo:** el factor de costo se puede aumentar a medida que el hardware mejora
3. **Salt incorporado:** bcrypt genera un salt unico por password automaticamente
4. **`@contentpi/lib` no es mantenido:** no deberia ser una dependencia de produccion
5. **bcrypt es el estandar:** usado por Rails, Django, y la mayoria de frameworks modernos

## Consequence

- Passwords almacenados de forma segura
- Migracion desde SHA1 requiere que todos los usuarios cambien su password (o re-hash en el proximo login)
- Dependencia de `bcrypt` (nativa, requiere build tools) o `bcryptjs` (JS puro, mas lento)

## Referencias

- OWASP - Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- bcrypt: https://www.npmjs.com/package/bcrypt
- bcryptjs (alternativa JS pura): https://www.npmjs.com/package/bcryptjs
- Why you should use bcrypt: https://danboterhoven.medium.com/why-you-should-use-bcrypt-to-hash-passwords-af330100b861
