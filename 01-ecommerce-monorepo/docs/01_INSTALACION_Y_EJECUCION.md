[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← 00_MAPA_DEL_PROYECTO.md](./00_MAPA_DEL_PROYECTO.md) · [02_FRONTEND_NUXT4_GUIA.md →](./02_FRONTEND_NUXT4_GUIA.md)

# Instalación y Ejecución del Monorepo

Esta guía explica cómo instalar y ejecutar el proyecto completo.

## Prerrequisitos

Antes de iniciar, instalar:

- Node.js LTS 24 o superior.
- npm.
- Git.
- Visual Studio Code.
- Cuenta de Firebase.
- Proyecto de Firebase con Firestore habilitado.

Verificar versiones:

```bash
node --version
npm --version
git --version
```

## Estructura esperada

```text
ecommerce-monorepo/
├── package.json
├── .gitignore
└── apps/
    ├── api/
    └── web/
```

## `package.json` raíz

El archivo raíz debe incluir:

```json
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
    "dev:api": "npm run dev --workspace=@ecommerce/api",
    "dev:web": "npm run dev --workspace=@ecommerce/web",
    "build:web": "npm run build --workspace=@ecommerce/web",
    "typecheck:web": "npm run typecheck --workspace=@ecommerce/web",
    "lint:web": "npm run lint --workspace=@ecommerce/web",
    "test:api": "npm run test --workspace=@ecommerce/api",
    "test:e2e:web": "npm run test:e2e --workspace=@ecommerce/web"
  },
  "engines": {
    "node": ">=24.0.0"
  }
}
```

## `.gitignore` recomendado

Archivo:

```text
.gitignore
```

Contenido:

```gitignore
node_modules/
.nuxt/
.output/
dist/
coverage/
playwright-report/
test-results/
.env
.env.*
!.env.example
.DS_Store
npm-debug.log*
```

## Instalar dependencias

Desde la raíz del monorepo:

```bash
npm install
```

## Variables de entorno del backend

Archivo:

```text
apps/api/.env
```

Contenido esperado:

```env
PORT=4050
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
JWT_ACCESS_SECRET=change-this-access-secret
JWT_REFRESH_SECRET=change-this-refresh-secret
JWT_ACCESS_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
```

## Variables de entorno del frontend

Archivo:

```text
apps/web/.env
```

Contenido:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:4050/api/v1
```

## Ejecutar backend

En una terminal:

```bash
npm run dev:api
```

Validar:

```bash
curl http://localhost:4050/api/v1/health
```

## Ejecutar frontend

En otra terminal:

```bash
npm run dev:web
```

Abrir:

```text
http://localhost:3000
```

## Orden recomendado de prueba

1. Verificar `/api/v1/health`.
2. Crear categorías.
3. Crear productos.
4. Registrar usuario.
5. Iniciar sesión.
6. Consultar catálogo.
7. Agregar producto al carrito.
8. Confirmar orden.
9. Consultar historial de órdenes.

## Validaciones recomendadas

Backend:

```bash
npm run test:api
```

Frontend:

```bash
npm run typecheck:web
npm run lint:web
npm run build:web
```

## Problemas frecuentes

| Problema | Causa probable | Solución |
| --- | --- | --- |
| El frontend no carga productos | API apagada o URL incorrecta | Revisar `NUXT_PUBLIC_API_BASE_URL` |
| Error 401 | Token ausente o inválido | Iniciar sesión nuevamente |
| Error 403 | Rol sin permisos | Promover usuario a `ADMIN` |
| Firebase falla | Variables incorrectas | Revisar `.env` del backend |
| Puerto ocupado | Otro proceso usa el puerto | Cambiar puerto o cerrar proceso |

## Commit sugerido

```bash
git switch -c feature/setup-monorepo
git add .
git commit -m "chore: setup ecommerce monorepo"
```

## Navegación

- [Volver a docs](./README.md)
- [Mapa del proyecto](./00_MAPA_DEL_PROYECTO.md)
- [Guía Frontend Nuxt 4](./02_FRONTEND_NUXT4_GUIA.md)

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← 00_MAPA_DEL_PROYECTO.md](./00_MAPA_DEL_PROYECTO.md) · [02_FRONTEND_NUXT4_GUIA.md →](./02_FRONTEND_NUXT4_GUIA.md)
