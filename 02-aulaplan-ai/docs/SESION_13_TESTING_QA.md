[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 12](./SESION_12_GENERACION_VERSIONADO.md) · [Sesión 14 →](./SESION_14_CICD_NETLIFY_FIREBASE_GITHUB.md)

# Sesión 13 — Testing y QA

**Duración:** 1 hora 30 minutos.

## Objetivo

Probar dominio, API, Firestore y flujo crítico.

## Distribución de tiempo

```text
00–20  pytest
20–40  unit tests
40–60  API tests
60–75  emulators
75–85  Playwright
85–90  report
```


## Backend

```bash
pytest -q
```

Cobertura mínima:

- Pydantic schemas;
- services;
- rules del scheduler;
- backtracking;
- scoring;
- auth helpers.

## Firestore

Usar Emulator Suite para integración.

## E2E

Flujo crítico:

```text
login
→ crear profesor
→ crear materia
→ capturar disponibilidad
→ generar horario
→ revisar
→ publicar
```

## Regla

Los tests del scheduler no deben depender de red ni Firestore.


## Cierre verificable

- [ ] pytest verde.
- [ ] integración contra emuladores.
- [ ] E2E crítico.
- [ ] caso NO_SOLUTION probado.
- [ ] reporte de evidencias.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 12](./SESION_12_GENERACION_VERSIONADO.md) · [Sesión 14 →](./SESION_14_CICD_NETLIFY_FIREBASE_GITHUB.md)
