[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 08](./SESION_08_SCHEDULING_DOMAIN.md) · [Sesión 10 →](./SESION_10_SCHEDULER_HEURISTICS_SCORING.md)

# Sesión 09 — Scheduler I — Backtracking

**Duración:** 1 hora 30 minutos.

## Objetivo

Generar la primera solución válida.

## Distribución de tiempo

```text
00–15  Backtracking
15–35  candidates
35–60  recursion
60–75  conflict checks
75–85  tests
85–90  commit
```


## Algoritmo

```python
def solve(assignments, state):
    if not assignments:
        return state

    current = assignments[0]

    for candidate in build_candidates(current, state):
        if can_place(candidate, state):
            next_state = place(candidate, state)
            result = solve(assignments[1:], next_state)

            if result is not None:
                return result

    return None
```

## Importante

La primera versión busca **una solución válida**, no la mejor.

## Heurística básica

Ordenar primero las asignaciones con menos candidatos posibles para reducir el árbol de búsqueda.


## Cierre verificable

- [ ] encuentra una solución para dataset válido.
- [ ] devuelve `None` para caso imposible.
- [ ] no duplica profesor, grupo o salón.
- [ ] tests unitarios del solver.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 08](./SESION_08_SCHEDULING_DOMAIN.md) · [Sesión 10 →](./SESION_10_SCHEDULER_HEURISTICS_SCORING.md)
