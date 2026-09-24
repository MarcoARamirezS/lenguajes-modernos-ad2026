# Sesión 04 — RBAC y rutas privadas

> Archivo restaurado para mantener íntegra la navegación del repositorio guía.

## Objetivo

Integrar autorización basada en roles sobre la autenticación desarrollada en la sesión anterior.

## Resultado esperado

- Middleware de autenticación reutilizable.
- Middleware de autorización por roles.
- Rutas administrativas protegidas.
- Respuestas `401` para sesiones inválidas y `403` para permisos insuficientes.
- Pruebas de los casos permitidos y rechazados.

## Flujo

```text
Request
  ↓
Access token
  ↓
authenticate
  ↓
requireRole(...roles)
  ↓
controller
```

## Checklist

- [ ] El usuario no autenticado recibe `401`.
- [ ] El usuario autenticado sin rol recibe `403`.
- [ ] El rol autorizado accede al recurso.
- [ ] Los permisos se validan en backend y no únicamente en frontend.
- [ ] Las pruebas se ejecutan en verde.

[Volver a documentación del Proyecto 01](./README.md)
