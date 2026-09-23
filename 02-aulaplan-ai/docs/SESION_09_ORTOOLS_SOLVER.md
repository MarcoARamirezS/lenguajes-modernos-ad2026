# Sesión 09 — OR-Tools CP-SAT: primer solver

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Construir el primer solver capaz de asignar cada sesión a un bloque y salón sin conflictos.

## Resultado esperado

`POST /schedules/generate` produce una solución FEASIBLE/OPTIMAL para el dataset pequeño y detecta escenarios INFEASIBLE.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | CP-SAT |
| 15–30 | Variables booleanas |
| 30–50 | Hard constraints |
| 50–70 | Extracción de solución |
| 70–82 | Endpoint generate |
| 82–90 | Caso inviable |

## Instalar

```bash
pip install ortools
```

## Variable conceptual

```text
x[assignment, occurrence, room, timeBlock] ∈ {0,1}
```

`1` significa que esa ocurrencia se asigna a ese salón y bloque.

## Hard constraints mínimas

1. Cada ocurrencia debe asignarse exactamente una vez.
2. Un profesor no puede tener dos clases en el mismo bloque.
3. Un grupo no puede tener dos clases en el mismo bloque.
4. Un salón no puede tener dos clases en el mismo bloque.
5. Solo crear variables para salones compatibles.
6. Solo crear variables para bloques donde el profesor esté disponible.

## Esqueleto

`app/scheduling/solver.py`:

```python
from ortools.sat.python import cp_model


class ScheduleSolver:
    def solve(self, problem):
        model = cp_model.CpModel()
        variables = {}

        # Crear variables únicamente para combinaciones permitidas.
        # Agregar restricciones exactly-one y no-overlap.

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.solve(model)

        return {
            "status": solver.status_name(status),
            "entries": [],
        }
```

No dejar `TODO` en la entrega final de la sesión: los alumnos deben implementar las restricciones con el dataset del aula. El esqueleto sirve para explicar la forma del solver antes de completarlo.

## Estado

Tratar al menos:

```text
OPTIMAL
FEASIBLE
INFEASIBLE
UNKNOWN
```

## Endpoint

```text
POST /api/v1/schedules/generate
```

Inicialmente puede recibir `academicPeriodId` y cargar todos los datos necesarios.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: implement OR-Tools schedule solver"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
