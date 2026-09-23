# AulaPlan AI — Frontend Nuxt 4 en una sola entrega

## Propósito

El frontend se instala y deja preparado desde el inicio. El objetivo del curso no es dedicar una sesión a cada pantalla, sino conectar progresivamente un cliente Nuxt completo con el backend FastAPI.

## Dependencias

Desde raíz:

```bash
npm install --workspace apps/web @pinia/nuxt firebase
npm install --workspace apps/web -D tailwindcss@latest @tailwindcss/vite@latest daisyui@latest
```

## Estructura

```text
apps/web/
├── app/
│   ├── assets/css/main.css
│   ├── components/
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   ├── EmptyState.vue
│   │   ├── PageHeader.vue
│   │   └── StatCard.vue
│   ├── composables/useApi.ts
│   ├── layouts/default.vue
│   ├── middleware/auth.ts
│   ├── pages/
│   │   ├── index.vue
│   │   ├── login.vue
│   │   ├── dashboard.vue
│   │   ├── teachers.vue
│   │   ├── subjects.vue
│   │   ├── groups.vue
│   │   ├── rooms.vue
│   │   ├── academic-periods.vue
│   │   ├── availability.vue
│   │   ├── constraints.vue
│   │   ├── generator.vue
│   │   ├── schedules/index.vue
│   │   └── settings.vue
│   ├── plugins/firebase.client.ts
│   ├── stores/auth.ts
│   ├── types/domain.ts
│   └── app.vue
├── nuxt.config.ts
└── .env.example
```

## `nuxt.config.ts`

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-09-01',
  devtools: { enabled: true },
  ssr: false,
  modules: ['@pinia/nuxt'],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
      firebaseApiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY || '',
      firebaseAuthDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN || '',
      firebaseProjectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID || '',
      firebaseStorageBucket: process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET || '',
      firebaseMessagingSenderId: process.env.NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '',
      firebaseAppId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID || '',
    },
  },
})
```

## `app/assets/css/main.css`

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
  min-height: 100vh;
}
```

## `app/app.vue`

```vue
<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
```

## `app/types/domain.ts`

```ts
export type EntityId = string

export interface Teacher {
  id: EntityId
  employeeNumber: string
  name: string
  email: string
  active: boolean
}

export interface Subject {
  id: EntityId
  code: string
  name: string
  weeklyBlocks: number
  roomType: 'CLASSROOM' | 'LAB' | 'COMPUTER_LAB' | 'AUDITORIUM'
  active: boolean
}

export interface AcademicGroup {
  id: EntityId
  code: string
  size: number
  active: boolean
}

export interface Room {
  id: EntityId
  code: string
  name: string
  capacity: number
  type: 'CLASSROOM' | 'LAB' | 'COMPUTER_LAB' | 'AUDITORIUM'
  active: boolean
}

export interface ScheduleVersion {
  id: EntityId
  version: number
  status: 'DRAFT' | 'GENERATED' | 'REVIEWED' | 'PUBLISHED' | 'ARCHIVED'
  score: number | null
  createdAt: string
}
```

## `app/plugins/firebase.client.ts`

```ts
import { initializeApp, getApps } from 'firebase/app'
import { getAuth } from 'firebase/auth'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const firebaseConfig = {
    apiKey: config.public.firebaseApiKey,
    authDomain: config.public.firebaseAuthDomain,
    projectId: config.public.firebaseProjectId,
    storageBucket: config.public.firebaseStorageBucket,
    messagingSenderId: config.public.firebaseMessagingSenderId,
    appId: config.public.firebaseAppId,
  }

  const app = getApps()[0] ?? initializeApp(firebaseConfig)
  const auth = getAuth(app)

  return {
    provide: {
      firebaseAuth: auth,
    },
  }
})
```

## `app/stores/auth.ts`

```ts
import { defineStore } from 'pinia'
import { onAuthStateChanged, signInWithEmailAndPassword, signOut, type User } from 'firebase/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const ready = ref(false)

  const init = () => {
    const { $firebaseAuth } = useNuxtApp()
    onAuthStateChanged($firebaseAuth, (value) => {
      user.value = value
      ready.value = true
    })
  }

  const login = async (email: string, password: string) => {
    const { $firebaseAuth } = useNuxtApp()
    await signInWithEmailAndPassword($firebaseAuth, email, password)
  }

  const logout = async () => {
    const { $firebaseAuth } = useNuxtApp()
    await signOut($firebaseAuth)
    await navigateTo('/login')
  }

  const getIdToken = async () => user.value ? user.value.getIdToken() : null

  return { user, ready, init, login, logout, getIdToken }
})
```

## `app/composables/useApi.ts`

```ts
export const useApi = () => {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  const request = async <T>(path: string, options: Parameters<typeof $fetch<T>>[1] = {}) => {
    const token = await auth.getIdToken()
    const headers = new Headers(options.headers as HeadersInit | undefined)

    if (token) {
      headers.set('Authorization', `Bearer ${token}`)
    }

    return $fetch<T>(path, {
      ...options,
      baseURL: config.public.apiBaseUrl,
      headers,
    })
  }

  return { request }
}
```

## `app/layouts/default.vue`

```vue
<script setup lang="ts">
const auth = useAuthStore()

onMounted(() => {
  if (!auth.ready) auth.init()
})
</script>

<template>
  <div class="drawer lg:drawer-open">
    <input id="main-drawer" type="checkbox" class="drawer-toggle">
    <div class="drawer-content min-h-screen bg-base-200">
      <AppHeader />
      <main class="p-4 lg:p-6">
        <slot />
      </main>
    </div>
    <div class="drawer-side z-40">
      <label for="main-drawer" class="drawer-overlay" />
      <AppSidebar />
    </div>
  </div>
</template>
```

## `app/components/AppHeader.vue`

```vue
<script setup lang="ts">
const auth = useAuthStore()
</script>

<template>
  <header class="navbar border-b border-base-300 bg-base-100 px-4 lg:px-6">
    <div class="flex-none lg:hidden">
      <label for="main-drawer" class="btn btn-square btn-ghost" aria-label="Abrir menú">☰</label>
    </div>
    <div class="flex-1">
      <span class="text-lg font-semibold">AulaPlan AI</span>
    </div>
    <button v-if="auth.user" class="btn btn-ghost btn-sm" @click="auth.logout()">
      Cerrar sesión
    </button>
  </header>
</template>
```

## `app/components/AppSidebar.vue`

```vue
<script setup lang="ts">
const items = [
  ['Dashboard', '/dashboard'],
  ['Profesores', '/teachers'],
  ['Materias', '/subjects'],
  ['Grupos', '/groups'],
  ['Salones', '/rooms'],
  ['Periodos', '/academic-periods'],
  ['Disponibilidad', '/availability'],
  ['Restricciones', '/constraints'],
  ['Generador IA', '/generator'],
  ['Horarios', '/schedules'],
  ['Configuración', '/settings'],
]
</script>

<template>
  <aside class="min-h-full w-72 border-r border-base-300 bg-base-100 p-4">
    <div class="mb-6">
      <p class="text-xs font-semibold uppercase opacity-60">Lenguajes Modernos</p>
      <h1 class="text-2xl font-bold">AulaPlan AI</h1>
    </div>
    <ul class="menu gap-1">
      <li v-for="item in items" :key="item[1]">
        <NuxtLink :to="item[1]">{{ item[0] }}</NuxtLink>
      </li>
    </ul>
  </aside>
</template>
```

## `app/components/PageHeader.vue`

```vue
<script setup lang="ts">
defineProps<{ title: string; description?: string }>()
</script>

<template>
  <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="text-3xl font-bold">{{ title }}</h1>
      <p v-if="description" class="mt-1 opacity-70">{{ description }}</p>
    </div>
    <div><slot /></div>
  </div>
</template>
```

## `app/components/StatCard.vue`

```vue
<script setup lang="ts">
defineProps<{ title: string; value: string | number; note?: string }>()
</script>

<template>
  <div class="stat rounded-box border border-base-300 bg-base-100">
    <div class="stat-title">{{ title }}</div>
    <div class="stat-value text-2xl">{{ value }}</div>
    <div v-if="note" class="stat-desc">{{ note }}</div>
  </div>
</template>
```

## `app/components/EmptyState.vue`

```vue
<script setup lang="ts">
defineProps<{ title: string; description: string }>()
</script>

<template>
  <div class="rounded-box border border-dashed border-base-300 bg-base-100 p-10 text-center">
    <h2 class="text-xl font-semibold">{{ title }}</h2>
    <p class="mt-2 opacity-70">{{ description }}</p>
  </div>
</template>
```

## `app/pages/index.vue`

```vue
<script setup lang="ts">
await navigateTo('/dashboard')
</script>
```

## `app/pages/login.vue`

```vue
<script setup lang="ts">
definePageMeta({ layout: false })

const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    await auth.login(email.value, password.value)
    await navigateTo('/dashboard')
  } catch {
    error.value = 'No fue posible iniciar sesión.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="grid min-h-screen place-items-center bg-base-200 p-4">
    <form class="card w-full max-w-md bg-base-100 shadow-xl" @submit.prevent="submit">
      <div class="card-body">
        <h1 class="card-title text-3xl">AulaPlan AI</h1>
        <p class="opacity-70">Acceso para coordinación académica.</p>
        <label class="form-control mt-4">
          <span class="label-text">Correo</span>
          <input v-model="email" type="email" class="input input-bordered" required>
        </label>
        <label class="form-control">
          <span class="label-text">Contraseña</span>
          <input v-model="password" type="password" class="input input-bordered" required>
        </label>
        <div v-if="error" class="alert alert-error text-sm">{{ error }}</div>
        <button class="btn btn-primary mt-2" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </div>
    </form>
  </main>
</template>
```

## `app/pages/dashboard.vue`

```vue
<template>
  <section>
    <PageHeader title="Dashboard" description="Resumen operativo de AulaPlan AI." />
    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard title="Profesores" value="--" note="Se conectará en sesión 04" />
      <StatCard title="Materias" value="--" note="Se conectará en sesión 04" />
      <StatCard title="Grupos" value="--" note="Se conectará en sesión 05" />
      <StatCard title="Horarios" value="--" note="Se conectará en sesión 12" />
    </div>
  </section>
</template>
```

## Páginas de catálogo

Crear `teachers.vue`, `subjects.vue`, `groups.vue`, `rooms.vue`, `academic-periods.vue`, `availability.vue` y `constraints.vue` con el siguiente patrón, cambiando título y descripción:

```vue
<template>
  <section>
    <PageHeader title="Profesores" description="Administración del catálogo de profesores.">
      <button class="btn btn-primary" disabled>Nuevo</button>
    </PageHeader>
    <EmptyState
      title="Módulo preparado"
      description="La interfaz se conectará con FastAPI durante las sesiones de backend."
    />
  </section>
</template>
```

## `app/pages/generator.vue`

```vue
<script setup lang="ts">
const text = ref('')
</script>

<template>
  <section>
    <PageHeader
      title="Generador inteligente"
      description="Interpreta restricciones y genera una nueva versión de horario."
    />
    <div class="grid gap-6 xl:grid-cols-2">
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <h2 class="card-title">Restricciones en lenguaje natural</h2>
          <textarea
            v-model="text"
            class="textarea textarea-bordered min-h-48"
            placeholder="Ej. El profesor Marco no puede los martes y prefiere terminar antes de las 13:00."
          />
          <button class="btn btn-secondary" disabled>Interpretar con IA</button>
        </div>
      </div>
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <h2 class="card-title">Generación</h2>
          <p class="opacity-70">OR-Tools se conectará en las sesiones 08–10.</p>
          <button class="btn btn-primary" disabled>Generar horario</button>
        </div>
      </div>
    </div>
  </section>
</template>
```

## `app/pages/schedules/index.vue`

```vue
<template>
  <section>
    <PageHeader title="Horarios" description="Versiones generadas y publicadas." />
    <EmptyState title="Sin horarios" description="Las versiones aparecerán después de integrar el solver." />
  </section>
</template>
```

## `app/pages/settings.vue`

```vue
<template>
  <section>
    <PageHeader title="Configuración" description="Parámetros generales de la institución." />
    <div class="card max-w-2xl bg-base-100 shadow-sm">
      <div class="card-body">
        <p class="opacity-70">Esta pantalla se habilitará cuando existan los endpoints de configuración.</p>
      </div>
    </div>
  </section>
</template>
```

## Verificación

```bash
npm run dev --workspace apps/web
```

Abrir:

```text
http://localhost:3000
```

Debe existir navegación hacia todas las páginas sin errores 404.

## Criterio de cierre

- [ ] Nuxt inicia.
- [ ] Tailwind funciona.
- [ ] daisyUI funciona.
- [ ] Pinia está configurado.
- [ ] Firebase client está preparado.
- [ ] Sidebar navega por todos los módulos.
- [ ] El frontend no contiene secretos.
- [ ] `useApi` está preparado para agregar Firebase ID Token.

## Nota didáctica

Las pantallas están intencionalmente preparadas antes del backend. A partir de la sesión 04, cada módulo se conecta al endpoint correspondiente sin rediseñar toda la aplicación.
