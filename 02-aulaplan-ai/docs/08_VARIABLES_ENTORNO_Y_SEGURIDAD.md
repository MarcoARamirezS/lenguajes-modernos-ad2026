[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Arquitectura](./07_ARQUITECTURA_PYTHON_FIREBASE_NETLIFY.md) · [Checklist global →](./09_CHECKLIST_GLOBAL.md)

# 08 — Variables de entorno y seguridad

## Frontend

`.env.example`:

```env
NUXT_PUBLIC_API_BASE_URL=/api
NUXT_PUBLIC_FIREBASE_API_KEY=
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NUXT_PUBLIC_FIREBASE_PROJECT_ID=
```

Las variables `NUXT_PUBLIC_*` son visibles al navegador. No colocar secretos.

## Backend Python

No subir JSON de service accounts.

En Firebase Functions se utilizan credenciales del entorno administrado mediante Application Default Credentials.

Para Gemini usa Secret Manager / parámetros de Functions según la configuración del proyecto.

## Local

Puedes usar:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/service-account.json"
```

solo en desarrollo y fuera del repositorio.

## Gitignore mínimo

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
serviceAccount*.json
node_modules/
.firebase/
.output/
```

## Reglas

- validar Firebase ID token en backend;
- no confiar en roles enviados por frontend;
- validar payloads con Pydantic;
- registrar errores sin secretos;
- no devolver stack traces en producción.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Arquitectura](./07_ARQUITECTURA_PYTHON_FIREBASE_NETLIFY.md) · [Checklist global →](./09_CHECKLIST_GLOBAL.md)
