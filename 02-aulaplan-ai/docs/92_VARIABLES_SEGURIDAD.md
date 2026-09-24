[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Modelo Firestore](./91_MODELO_FIRESTORE.md) · [Comandos rápidos →](./93_COMANDOS_RAPIDOS.md)

# 92 — Variables de entorno y secretos

## Frontend

### `apps/web/.env.example`

```text
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5001/PROJECT_ID/us-central1/api
NUXT_PUBLIC_USE_FIREBASE_EMULATORS=true
NUXT_PUBLIC_FIREBASE_API_KEY=
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NUXT_PUBLIC_FIREBASE_PROJECT_ID=
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NUXT_PUBLIC_FIREBASE_APP_ID=
```


Estas variables son públicas. **Nunca** pongas secretos en variables `NUXT_PUBLIC_*`.

## Backend local

Gemini:

```text
apps/api/.secret.local
```

```env
GEMINI_API_KEY=...
```

## Producción

```bash
firebase functions:secrets:set GEMINI_API_KEY
```

## Credenciales Firebase Admin

En Cloud Functions se usan credenciales administradas por Google.

Para scripts locales contra un proyecto real, usa Application Default Credentials o `GOOGLE_APPLICATION_CREDENTIALS` apuntando a un archivo fuera del repositorio.

## Nunca subir

### `.gitignore`

```text
node_modules/
apps/web/.nuxt/
apps/web/.output/
apps/web/.env
apps/web/.env.*
!apps/web/.env.example
apps/api/.venv/
apps/api/venv/
apps/api/__pycache__/
apps/api/**/*.pyc
apps/api/.env
apps/api/.env.*
apps/api/.secret.local
serviceAccount*.json
.firebase/
.DS_Store
coverage/
playwright-report/
test-results/
```


## CORS y proxy

El endpoint de Functions puede recibir requests externos, pero la aplicación sigue validando Firebase ID tokens para rutas protegidas. En producción Nuxt consume `/api/*` a través de Netlify.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Modelo Firestore](./91_MODELO_FIRESTORE.md) · [Comandos rápidos →](./93_COMANDOS_RAPIDOS.md)
