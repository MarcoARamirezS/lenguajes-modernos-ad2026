# 06 — Decisión de arquitectura Netlify

## Requisito no negociable

Frontend y backend deben desplegarse en **un único proyecto Netlify** desde **un único monorepo**.

## Arquitectura seleccionada

```text
Nuxt 4 SPA/static
+
Modern Netlify Functions TypeScript
+
Firebase
+
Gemini
```

## Por qué no FastAPI

Netlify no ofrece Python como runtime de sus Functions modernas. Python disponible en build no equivale a un backend Python persistente/serverless.

## Por qué no Go para un proyecto nuevo

Netlify documenta Go mediante el modo compatible con AWS Lambda. Ese modo está deprecated y Netlify anunció que los despliegues que lo utilicen dejarán de aceptarse a partir del 1 de julio de 2027.

## Por qué TypeScript sigue aportando aprendizaje nuevo

No se repite Express. El backend usa:

- Web `Request` y `Response`;
- Functions serverless;
- rutas declarativas `/api/*`;
- cold starts y stateless execution;
- environment variables por runtime;
- límites de ejecución;
- Firebase Admin;
- motor algorítmico propio;
- integración IA;
- same-origin frontend/API.

## Patrón API

Se usa una Function principal:

```text
apps/api/netlify/functions/api.mts
```

con:

```text
path: ["/api", "/api/*"]
```

La Function delega a un router interno, evitando crear una Function diferente por cada endpoint.

## Beneficios

- Un dominio.
- Sin CORS para el flujo normal.
- Un deploy atómico.
- Deploy previews completos.
- Rollback conjunto.
- Configuración de secrets centralizada.
- Menor complejidad operativa para el alumno.

## Restricción de tiempo

El solver debe tener un presupuesto de tiempo propio inferior al límite de la Function. En el curso se usará un límite configurable, por ejemplo `MAX_SOLVER_MS=8000`, y se devolverá la mejor solución encontrada dentro de ese presupuesto.
