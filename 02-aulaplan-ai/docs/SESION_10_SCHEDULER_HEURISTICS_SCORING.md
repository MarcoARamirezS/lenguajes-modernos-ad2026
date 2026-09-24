[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 09](./SESION_09_SCHEDULER_BACKTRACKING.md) · [Sesión 11 →](./SESION_11_GEMINI_PYTHON.md)

# Sesión 10 — Scheduler II — Heurísticas y scoring

**Duración:** 1 hora 30 minutos.

## Objetivo

Comparar soluciones válidas y elegir la de mejor calidad.

## Distribución de tiempo

```text
00–15  quality model
15–35  scoring
35–55  heuristics
55–75  search improvements
75–85  tests
85–90  commit
```


## Ejemplo de scoring

```text
+10 preferencia cumplida
+8  agenda compacta
+5  clases distribuidas

-15 hueco largo
-10 demasiadas clases consecutivas
-5  última hora
```

## Función

```python
def score_solution(solution, context) -> int:
    score = 0

    for assignment in solution:
        score += score_preferences(assignment, context)
        score -= score_penalties(assignment, context)

    return score
```

## Diagnóstico

Cuando no exista solución, devolver motivos detectables:

```json
{
  "status": "NO_SOLUTION",
  "issues": [
    "ROOM_CAPACITY_SHORTAGE",
    "TEACHER_AVAILABILITY_CONFLICT"
  ]
}
```


## Cierre verificable

- [ ] score reproducible.
- [ ] dos soluciones comparables.
- [ ] heurísticas documentadas.
- [ ] diagnóstico básico de no solución.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 09](./SESION_09_SCHEDULER_BACKTRACKING.md) · [Sesión 11 →](./SESION_11_GEMINI_PYTHON.md)
