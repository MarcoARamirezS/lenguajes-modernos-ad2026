[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Seguridad](./92_VARIABLES_SEGURIDAD.md) · [Código final →](./94_ANEXO_BACKEND_FINAL.md)

# 93 — Comandos rápidos

## Frontend

```bash
npm run dev:web
npm run typecheck:web
npm run generate:web
```

## Backend macOS/Linux

```bash
cd apps/api
source .venv/bin/activate
PYTHONPATH=. pytest tests -q
```

## Backend Windows

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH="."
pytest tests -q
```

## Firebase

```bash
firebase login
firebase use
firebase emulators:start
firebase deploy --only functions
firebase deploy --only firestore
```

## Secret

```bash
firebase functions:secrets:set GEMINI_API_KEY
```

## Git

```bash
git status
git add .
git commit -m "mensaje"
git push
```

## Crear `.venv`

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Seguridad](./92_VARIABLES_SEGURIDAD.md) · [Código final →](./94_ANEXO_BACKEND_FINAL.md)
