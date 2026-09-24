[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 07](./SESION_07_FIREBASE_AUTH_RBAC.md) · [Sesión 09 →](./SESION_09_SCHEDULER_BACKTRACKING.md)

# Sesión 08 — Scheduling Domain

**Duración:** 1 hora 30 minutos.

## Objetivo

Modelar el problema sin resolverlo todavía.

## Distribución de tiempo

```text
00–20  CSP
20–40  Assignment
40–55  Candidate
55–70  Hard rules
70–85  test data
85–90  commit
```


## Entidades de dominio

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class AssignmentRequest:
    subject_id: str
    teacher_id: str
    group_id: str
    weekly_blocks: int
    required_room_type: str

@dataclass(frozen=True)
class Slot:
    day: str
    block_id: str
    room_id: str
```

## Candidate

Un candidato combina:

```text
assignment
+
slot
```

## Restricciones duras

Implementarlas como funciones puras para poder probarlas sin Firebase.


## Cierre verificable

- [ ] Domain models independientes de Firestore.
- [ ] Candidate model.
- [ ] Hard rules como funciones puras.
- [ ] Dataset pequeño de prueba.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 07](./SESION_07_FIREBASE_AUTH_RBAC.md) · [Sesión 09 →](./SESION_09_SCHEDULER_BACKTRACKING.md)
