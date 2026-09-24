[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Checklist global](./09_CHECKLIST_GLOBAL.md) · [Sesión 02 →](./SESION_02_BACKEND_PYTHON_ARQUITECTURA.md)

# Sesión 01 — Foundation: monorepo + Python + Nuxt + Firebase

**Duración:** 1 hora 30 minutos.

## Objetivo

Crear el proyecto desde cero y dejar frontend y entorno backend listos.

## Distribución de tiempo

```text
00–15  Arquitectura
15–35  Monorepo
35–55  Nuxt
55–75  Python virtualenv
75–85  Firebase/Netlify CLI
85–90  Git
```


## Estructura inicial

```text
aulaplan-ai/
├── apps/
│   ├── web/
│   └── api/
├── firebase/
├── docs/
├── firebase.json
├── netlify.toml
└── package.json
```

## Raíz

```json
{
  "name": "aulaplan-ai",
  "private": true,
  "workspaces": [
    "apps/web"
  ],
  "scripts": {
    "dev:web": "npm run dev --workspace apps/web",
    "build:web": "npm run build --workspace apps/web",
    "generate:web": "npm run generate --workspace apps/web"
  }
}
```

## Backend Python

Crear `apps/api/.python-version`:

```text
3.11
```

Crear `requirements.txt`:

```text
firebase-functions
firebase-admin
Flask
pydantic
google-genai
```

## Primer commit

```bash
git add .
git commit -m "chore: initialize AulaPlan AI monorepo"
```


## Cierre verificable

- [ ] `npm run dev:web` inicia Nuxt.
- [ ] `.venv` activa correctamente.
- [ ] `python --version` muestra 3.11.x.
- [ ] Firebase CLI responde.
- [ ] Primer commit creado.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Checklist global](./09_CHECKLIST_GLOBAL.md) · [Sesión 02 →](./SESION_02_BACKEND_PYTHON_ARQUITECTURA.md)
