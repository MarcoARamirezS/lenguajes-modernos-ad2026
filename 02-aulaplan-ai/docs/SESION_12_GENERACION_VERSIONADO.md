# Sesión 12 — Generación E2E, versionado y publicación

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Unir repositorios, problem builder, solver y persistencia para cerrar el flujo de negocio de generación de horarios.

## Resultado esperado

El usuario genera una nueva versión, la revisa y puede publicarla sin sobrescribir versiones anteriores.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Orquestación |
| 15–35 | ScheduleService |
| 35–50 | Persistencia |
| 50–65 | Estados |
| 65–80 | Conectar Nuxt |
| 80–90 | Flujo E2E |

## Estados

```text
DRAFT
GENERATED
REVIEWED
PUBLISHED
ARCHIVED
```

## Transiciones

```text
GENERATED → REVIEWED → PUBLISHED → ARCHIVED
```

No permitir `GENERATED → PUBLISHED` si la regla de negocio exige revisión.

## `ScheduleService.generate()`

Responsabilidades:

1. Obtener periodo.
2. Cargar catálogos activos.
3. Cargar teaching assignments.
4. Cargar disponibilidad.
5. Cargar constraints.
6. Construir `SchedulingProblem`.
7. Prevalidar.
8. Ejecutar solver.
9. Construir resultado.
10. Calcular siguiente versión.
11. Guardar `schedule_versions`.
12. Devolver DTO.

## Versiones

No usar `count + 1` sin protección conceptual. Para el curso, obtener `max(version)` dentro del periodo y documentar el riesgo de concurrencia; en una versión productiva se debe proteger el consecutivo con una transacción o contador atómico.

## Frontend

Habilitar botones de `/generator`:

```text
Interpretar IA → POST /ai/constraints/parse
Generar       → POST /schedules/generate
```

En `/schedules` listar versiones y mostrar status, score y fecha.

## Publicación

Al publicar una versión, archivar la versión publicada previa del mismo periodo dentro de una operación controlada.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: complete schedule generation workflow"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
