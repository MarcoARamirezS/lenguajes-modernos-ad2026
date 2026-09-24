# 07 — Variables de entorno y seguridad

## Frontend público

```text
NUXT_PUBLIC_FIREBASE_API_KEY=
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NUXT_PUBLIC_FIREBASE_PROJECT_ID=
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NUXT_PUBLIC_FIREBASE_APP_ID=
```

Estos valores configuran el SDK web. No otorgan privilegios administrativos por sí solos.

## Backend privado

```text
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=
GEMINI_API_KEY=
MAX_SOLVER_MS=8000
```

## Nunca subir

```text
.env
.env.*
!*.env.example
service-account*.json
firebase-adminsdk*.json
```

## Clave privada Firebase

Si Netlify almacena saltos de línea escapados, normalizar en runtime:

```ts
const privateKey = process.env.FIREBASE_PRIVATE_KEY?.replace(/\n/g, "
")
```

## Principios

- El frontend nunca recibe la private key.
- `GEMINI_API_KEY` solo existe en Functions.
- El backend verifica Firebase ID tokens.
- RBAC se valida en backend.
- Las entradas de Gemini pasan por Zod.
- Nunca se persiste una salida de IA sin validación y confirmación cuando modifica reglas académicas.
- Los logs no deben imprimir tokens ni secretos.

## Netlify

Crear variables en Project configuration → Environment variables y dar acceso al runtime de Functions cuando corresponda.

## Ambientes

Mantener al menos:

```text
local/emulator
preview
production
```

No usar el proyecto Firebase de producción durante prácticas destructivas.
