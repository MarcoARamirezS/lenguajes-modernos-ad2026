[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← GitHub](./08_GITHUB_SETUP.md) · [Frontend base →](./10_FRONTEND_NUXT4_CODIGO_COMPLETO.md)

# 09 — Frontend Nuxt 4: instalación rápida

El frontend se prepara antes de las sesiones backend.

## Instalar dependencias

Desde la raíz:

```bash
npm install --workspace apps/web @pinia/nuxt pinia firebase
npm install -D --workspace apps/web tailwindcss @tailwindcss/vite daisyui
npm install -D concurrently
```

## Configuración

### `apps/web/package.json`

```json
{
  "name": "@aulaplan/web",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "nuxt dev",
    "build": "nuxt build",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "typecheck": "nuxt typecheck"
  },
  "dependencies": {
    "@pinia/nuxt": "latest",
    "firebase": "latest",
    "nuxt": "latest",
    "pinia": "latest",
    "vue": "latest",
    "vue-router": "latest"
  },
  "devDependencies": {
    "@tailwindcss/vite": "latest",
    "daisyui": "latest",
    "tailwindcss": "latest"
  }
}
```
### `apps/web/nuxt.config.ts`

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-09-01',
  ssr: false,
  devtools: { enabled: true },
  modules: ['@pinia/nuxt'],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL || '/api',
      useFirebaseEmulators:
        process.env.NUXT_PUBLIC_USE_FIREBASE_EMULATORS === 'true',
      firebaseApiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY || '',
      firebaseAuthDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN || '',
      firebaseProjectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID || '',
      firebaseStorageBucket:
        process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET || '',
      firebaseMessagingSenderId:
        process.env.NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '',
      firebaseAppId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID || '',
    },
  },
})
```
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
### `apps/web/app/assets/css/main.css`

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: light --default, dark --prefersdark;
}

html,
body,
#__nuxt {
  min-height: 100%;
}

body {
  background: var(--color-base-200);
}
```

## Variables locales

Copia:

```bash
cp apps/web/.env.example apps/web/.env
```

En Windows:

```powershell
Copy-Item apps/web/.env.example apps/web/.env
```

Reemplaza `PROJECT_ID` y las variables públicas con los valores de la aplicación Web de Firebase.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← GitHub](./08_GITHUB_SETUP.md) · [Frontend base →](./10_FRONTEND_NUXT4_CODIGO_COMPLETO.md)
