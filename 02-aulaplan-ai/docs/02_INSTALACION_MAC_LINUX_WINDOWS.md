[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Mapa del proyecto](./01_MAPA_DEL_PROYECTO.md) · [Frontend Nuxt 4 →](./03_FRONTEND_NUXT4_ENTREGA_UNICA.md)

# 02 — Instalación macOS, Linux y Windows

## Versiones objetivo

```text
Node.js 24 LTS
Python 3.11
Java 21
Git
Firebase CLI
Netlify CLI
```

## Verificación

### macOS / Linux

```bash
node --version
npm --version
python3 --version
git --version
java --version
firebase --version
netlify --version
```

### Windows PowerShell

```powershell
node --version
npm --version
py -3.11 --version
git --version
java --version
firebase --version
netlify --version
```

## Crear directorios

### macOS / Linux

```bash
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
npm pkg set private=true --json
npm pkg set "workspaces[0]=apps/web"
mkdir -p apps/api/src apps/api/tests firebase docs
```

### Windows PowerShell

```powershell
mkdir aulaplan-ai
cd aulaplan-ai
git init
npm init -y
npm pkg set private=true --json
npm pkg set "workspaces[0]=apps/web"
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

### macOS / Linux

```bash
cd apps/api
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Windows PowerShell

```powershell
cd apps/api
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## Dependencias Python

```bash
pip install firebase-functions firebase-admin Flask pydantic google-genai pytest
pip freeze > requirements.txt
```

## CLI

```bash
npm install -g firebase-tools netlify-cli
firebase login
netlify login
```

## Java

Firebase Emulator Suite necesita Java. Para un curso nuevo usa JDK 21.

## No hacer commit

```text
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
node_modules/
serviceAccount*.json
.firebase/
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Mapa del proyecto](./01_MAPA_DEL_PROYECTO.md) · [Frontend Nuxt 4 →](./03_FRONTEND_NUXT4_ENTREGA_UNICA.md)
