[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 11](./SESION_11_GEMINI_PYTHON.md) · [Sesión 13 →](./SESION_13_TESTING_QA.md)

# Sesión 12 — Generación y versionado

**Duración:** 1 hora 30 minutos.

## Objetivo

Convertir el solver en un flujo de negocio auditable.

## Distribución de tiempo

```text
00–15  workflow
15–35  generate endpoint
35–55  versions
55–70  publish
70–85  audit
85–90  commit
```


## Estados

```text
DRAFT
GENERATING
GENERATED
REVIEWED
PUBLISHED
ARCHIVED
```

## Regla

Una versión publicada no se sobrescribe.

## Flujo

```text
POST /schedules/generate
 ↓
load data
 ↓
validate
 ↓
solve
 ↓
score
 ↓
save immutable version
 ↓
return result
```

## Publicación

```text
POST /schedules/:id/publish
```

Debe registrar:

- user_id;
- timestamp;
- version;
- score;
- cambios relevantes.


## Cierre verificable

- [ ] generación persiste versión.
- [ ] publicación protegida.
- [ ] versión publicada inmutable.
- [ ] auditoría mínima.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 11](./SESION_11_GEMINI_PYTHON.md) · [Sesión 13 →](./SESION_13_TESTING_QA.md)
