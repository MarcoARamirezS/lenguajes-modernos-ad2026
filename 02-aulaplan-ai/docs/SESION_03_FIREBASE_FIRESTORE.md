# 03 — Firebase Authentication, Firestore y Emulators

**Duración:** 1 hora 30 minutos.

## Objetivo

Crear el proyecto Firebase, inicializar emuladores y conectar Firebase Admin desde Netlify Functions sin incluir credenciales en el repositorio.

## Distribución de tiempo

- **00–20 min** — Firebase project
- **20–40 min** — CLI y emulators
- **40–60 min** — Admin SDK
- **60–75 min** — Firestore repository
- **75–90 min** — Smoke test

## Conceptos

- Firebase project
- Admin SDK
- Application credentials
- Firestore
- Auth Emulator
- Firestore Emulator

## Desarrollo

### 1. Instalar Admin SDK

```bash
npm install --workspace apps/api firebase-admin
```

### 2. Firebase CLI

```bash
npx firebase login
npx firebase init firestore emulators
```
Seleccionar Auth y Firestore emulators cuando se solicite.

### 3. Variables locales macOS/Linux

```bash
export FIREBASE_PROJECT_ID="demo-aulaplan"
```

### 4. Variables locales Windows PowerShell

```powershell
$env:FIREBASE_PROJECT_ID="demo-aulaplan"
```

### 5. Inicialización segura

Crear un módulo singleton de Firebase Admin. En producción usar `FIREBASE_PROJECT_ID`, `FIREBASE_CLIENT_EMAIL` y `FIREBASE_PRIVATE_KEY`; en emuladores apuntar a hosts locales. Nunca versionar service-account JSON.

### 6. Repository base

Crear utilidades para timestamps, creación de documentos, lectura por ID y manejo consistente de `not found`.

### 7. Smoke test

Crear/leer un documento de prueba contra el emulador y eliminarlo al terminar.

## Endpoints al cierre

- `GET /api/health`
- `GET /api/info`

## Checklist de cierre

- [ ] Firebase Emulator UI abre
- [ ] Firestore Emulator responde
- [ ] Admin SDK inicializa una sola vez
- [ ] No hay credenciales reales en Git
- [ ] Smoke test de Firestore en verde

## Commit sugerido

```bash
git add .
git commit -m "feat: integrate Firebase Admin and emulators"
```

## Archivos de Firebase

### `firebase/firebase.json`

```json
{
  "firestore": {
    "rules": "firestore.rules",
    "indexes": "firestore.indexes.json"
  },
  "emulators": {
    "auth": { "port": 9099 },
    "firestore": { "port": 8080 },
    "ui": { "enabled": true, "port": 4000 }
  }
}
```

### `firebase/firestore.rules`

La lógica de negocio de AulaPlan pasa por Firebase Admin. Para el cliente se empieza con reglas cerradas y se abren únicamente los casos que realmente se necesiten:

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

### `firebase/firestore.indexes.json`

```json
{
  "indexes": [],
  "fieldOverrides": []
}
```

### `apps/api/.env.example`

```env
APP_ENV=local
FIREBASE_PROJECT_ID=demo-aulaplan
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=
FIRESTORE_EMULATOR_HOST=127.0.0.1:8080
FIREBASE_AUTH_EMULATOR_HOST=127.0.0.1:9099
GEMINI_API_KEY=
GEMINI_MODEL=
MAX_SOLVER_MS=8000
```

### `apps/api/src/firebase/admin.ts`

```ts
import { cert, getApps, initializeApp } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'
import { getFirestore } from 'firebase-admin/firestore'

const projectId = process.env.FIREBASE_PROJECT_ID

if (!projectId) {
  throw new Error('FIREBASE_PROJECT_ID is required')
}

const usingEmulators = Boolean(
  process.env.FIRESTORE_EMULATOR_HOST ||
  process.env.FIREBASE_AUTH_EMULATOR_HOST
)

function createApp() {
  if (usingEmulators) {
    return initializeApp({ projectId })
  }

  const clientEmail = process.env.FIREBASE_CLIENT_EMAIL
  const privateKey = process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n')

  if (!clientEmail || !privateKey) {
    throw new Error('Firebase Admin credentials are missing')
  }

  return initializeApp({
    projectId,
    credential: cert({
      projectId,
      clientEmail,
      privateKey
    })
  })
}

export const firebaseApp = getApps()[0] ?? createApp()
export const db = getFirestore(firebaseApp)
export const auth = getAuth(firebaseApp)
```

### `apps/api/src/repositories/firestore.repository.ts`

```ts
import { db } from '../firebase/admin'
import { AppError } from '../core/errors'

type Entity = Record<string, unknown>

export function firestoreRepository<T extends Entity>(collectionName: string) {
  const collection = db.collection(collectionName)

  return {
    async list(): Promise<Array<T & { id: string }>> {
      const snapshot = await collection.get()
      return snapshot.docs.map(doc => ({
        id: doc.id,
        ...(doc.data() as T)
      }))
    },

    async getById(id: string): Promise<T & { id: string }> {
      const doc = await collection.doc(id).get()

      if (!doc.exists) {
        throw new AppError(404, 'NOT_FOUND', `${collectionName} resource not found`)
      }

      return {
        id: doc.id,
        ...(doc.data() as T)
      }
    },

    async create(data: T): Promise<T & { id: string }> {
      const now = new Date().toISOString()
      const ref = collection.doc()
      const payload = {
        ...data,
        createdAt: now,
        updatedAt: now
      }

      await ref.set(payload)

      return {
        id: ref.id,
        ...payload
      } as T & { id: string }
    },

    async update(id: string, data: Partial<T>) {
      const ref = collection.doc(id)
      const current = await ref.get()

      if (!current.exists) {
        throw new AppError(404, 'NOT_FOUND', `${collectionName} resource not found`)
      }

      await ref.update({
        ...data,
        updatedAt: new Date().toISOString()
      })

      return this.getById(id)
    },

    async remove(id: string) {
      await this.getById(id)
      await collection.doc(id).delete()
    }
  }
}
```

## Ejecutar emuladores y Netlify

Terminal 1:

```bash
npx firebase emulators:start --config firebase/firebase.json
```

Terminal 2:

```bash
npx netlify dev
```

[Volver al índice](./README.md)
