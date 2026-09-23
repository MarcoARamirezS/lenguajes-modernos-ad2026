# AulaPlan AI — Instalación y ejecución

Esta guía concentra los prerrequisitos, comandos de creación y forma de ejecutar el proyecto en **macOS, Linux y Windows PowerShell**.

## Versiones de trabajo

| Herramienta | Versión objetivo |
| --- | --- |
| Node.js | 24 LTS |
| npm | incluida con Node |
| Python | 3.12 |
| Git | versión estable actual |
| Java | JDK 21 |
| Firebase CLI | versión estable actual |

## Verificación

### macOS / Linux

```bash
node --version
npm --version
python3 --version
git --version
java --version
```

### Windows PowerShell

```powershell
node --version
npm --version
py --version
git --version
java --version
```

## Crear raíz del monorepo

### macOS / Linux

```bash
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
npm pkg set private=true --json
npm pkg set "workspaces[0]=apps/web"
mkdir -p apps/api firebase docs .github/workflows
```

### Windows PowerShell

```powershell
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
npm pkg set private=true --json
npm pkg set "workspaces[0]=apps/web"
New-Item -ItemType Directory -Force apps/api
New-Item -ItemType Directory -Force firebase
New-Item -ItemType Directory -Force docs
New-Item -ItemType Directory -Force .github/workflows
```

## Crear Nuxt 4

Desde la raíz:

```bash
npm create nuxt@latest apps/web
```

Seleccionar `npm` como package manager.

## Crear entorno Python

### macOS / Linux

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install "fastapi[standard]"
cd ../..
```

### Windows PowerShell

```powershell
cd apps/api
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install "fastapi[standard]"
cd ../..
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Dependencias backend finales

Archivo `apps/api/requirements.txt`:

```txt
fastapi[standard]
firebase-admin
pydantic-settings
ortools
google-genai
httpx
```

Archivo `apps/api/requirements-dev.txt`:

```txt
-r requirements.txt
pytest
pytest-asyncio
ruff
```

Instalar:

```bash
cd apps/api
pip install -r requirements-dev.txt
```

## Variables de entorno backend

Archivo `apps/api/.env.example`:

```env
APP_NAME=AulaPlan AI API
APP_ENV=development
API_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000
FIREBASE_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/service-account.json
GEMINI_API_KEY=replace-me
GEMINI_MODEL=replace-with-current-free-tier-model
```

Nunca subir `.env` ni el JSON de la cuenta de servicio.

## Variables frontend

`apps/web/.env.example`:

```env
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
NUXT_PUBLIC_FIREBASE_API_KEY=replace-me
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NUXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=replace-me
NUXT_PUBLIC_FIREBASE_APP_ID=replace-me
```

## Ejecutar backend

Terminal 1:

### macOS / Linux

```bash
cd apps/api
source .venv/bin/activate
fastapi dev app/main.py
```

### Windows

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
fastapi dev app/main.py
```

Abrir:

```text
http://127.0.0.1:8000/docs
```

## Ejecutar frontend

Terminal 2, desde raíz:

```bash
npm run dev --workspace apps/web
```

Abrir:

```text
http://localhost:3000
```

## Firebase CLI

```bash
npm install -g firebase-tools
firebase --version
firebase login
```

La inicialización completa se realiza en la sesión 03.

## Git inicial

```bash
git add .
git commit -m "chore: initialize AulaPlan AI monorepo"
git branch -M main
```

Con GitHub CLI:

```bash
gh repo create aulaplan-ai --public --source=. --remote=origin --push
```

Sin GitHub CLI:

```bash
git remote add origin https://github.com/USUARIO/aulaplan-ai.git
git push -u origin main
```

## Diagnóstico rápido

| Síntoma | Revisión |
| --- | --- |
| `python` no existe | usar `python3` o `py -3.12` |
| `fastapi` no existe | activar `.venv` |
| Nuxt no inicia | `npm install` en raíz |
| Firebase CLI no existe | reinstalar `firebase-tools` global |
| Emulator no inicia | verificar JDK 21 |
| CORS | revisar `CORS_ORIGINS` |

## Navegación

- [Mapa](./00_MAPA_DEL_PROYECTO.md)
- [Frontend](./02_FRONTEND_NUXT4_ENTREGA_UNICA.md)
- [Sesión 01](./SESION_01_FOUNDATION_MONOREPO.md)
