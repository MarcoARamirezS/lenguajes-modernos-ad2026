# 01 — Instalación y ejecución

## Versiones de trabajo

- Node.js: **24 LTS**.
- npm: incluido con Node.
- Git: versión estable actual.
- Firebase CLI: dependencia de desarrollo del monorepo.
- Netlify CLI: dependencia de desarrollo del monorepo.

## Verificar herramientas

### macOS / Linux

```bash
node --version
npm --version
git --version
```

### Windows PowerShell

```powershell
node --version
npm --version
git --version
```

## Crear carpeta

### macOS / Linux

```bash
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
mkdir -p apps/web apps/api/netlify/functions apps/api/src packages/contracts/src firebase docs .github/workflows
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force aulaplan-ai | Out-Null
Set-Location aulaplan-ai
git init
npm init -y
New-Item -ItemType Directory -Force apps/web | Out-Null
New-Item -ItemType Directory -Force apps/api/netlify/functions | Out-Null
New-Item -ItemType Directory -Force apps/api/src | Out-Null
New-Item -ItemType Directory -Force packages/contracts/src | Out-Null
New-Item -ItemType Directory -Force firebase | Out-Null
New-Item -ItemType Directory -Force docs | Out-Null
New-Item -ItemType Directory -Force .github/workflows | Out-Null
```

## Configurar workspaces

Desde la raíz:

```bash
npm pkg set private=true --json
npm pkg set "workspaces[0]=apps/*" "workspaces[1]=packages/*"
```

## Crear Nuxt 4

```bash
npm create nuxt@latest apps/web
```

Seleccionar `npm` como package manager.

## Crear paquetes backend

```bash
cd apps/api
npm init -y
cd ../..

cd packages/contracts
npm init -y
cd ../..
```

## Dependencias del backend serverless

```bash
npm install --workspace apps/api @netlify/functions firebase-admin zod @google/genai
npm install --workspace apps/api -D typescript vitest @types/node
```

## Dependencias frontend

```bash
npm install --workspace apps/web @pinia/nuxt pinia firebase
npm install --workspace apps/web -D tailwindcss @tailwindcss/vite daisyui
```

## Herramientas de proyecto

```bash
npm install -D netlify-cli firebase-tools concurrently
```

## Ejecución recomendada

La ejecución integrada debe realizarse desde raíz:

```bash
npx netlify dev
```

URL esperada:

```text
http://localhost:8888
```

API:

```text
http://localhost:8888/api/health
```

## Firebase Emulators

Después de inicializar Firebase:

```bash
npx firebase emulators:start
```

Puertos recomendados:

- Emulator UI: `4000`.
- Auth: `9099`.
- Firestore: `8080`.

## Comandos de validación

```bash
npm run typecheck
npm run lint
npm run test
npm run generate:web
```

## Regla

Durante el curso no se ejecutará un segundo backend en otro proveedor. La API existe como Netlify Functions dentro del mismo monorepo.

## Configuración reproducible de la raíz

Después de crear los workspaces, ejecutar:

```bash
npm pkg set name="aulaplan-ai"
npm pkg set scripts.dev="netlify dev"
npm pkg set scripts.dev:web="npm run dev --workspace @aulaplan/web"
npm pkg set scripts.generate:web="npm run generate --workspace @aulaplan/web"
npm pkg set scripts.typecheck="npm run typecheck --workspace @aulaplan/api && npm run typecheck --workspace @aulaplan/web"
npm pkg set scripts.test="npm run test --workspace @aulaplan/api"
```

En `apps/web/package.json` ajustar el nombre:

```bash
npm pkg set name="@aulaplan/web" --workspace apps/web
```

En `apps/api/package.json`:

```bash
npm pkg set name="@aulaplan/api" --workspace apps/api
npm pkg set private=true --json --workspace apps/api
npm pkg set type="module" --workspace apps/api
npm pkg set scripts.typecheck="tsc --noEmit" --workspace apps/api
npm pkg set scripts.test="vitest run" --workspace apps/api
npm pkg set scripts.test:watch="vitest" --workspace apps/api
```

En `packages/contracts/package.json`:

```bash
npm pkg set name="@aulaplan/contracts" --workspace packages/contracts
npm pkg set private=true --json --workspace packages/contracts
npm pkg set type="module" --workspace packages/contracts
```

## `.nvmrc`

Archivo raíz:

```text
24
```

## `netlify.toml`

Archivo raíz:

```toml
[build]
  command = "npm run generate:web"
  publish = "apps/web/.output/public"
  functions = "apps/api/netlify/functions"

[build.environment]
  NODE_VERSION = "24"

[dev]
  command = "npm run dev:web"
  targetPort = 3000
  port = 8888
  autoLaunch = false

[functions]
  node_bundler = "esbuild"
```

## `apps/api/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["src/**/*.ts", "netlify/functions/**/*.mts", "tests/**/*.ts"]
}
```

## `.gitignore` mínimo

```gitignore
node_modules/
.nuxt/
.output/
.netlify/
coverage/
.env
.env.*
!.env.example
service-account*.json
firebase-adminsdk*.json
.DS_Store
```
