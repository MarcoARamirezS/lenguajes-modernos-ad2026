[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Frontend base](./10_FRONTEND_NUXT4_CODIGO_COMPLETO.md) · [Mapa backend →](./12_MAPA_SESIONES_BACKEND.md)

# 11 — Frontend Nuxt 4: páginas y prueba

### `apps/web/app/pages/index.vue`

```vue
<script setup lang="ts">
await navigateTo('/dashboard')
</script>

<template><div /></template>
```
### `apps/web/app/pages/login.vue`

```vue
<script setup lang="ts">
definePageMeta({ layout: 'auth' })
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const { login } = useAuth()

async function submit() {
  loading.value = true
  errorMessage.value = ''
  try {
    await login(email.value, password.value)
    await navigateTo('/dashboard')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No fue posible iniciar sesión.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="card border border-base-300 bg-base-100 shadow-xl" @submit.prevent="submit">
    <div class="card-body">
      <h1 class="card-title text-2xl">AulaPlan AI</h1>
      <p class="text-sm opacity-60">Acceso al generador inteligente de horarios.</p>
      <div v-if="errorMessage" class="alert alert-error text-sm">{{ errorMessage }}</div>
      <label class="form-control">
        <span class="label-text mb-1">Correo</span>
        <input v-model="email" type="email" class="input input-bordered" required />
      </label>
      <label class="form-control">
        <span class="label-text mb-1">Contraseña</span>
        <input v-model="password" type="password" class="input input-bordered" required />
      </label>
      <button class="btn btn-primary mt-2" :disabled="loading">{{ loading ? 'Entrando…' : 'Entrar' }}</button>
    </div>
  </form>
</template>
```
### `apps/web/app/pages/dashboard.vue`

```vue
<script setup lang="ts">
const cards = [
  ['Profesores', '—', 'Carga desde Firestore'],
  ['Materias', '—', 'Catálogo académico'],
  ['Grupos', '—', 'Grupos activos'],
  ['Horarios', '—', 'Versiones generadas'],
]
</script>

<template>
  <section class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold">Dashboard</h1>
      <p class="opacity-60">Resumen operativo de AulaPlan AI.</p>
    </div>
    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard v-for="card in cards" :key="card[0]" :title="card[0]" :value="card[1]" :description="card[2]" />
    </div>
    <div class="card border border-base-300 bg-base-100">
      <div class="card-body">
        <h2 class="card-title">Flujo recomendado</h2>
        <ol class="list-decimal space-y-2 pl-6">
          <li>Captura catálogos y periodo académico.</li>
          <li>Define ofertas, disponibilidad y restricciones.</li>
          <li>Genera un horario y revisa el score.</li>
          <li>Publica una versión cuando sea aprobada.</li>
        </ol>
      </div>
    </div>
  </section>
</template>
```
### `apps/web/app/pages/academic-periods.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'code', label: 'Código', type: 'text', required: true },\n  { key: 'name', label: 'Nombre', type: 'text', required: true },\n  { key: 'start_date', label: 'Inicio', type: 'text', required: true },\n  { key: 'end_date', label: 'Fin', type: 'text', required: true },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Periodos académicos" endpoint="/academic-periods" :fields="fields" />
</template>
```
### `apps/web/app/pages/teachers.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'code', label: 'Código', type: 'text', required: true },\n  { key: 'name', label: 'Nombre', type: 'text', required: true },\n  { key: 'email', label: 'Correo', type: 'email', required: true },\n  { key: 'max_daily_blocks', label: 'Máx. bloques/día', type: 'number', required: true },\n  { key: 'max_weekly_blocks', label: 'Máx. bloques/semana', type: 'number', required: true },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Profesores" endpoint="/teachers" :fields="fields" />
</template>
```
### `apps/web/app/pages/subjects.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'code', label: 'Código', type: 'text', required: true },\n  { key: 'name', label: 'Nombre', type: 'text', required: true },\n  { key: 'weekly_blocks', label: 'Bloques/semana', type: 'number', required: true },\n  { key: 'required_room_type', label: 'Tipo de salón', type: 'text', required: true },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Materias" endpoint="/subjects" :fields="fields" />
</template>
```
### `apps/web/app/pages/groups.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'code', label: 'Código', type: 'text', required: true },\n  { key: 'name', label: 'Nombre', type: 'text', required: true },\n  { key: 'student_count', label: 'Alumnos', type: 'number', required: true },\n  { key: 'academic_period_id', label: 'ID periodo', type: 'text', required: true },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Grupos" endpoint="/groups" :fields="fields" />
</template>
```
### `apps/web/app/pages/rooms.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'code', label: 'Código', type: 'text', required: true },\n  { key: 'name', label: 'Nombre', type: 'text', required: true },\n  { key: 'capacity', label: 'Capacidad', type: 'number', required: true },\n  { key: 'type', label: 'Tipo', type: 'text', required: true },\n  { key: 'building', label: 'Edificio', type: 'text', required: false },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Salones" endpoint="/rooms" :fields="fields" />
</template>
```
### `apps/web/app/pages/time-blocks.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'day', label: 'Día', type: 'text', required: true },\n  { key: 'start_time', label: 'Inicio', type: 'text', required: true },\n  { key: 'end_time', label: 'Fin', type: 'text', required: true },\n  { key: 'order', label: 'Orden', type: 'number', required: true },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Bloques horarios" endpoint="/time-blocks" :fields="fields" />
</template>
```
### `apps/web/app/pages/offerings.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'academic_period_id', label: 'ID periodo', type: 'text', required: true },\n  { key: 'subject_id', label: 'ID materia', type: 'text', required: true },\n  { key: 'group_id', label: 'ID grupo', type: 'text', required: true },\n  { key: 'teacher_id', label: 'ID profesor', type: 'text', required: true },\n  { key: 'active', label: 'Activo', type: 'checkbox', required: false, defaultValue: true }
]
</script>

<template>
  <CatalogManager title="Ofertas académicas" endpoint="/offerings" :fields="fields" />
</template>
```
### `apps/web/app/pages/availability.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'

const fields: CatalogField[] = [
  { key: 'teacher_id', label: 'ID profesor', type: 'text', required: true },\n  { key: 'time_block_id', label: 'ID bloque', type: 'text', required: true },\n  { key: 'available', label: 'Disponible', type: 'checkbox', required: false, defaultValue: true },\n  { key: 'preference_weight', label: 'Preferencia', type: 'number', required: false }
]
</script>

<template>
  <CatalogManager title="Disponibilidad docente" endpoint="/availability" :fields="fields" />
</template>
```
### `apps/web/app/pages/constraints.vue`

```vue
<script setup lang="ts">
import type { CatalogField } from '~/types'
const { request } = useApi()
const naturalText = ref('')
const parsed = ref<unknown>(null)
const fields: CatalogField[] = [
  { key: 'type', label: 'Tipo', required: true },
  { key: 'priority', label: 'Prioridad', required: true },
  { key: 'target_type', label: 'Tipo objetivo', required: true },
  { key: 'target_id', label: 'ID objetivo', required: true },
  { key: 'weight', label: 'Peso', type: 'number', defaultValue: 0 },
  { key: 'active', label: 'Activo', type: 'checkbox', defaultValue: true },
]
async function parseText() {
  parsed.value = await request('/ai/constraints/parse', {
    method: 'POST', body: { text: naturalText.value },
  })
}
</script>

<template>
  <section class="space-y-8">
    <CatalogManager title="Restricciones" endpoint="/constraints" :fields="fields" />
    <div class="card border border-base-300 bg-base-100">
      <div class="card-body">
        <h2 class="card-title">Interpretar con Gemini</h2>
        <textarea v-model="naturalText" class="textarea textarea-bordered min-h-32" placeholder="Ej. Marco no puede dar clases los martes..." />
        <button class="btn btn-secondary w-fit" @click="parseText">Interpretar</button>
        <pre v-if="parsed" class="overflow-auto rounded bg-base-200 p-4 text-xs">{{ JSON.stringify(parsed, null, 2) }}</pre>
      </div>
    </div>
  </section>
</template>
```
### `apps/web/app/pages/generator.vue`

```vue
<script setup lang="ts">
const { request } = useApi()
const periodId = ref('')
const maxNodes = ref(50000)
const result = ref<unknown>(null)
const loading = ref(false)
async function generate() {
  loading.value = true
  try {
    result.value = await request('/schedules/generate', {
      method: 'POST',
      body: { academic_period_id: periodId.value, max_nodes: maxNodes.value },
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="space-y-6">
    <div><h1 class="text-3xl font-bold">Generador de horarios</h1><p class="opacity-60">Ejecuta el scheduler Python.</p></div>
    <div class="card border border-base-300 bg-base-100">
      <div class="card-body max-w-2xl">
        <label class="form-control"><span class="label-text mb-1">ID periodo académico</span><input v-model="periodId" class="input input-bordered" /></label>
        <label class="form-control"><span class="label-text mb-1">Máximo de nodos</span><input v-model="maxNodes" type="number" class="input input-bordered" /></label>
        <button class="btn btn-primary w-fit" :disabled="loading || !periodId" @click="generate">{{ loading ? 'Generando…' : 'Generar horario' }}</button>
      </div>
    </div>
    <pre v-if="result" class="overflow-auto rounded-box bg-neutral p-4 text-xs text-neutral-content">{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>
```
### `apps/web/app/pages/schedules.vue`

```vue
<script setup lang="ts">
const { request } = useApi()
const rows = ref<any[]>([])
onMounted(async () => { rows.value = await request<any[]>('/schedules') })
async function publish(id: string) {
  await request(`/schedules/${id}/publish`, { method: 'POST' })
  rows.value = await request<any[]>('/schedules')
}
</script>

<template>
  <section class="space-y-6">
    <div><h1 class="text-3xl font-bold">Horarios</h1><p class="opacity-60">Versiones generadas y publicadas.</p></div>
    <div class="overflow-x-auto rounded-box border border-base-300 bg-base-100">
      <table class="table"><thead><tr><th>ID</th><th>Periodo</th><th>Estado</th><th>Score</th><th></th></tr></thead>
        <tbody><tr v-for="row in rows" :key="row.id"><td class="font-mono text-xs">{{ row.id }}</td><td>{{ row.academic_period_id }}</td><td>{{ row.status }}</td><td>{{ row.score }}</td><td><button v-if="row.status !== 'PUBLISHED'" class="btn btn-xs btn-primary" @click="publish(row.id)">Publicar</button></td></tr></tbody>
      </table>
    </div>
  </section>
</template>
```
### `apps/web/app/pages/users.vue`

```vue
<script setup lang="ts">
const { request } = useApi()
const users = ref<any[]>([])
onMounted(async () => { users.value = await request<any[]>('/users') })
</script>

<template>
  <section class="space-y-6">
    <div><h1 class="text-3xl font-bold">Usuarios</h1><p class="opacity-60">Solo ADMIN puede consultar esta vista.</p></div>
    <div class="overflow-x-auto rounded-box border border-base-300 bg-base-100">
      <table class="table"><thead><tr><th>Correo</th><th>Nombre</th><th>Rol</th><th>Activo</th></tr></thead>
        <tbody><tr v-for="user in users" :key="user.uid"><td>{{ user.email }}</td><td>{{ user.display_name }}</td><td>{{ user.role }}</td><td>{{ user.active }}</td></tr></tbody>
      </table>
    </div>
  </section>
</template>
```

## Ejecutar

```bash
npm run dev:web
```

Abre `http://localhost:3000`. Mientras el backend aún no exista, las vistas protegidas requerirán terminar Firebase Auth en las sesiones correspondientes.

## Verificación estática

```bash
npm run typecheck:web
npm run generate:web
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Frontend base](./10_FRONTEND_NUXT4_CODIGO_COMPLETO.md) · [Mapa backend →](./12_MAPA_SESIONES_BACKEND.md)
