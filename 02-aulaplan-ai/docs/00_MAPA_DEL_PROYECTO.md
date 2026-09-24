# 00 — Mapa del Proyecto AulaPlan AI

## Problema

Una institución necesita construir horarios considerando profesores, materias, grupos, aulas, disponibilidad, capacidad y preferencias. El sistema debe evitar conflictos y producir una solución explicable y versionable.

## Flujo funcional

```text
Coordinador
   ↓
Configura periodo académico
   ↓
Registra profesores / materias / grupos / salones / bloques
   ↓
Captura disponibilidad y restricciones
   ↓
Solicita generación
   ↓
Scheduler
   ├── valida hard constraints
   ├── explora candidatos
   ├── backtracking
   ├── heurísticas
   └── scoring
   ↓
Horario candidato
   ↓
Revisión
   ↓
Publicación
```

## Flujo IA

```text
Texto del coordinador
"Ana no puede los martes y prefiere terminar antes de las 14:00"
        ↓
Gemini
        ↓
JSON estructurado
        ↓
Zod
        ↓
Confirmación humana
        ↓
Firestore
        ↓
Scheduler
```

La IA **interpreta** restricciones; no sustituye al motor determinista.

## Arquitectura de despliegue

```text
GitHub
  ↓ push
Netlify
  ├── build Nuxt 4
  │      └── apps/web/.output/public
  └── build Functions
         └── apps/api/netlify/functions/api.mts
                    ↓
                  /api/*
                    ↓
        Firebase Admin + Firestore + Gemini
```

## Módulos

1. Authentication.
2. Dashboard.
3. Academic periods.
4. Teachers.
5. Subjects.
6. Groups.
7. Rooms.
8. Time blocks.
9. Teaching assignments.
10. Availability.
11. Constraints.
12. Scheduler.
13. AI constraint parser.
14. Schedule versions.
15. Publication.
16. Audit.

## Hard constraints

- Un profesor no puede ocupar dos clases al mismo tiempo.
- Un grupo no puede ocupar dos clases al mismo tiempo.
- Un salón no puede reservarse dos veces en el mismo bloque.
- El profesor debe estar disponible.
- La capacidad del salón debe cubrir el grupo.
- Un laboratorio debe asignarse a un salón compatible.
- Debe cumplirse la carga semanal de la asignación.

## Soft constraints

- Preferencia de horario del profesor.
- Reducir huecos.
- Evitar primera/última hora.
- Distribuir sesiones en distintos días.
- Evitar demasiadas clases consecutivas.
- Compactar el horario del grupo.

## Estados de horario

```text
DRAFT → GENERATED → REVIEWED → PUBLISHED → ARCHIVED
```

## Definición de terminado

- Sin conflictos duros.
- Score calculado.
- Versión almacenada.
- API protegida.
- Tests críticos en verde.
- Deploy disponible desde una sola URL Netlify.
