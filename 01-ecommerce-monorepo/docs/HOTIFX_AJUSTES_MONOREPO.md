[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_07_TESTING_OPENAPI_CIERRE.md](./SESION_07_TESTING_OPENAPI_CIERRE.md) · [Proyecto →](../README.md)

# Ajustes Mono - Repo

Para poder trabajar todo como un monorepo debes de realizar los siguientes ajuste, primero borrar todas las carpetas 'node_modules' y archivos package-lock.json de tu proyecto

## Sustituir package.json de raiz

En raíz debes de sustituir el package.json con el siguiente codigo

```bash
{
  "name": "ecommerce-monorepo",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "workspaces": [
    "apps/api",
    "apps/web"
  ],
  "scripts": {
    "dev": "concurrently --kill-others --names API,WEB \"npm run dev:api\" \"npm run dev:web\"",
    "dev:api": "npm run dev --workspace=@ecommerce/api",
    "dev:web": "npm run dev --workspace=@ecommerce/web",

    "start:api": "npm run start --workspace=@ecommerce/api",

    "build": "npm run build:web",
    "build:web": "npm run build --workspace=@ecommerce/web",
    "generate:web": "npm run generate --workspace=@ecommerce/web",
    "preview:web": "npm run preview --workspace=@ecommerce/web",

    "lint": "npm run lint --workspaces",
    "lint:api": "npm run lint --workspace=@ecommerce/api",
    "lint:web": "npm run lint --workspace=@ecommerce/web",

    "typecheck": "npm run typecheck:web",
    "typecheck:web": "npm run typecheck --workspace=@ecommerce/web",

    "test": "npm run test --workspaces",
    "test:api": "npm run test --workspace=@ecommerce/api",
    "test:web": "npm run test --workspace=@ecommerce/web",
    "test:e2e:web": "npm run test:e2e --workspace=@ecommerce/web",

    "check": "npm run lint && npm run typecheck"
  },
  "devDependencies": {
    "concurrently": "^9.2.1"
  },
  "engines": {
    "node": ">=24.0.0"
  }
}
```

---

## Sustituir los package.json de web y api

### Package.json WEB

```bash
{
  "name": "@ecommerce/web",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "nuxt dev --port 3000",
    "build": "nuxt build",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "typecheck": "nuxt typecheck",
    "lint": "eslint .",
    "test": "vitest run",
    "test:e2e": "playwright test"
  },
  "dependencies": {
    "@nuxt/eslint": "^1.9.0",
    "@nuxt/icon": "^2.0.0",
    "@pinia/nuxt": "^0.11.2",
    "@tailwindcss/vite": "^4.1.17",
    "nuxt": "4.5.2",
    "pinia": "^3.0.4",
    "tailwindcss": "^4.1.17"
  },
  "devDependencies": {
    "@playwright/test": "^1.56.1",
    "typescript": "^5.9.3",
    "vitest": "^4.0.14",
    "vue-tsc": "^3.1.5"
  }
}
```

### Package.json API

```bash
{
  "name": "@ecommerce/api",
  "version": "1.0.0",
  "description": "Api del E-Commerce",
  "main": "src/server.js",
  "private": true,
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "dev": "nodemon src/server.js",
    "start": "node src/server.js",
    "lint": "eslint src"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "type": "module",
  "engines": {
    "node": ">=24"
  },
  "dependencies": {
    "bcryptjs": "^3.0.3",
    "cors": "^2.8.6",
    "dotenv": "^17.4.2",
    "express": "^5.2.1",
    "firebase-admin": "^14.3.0",
    "helmet": "^8.3.0",
    "jsonwebtoken": "^9.0.3",
    "pino": "^10.3.1",
    "pino-http": "^11.0.0",
    "zod": "^4.4.3"
  },
  "devDependencies": {
    "@eslint/js": "^10.0.1",
    "eslint": "^10.8.1",
    "globals": "^17.11.0",
    "nodemon": "^3.1.14",
    "pino-pretty": "^13.1.3"
  }
}

```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_07_TESTING_OPENAPI_CIERRE.md](./SESION_07_TESTING_OPENAPI_CIERRE.md) · [Proyecto →](../README.md)
