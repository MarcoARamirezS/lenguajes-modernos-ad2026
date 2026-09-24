# 02 — Frontend Nuxt 4: entrega única

## Objetivo

Entregar desde el inicio una interfaz completa para que las sesiones posteriores se concentren en backend, Firebase y scheduling.

## Stack frontend

- Nuxt 4.
- Vue 3.
- TypeScript strict.
- Composition API con `<script setup>`.
- Pinia.
- Tailwind CSS 4.
- daisyUI.
- Firebase Web SDK para login.

## Rutas

```text
/login
/dashboard
/academic-periods
/teachers
/subjects
/groups
/rooms
/time-blocks
/assignments
/availability
/constraints
/generator
/schedules
/schedules/:id
/users
/settings
```

## Capas frontend

```text
page
  ↓
component
  ↓
store/composable
  ↓
API client
  ↓
/api/*
```

No se accede directamente a Firestore para operaciones de negocio. La excepción es Firebase Authentication en el cliente para obtener el ID token.

## API client

La base URL será relativa:

```text
/api
```

Esto funciona igual en local mediante `netlify dev` y en producción porque frontend y Functions comparten dominio.

## Autenticación

```text
Firebase Auth client
   ↓
ID token
   ↓
Authorization: Bearer <token>
   ↓
/api/*
```

## Pantallas mínimas

### Dashboard

- profesores activos;
- grupos activos;
- salones disponibles;
- horarios publicados;
- estado del periodo actual.

### Generador

- periodo académico;
- parámetros del solver;
- caja para restricción escrita en lenguaje natural;
- botón validar datos;
- botón generar horario;
- score;
- conflictos;
- comparación de versiones.

### Horario

Vista semanal por:

- grupo;
- profesor;
- salón.

## Criterio de congelamiento

Al cerrar la entrega inicial:

- [ ] Navegación completa.
- [ ] Layout responsive.
- [ ] Estados loading/empty/error.
- [ ] Formularios listos.
- [ ] API client centralizado.
- [ ] Firebase Auth client integrado.
- [ ] No hay lógica de negocio del scheduler en el frontend.
- [ ] A partir de aquí solo se realizan ajustes de contrato y bugs.

## Configuración de Nuxt para frontend estático

Archivo `apps/web/nuxt.config.ts`:

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-09-01',
  devtools: { enabled: true },
  ssr: false,
  modules: ['@pinia/nuxt'],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()]
  },
  typescript: {
    strict: true,
    typeCheck: true
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || '/api',
      firebaseApiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY || '',
      firebaseAuthDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN || '',
      firebaseProjectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID || '',
      firebaseStorageBucket: process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET || '',
      firebaseMessagingSenderId: process.env.NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '',
      firebaseAppId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID || ''
    }
  }
})
```

Archivo `apps/web/app/assets/css/main.css` o la ruta equivalente generada por Nuxt:

```css
@import "tailwindcss";
@plugin "daisyui";
```

## Contrato del API client

Crear un único cliente que resuelva siempre contra `/api`. El token de Firebase se agrega por interceptor/composable; ninguna página arma URLs de backend manualmente.

Ejemplo conceptual:

```ts
export async function apiFetch<T>(path: string, options: RequestInit = {}) {
  const config = useRuntimeConfig()
  const token = await getCurrentFirebaseIdToken()

  const headers = new Headers(options.headers)
  headers.set('content-type', 'application/json')

  if (token) {
    headers.set('authorization', `Bearer ${token}`)
  }

  return await $fetch<T>(`${config.public.apiBaseUrl}${path}`, {
    ...options,
    headers
  })
}
```

La implementación final del frontend se entrega como un bloque único; las sesiones posteriores solo conectan endpoints y corrigen integración.
