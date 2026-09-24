[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación Windows](./05_INSTALACION_WINDOWS.md) · [Firebase →](./07_FIREBASE_SETUP.md)

# 06 — Creación del monorepo

## macOS/Linux

```bash
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
npm pkg set private=true --json
npm pkg set 'workspaces[0]=apps/web'
mkdir -p apps/api/src apps/api/tests firebase docs
```

## Windows PowerShell

```powershell
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
npm pkg set private=true --json
npm pkg set 'workspaces[0]=apps/web'
New-Item -ItemType Directory -Force apps/api/src
New-Item -ItemType Directory -Force apps/api/tests
New-Item -ItemType Directory -Force firebase
New-Item -ItemType Directory -Force docs
```

## Crear Nuxt

```bash
npm create nuxt@latest apps/web
```

Selecciona `npm`.

## Crear entorno Python

### macOS/Linux

```bash
cd apps/api
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

### Windows

```powershell
cd apps/api
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

La salida debe ser `Python 3.11.x`.

## Dependencias backend iniciales

```bash
python -m pip install --upgrade pip
pip install firebase-functions firebase-admin Flask 'pydantic[email]' google-genai pytest
pip freeze > requirements.txt
```

## Raíz del proyecto

### `package.json`

```json
{
  "name": "aulaplan-ai",
  "private": true,
  "workspaces": ["apps/web"],
  "scripts": {
    "dev:web": "npm run dev --workspace apps/web",
    "generate:web": "npm run generate --workspace apps/web",
    "typecheck:web": "npm run typecheck --workspace apps/web",
    "dev:firebase": "firebase emulators:start",
    "dev": "concurrently -n WEB,FIREBASE -c auto \"npm:dev:web\" \"npm:dev:firebase\""
  },
  "devDependencies": {
    "concurrently": "^9.2.1"
  }
}
```
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

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación Windows](./05_INSTALACION_WINDOWS.md) · [Firebase →](./07_FIREBASE_SETUP.md)
