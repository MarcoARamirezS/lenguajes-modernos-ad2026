[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Frontend setup](./09_FRONTEND_NUXT4_SETUP.md) · [Frontend páginas →](./11_FRONTEND_NUXT4_PAGINAS_Y_PRUEBA.md)

# 10 — Frontend Nuxt 4: código completo — base

Crea cada archivo exactamente en la ruta indicada.

### `apps/web/app/app.vue`

```vue
<template>
  <NuxtLoadingIndicator />
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
```
### `apps/web/app/types/index.ts`

```ts
export type Role = 'ADMIN' | 'COORDINATOR' | 'VIEWER'

export interface UserProfile {
  uid: string
  email: string
  display_name?: string
  role: Role
  active: boolean
}

export interface CatalogRecord {
  id: string
  [key: string]: unknown
}

export interface CatalogField {
  key: string
  label: string
  type?: 'text' | 'number' | 'email' | 'select' | 'checkbox'
  required?: boolean
  options?: Array<{ label: string; value: string }>
  defaultValue?: string | number | boolean
}

export interface ScheduleEntry {
  offering_id: string
  subject_id: string
  teacher_id: string
  group_id: string
  room_id: string
  time_block_id: string
  day: string
  start_time: string
  end_time: string
}

export interface ScheduleVersion {
  version: number
  score: number
  entries: ScheduleEntry[]
}
```
### `apps/web/app/plugins/firebase.client.ts`

```ts
import { initializeApp, getApps } from 'firebase/app'
import {
  connectAuthEmulator,
  getAuth,
  onAuthStateChanged,
} from 'firebase/auth'

export default defineNuxtPlugin(async () => {
  const config = useRuntimeConfig()

  const firebaseConfig = {
    apiKey: config.public.firebaseApiKey,
    authDomain: config.public.firebaseAuthDomain,
    projectId: config.public.firebaseProjectId,
    storageBucket: config.public.firebaseStorageBucket,
    messagingSenderId: config.public.firebaseMessagingSenderId,
    appId: config.public.firebaseAppId,
  }

  const app = getApps()[0] || initializeApp(firebaseConfig)
  const auth = getAuth(app)

  if (config.public.useFirebaseEmulators) {
    try {
      connectAuthEmulator(auth, 'http://127.0.0.1:9099', {
        disableWarnings: true,
      })
    } catch {
      // El plugin se carga una vez; este catch evita fallar durante HMR.
    }
  }

  const authStore = useAuthStore()

  await new Promise<void>((resolve) => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      authStore.setFirebaseUser(user)
      authStore.setReady(true)
      unsubscribe()
      resolve()
    })
  })

  return {
    provide: {
      firebaseAuth: auth,
    },
  }
})
```
### `apps/web/app/stores/auth.ts`

```ts
import type { User } from 'firebase/auth'
import type { UserProfile } from '~/types'

export const useAuthStore = defineStore('auth', () => {
  const firebaseUser = shallowRef<User | null>(null)
  const profile = ref<UserProfile | null>(null)
  const ready = ref(false)

  const isAuthenticated = computed(() => Boolean(firebaseUser.value))
  const role = computed(() => profile.value?.role ?? null)

  function setFirebaseUser(user: User | null) {
    firebaseUser.value = user
    if (!user) profile.value = null
  }

  function setProfile(value: UserProfile | null) {
    profile.value = value
  }

  function setReady(value: boolean) {
    ready.value = value
  }

  return {
    firebaseUser,
    profile,
    ready,
    isAuthenticated,
    role,
    setFirebaseUser,
    setProfile,
    setReady,
  }
})
```
### `apps/web/app/composables/useApi.ts`

```ts
export function useApi() {
  const config = useRuntimeConfig()
  const { $firebaseAuth } = useNuxtApp()

  async function request<T>(path: string, options: Record<string, unknown> = {}) {
    const user = $firebaseAuth.currentUser
    const token = user ? await user.getIdToken() : null
    const headers = new Headers((options.headers as HeadersInit | undefined) || {})

    if (token) headers.set('Authorization', `Bearer ${token}`)
    headers.set('Content-Type', 'application/json')

    return await $fetch<T>(path, {
      baseURL: config.public.apiBase,
      ...options,
      headers,
    })
  }

  return { request }
}
```
### `apps/web/app/composables/useAuth.ts`

```ts
import { signInWithEmailAndPassword, signOut } from 'firebase/auth'
import type { UserProfile } from '~/types'

export function useAuth() {
  const { $firebaseAuth } = useNuxtApp()
  const store = useAuthStore()
  const { request } = useApi()

  async function loadProfile() {
    if (!$firebaseAuth.currentUser) {
      store.setProfile(null)
      return
    }

    const profile = await request<UserProfile>('/auth/me')
    store.setProfile(profile)
  }

  async function login(email: string, password: string) {
    const credential = await signInWithEmailAndPassword(
      $firebaseAuth,
      email,
      password,
    )
    store.setFirebaseUser(credential.user)
    await loadProfile()
  }

  async function logout() {
    await signOut($firebaseAuth)
    store.setFirebaseUser(null)
    await navigateTo('/login')
  }

  return { login, logout, loadProfile }
}
```
### `apps/web/app/middleware/auth.global.ts`

```ts
export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const store = useAuthStore()
  const publicRoutes = ['/login']

  if (!store.ready) return

  if (!store.isAuthenticated && !publicRoutes.includes(to.path)) {
    return navigateTo('/login')
  }

  if (store.isAuthenticated && to.path === '/login') {
    return navigateTo('/dashboard')
  }
})
```
### `apps/web/app/layouts/auth.vue`

```vue
<template>
  <main class="min-h-screen bg-base-200 p-4 flex items-center justify-center">
    <div class="w-full max-w-md">
      <slot />
    </div>
  </main>
</template>
```
### `apps/web/app/layouts/default.vue`

```vue
<template>
  <div class="drawer lg:drawer-open min-h-screen">
    <input id="aulaplan-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex min-w-0 flex-col">
      <AppHeader />
      <main class="p-4 lg:p-6">
        <slot />
      </main>
    </div>
    <div class="drawer-side z-40">
      <label for="aulaplan-drawer" class="drawer-overlay" />
      <AppSidebar />
    </div>
  </div>
</template>
```
### `apps/web/app/components/AppHeader.vue`

```vue
<script setup lang="ts">
const { logout } = useAuth()
const store = useAuthStore()
</script>

<template>
  <header class="navbar sticky top-0 z-30 border-b border-base-300 bg-base-100 px-4">
    <div class="flex-none lg:hidden">
      <label for="aulaplan-drawer" class="btn btn-square btn-ghost" aria-label="Abrir menú">☰</label>
    </div>
    <div class="flex-1">
      <span class="font-semibold">AulaPlan AI</span>
    </div>
    <div class="flex items-center gap-3">
      <div class="hidden text-right sm:block">
        <p class="text-sm font-medium">{{ store.profile?.display_name || store.firebaseUser?.email }}</p>
        <p class="text-xs opacity-60">{{ store.profile?.role }}</p>
      </div>
      <button class="btn btn-sm btn-outline" @click="logout">Salir</button>
    </div>
  </header>
</template>
```
### `apps/web/app/components/AppSidebar.vue`

```vue
<script setup lang="ts">
const items = [
  ['Dashboard', '/dashboard'],
  ['Periodos', '/academic-periods'],
  ['Profesores', '/teachers'],
  ['Materias', '/subjects'],
  ['Grupos', '/groups'],
  ['Salones', '/rooms'],
  ['Bloques', '/time-blocks'],
  ['Ofertas académicas', '/offerings'],
  ['Disponibilidad', '/availability'],
  ['Restricciones', '/constraints'],
  ['Generador', '/generator'],
  ['Horarios', '/schedules'],
  ['Usuarios', '/users'],
]
</script>

<template>
  <aside class="min-h-full w-72 border-r border-base-300 bg-base-100 p-4">
    <NuxtLink to="/dashboard" class="mb-6 block text-xl font-bold">AulaPlan AI</NuxtLink>
    <ul class="menu gap-1 p-0">
      <li v-for="item in items" :key="item[1]">
        <NuxtLink :to="item[1]" active-class="menu-active">{{ item[0] }}</NuxtLink>
      </li>
    </ul>
  </aside>
</template>
```
### `apps/web/app/components/StatCard.vue`

```vue
<script setup lang="ts">
defineProps<{ title: string; value: string | number; description?: string }>()
</script>

<template>
  <div class="card border border-base-300 bg-base-100 shadow-sm">
    <div class="card-body">
      <p class="text-sm opacity-60">{{ title }}</p>
      <p class="text-3xl font-bold">{{ value }}</p>
      <p v-if="description" class="text-sm opacity-60">{{ description }}</p>
    </div>
  </div>
</template>
```
### `apps/web/app/components/catalog/CatalogManager.vue`

```vue
<script setup lang="ts">
import type { CatalogField, CatalogRecord } from '~/types'

const props = defineProps<{
  title: string
  endpoint: string
  fields: CatalogField[]
}>()

const { request } = useApi()
const rows = ref<CatalogRecord[]>([])
const form = reactive<Record<string, unknown>>({})
const editingId = ref<string | null>(null)
const loading = ref(false)
const errorMessage = ref('')

function resetForm() {
  editingId.value = null
  for (const key of Object.keys(form)) delete form[key]
  for (const field of props.fields) {
    form[field.key] = field.defaultValue ?? (field.type === 'checkbox' ? true : '')
  }
}

async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    rows.value = await request<CatalogRecord[]>(props.endpoint)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No fue posible cargar los datos.'
  } finally {
    loading.value = false
  }
}

function edit(row: CatalogRecord) {
  editingId.value = row.id
  for (const field of props.fields) form[field.key] = row[field.key]
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function save() {
  const method = editingId.value ? 'PUT' : 'POST'
  const path = editingId.value ? `${props.endpoint}/${editingId.value}` : props.endpoint
  await request(path, { method, body: { ...form } })
  resetForm()
  await load()
}

async function remove(id: string) {
  if (!confirm('¿Eliminar este registro?')) return
  await request(`${props.endpoint}/${id}`, { method: 'DELETE' })
  await load()
}

onMounted(async () => {
  resetForm()
  await load()
})
</script>

<template>
  <section class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold">{{ title }}</h1>
      <p class="text-sm opacity-60">Catálogo conectado al backend Python.</p>
    </div>

    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>

    <form class="card border border-base-300 bg-base-100" @submit.prevent="save">
      <div class="card-body grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <label v-for="field in fields" :key="field.key" class="form-control">
          <span class="label-text mb-1">{{ field.label }}</span>

          <select v-if="field.type === 'select'" v-model="form[field.key]" class="select select-bordered" :required="field.required">
            <option value="">Selecciona una opción</option>
            <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>

          <input v-else-if="field.type === 'checkbox'" v-model="form[field.key]" type="checkbox" class="toggle toggle-primary" />

          <input v-else v-model="form[field.key]" :type="field.type || 'text'" class="input input-bordered" :required="field.required" />
        </label>

        <div class="md:col-span-2 xl:col-span-3 flex gap-2">
          <button class="btn btn-primary" type="submit">{{ editingId ? 'Actualizar' : 'Guardar' }}</button>
          <button v-if="editingId" class="btn" type="button" @click="resetForm">Cancelar</button>
        </div>
      </div>
    </form>

    <div class="overflow-x-auto rounded-box border border-base-300 bg-base-100">
      <table class="table">
        <thead>
          <tr>
            <th v-for="field in fields" :key="field.key">{{ field.label }}</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td :colspan="fields.length + 1">Cargando…</td></tr>
          <tr v-for="row in rows" :key="row.id">
            <td v-for="field in fields" :key="field.key">{{ row[field.key] }}</td>
            <td class="flex gap-2">
              <button class="btn btn-xs" @click="edit(row)">Editar</button>
              <button class="btn btn-xs btn-error btn-outline" @click="remove(row.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Frontend setup](./09_FRONTEND_NUXT4_SETUP.md) · [Frontend páginas →](./11_FRONTEND_NUXT4_PAGINAS_Y_PRUEBA.md)
