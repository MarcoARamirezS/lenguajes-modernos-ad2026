[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Creación monorepo](./06_CREACION_MONOREPO.md) · [GitHub →](./08_GITHUB_SETUP.md)

# 07 — Configuración de Firebase

## Crear proyecto

1. Abre Firebase Console.
2. Crea un proyecto, por ejemplo `aulaplan-ai-ad2026`.
3. Activa Authentication → Email/Password.
4. Crea Firestore.
5. Registra una aplicación Web para obtener la configuración pública del frontend.

## Login CLI

```bash
firebase login
firebase projects:list
```

## Asociar proyecto

```bash
firebase use --add
```

## Inicializar

```bash
firebase init functions firestore emulators
```

Para Functions selecciona Python. La guía reemplazará la configuración generada por la versión de monorepo siguiente.

### `firebase.json`

```json
{
  "functions": [
    {
      "source": "apps/api",
      "codebase": "aulaplan-api",
      "runtime": "python311",
      "ignore": [".venv", "venv", "__pycache__", "*.pyc", ".git"]
    }
  ],
  "firestore": {
    "rules": "firebase/firestore.rules",
    "indexes": "firebase/firestore.indexes.json"
  },
  "emulators": {
    "auth": { "port": 9099 },
    "functions": { "port": 5001 },
    "firestore": { "port": 8080 },
    "ui": { "enabled": true, "port": 4000 }
  }
}
```
### `firebase/firestore.rules`

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

## Emuladores

```bash
firebase emulators:start
```

Puertos del curso:

- Auth: `9099`
- Functions: `5001`
- Firestore: `8080`
- Emulator UI: `4000`

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Creación monorepo](./06_CREACION_MONOREPO.md) · [GitHub →](./08_GITHUB_SETUP.md)
