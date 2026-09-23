# AulaPlan AI — Git y GitHub Workflow

## Estrategia

Se utilizará un repositorio remoto único y ramas cortas por sesión.

```text
main
├── feature/sesion-01-foundation
├── feature/sesion-02-fastapi
├── feature/sesion-03-firebase
├── feature/sesion-04-academic-core
├── feature/sesion-05-resources
├── feature/sesion-06-constraints
├── feature/sesion-07-auth
├── feature/sesion-08-scheduling-domain
├── feature/sesion-09-ortools
├── feature/sesion-10-optimization
├── feature/sesion-11-ai
├── feature/sesion-12-generation
├── feature/sesion-13-testing
└── feature/sesion-14-cicd
```

## Inicio de una sesión

```bash
git switch main
git pull
git switch -c feature/sesion-XX-descripcion
```

## Durante el trabajo

```bash
git status
git diff
```

## Cierre

```bash
git add .
git commit -m "feat: complete session XX"
git push -u origin feature/sesion-XX-descripcion
```

Crear Pull Request y fusionar únicamente cuando el checklist de sesión esté en verde.

## Convención de commits

| Prefijo | Uso |
| --- | --- |
| `chore:` | configuración |
| `feat:` | funcionalidad |
| `fix:` | corrección |
| `test:` | pruebas |
| `docs:` | documentación |
| `refactor:` | reorganización sin cambiar comportamiento |
| `ci:` | integración/despliegue |

## Tags del curso

```bash
git tag -a v0.1.0 -m "Foundation"
git push origin v0.1.0
```

Propuesta:

| Tag | Hito |
| --- | --- |
| `v0.1.0` | Foundation |
| `v0.2.0` | Firebase |
| `v0.3.0` | Academic Core |
| `v0.4.0` | Auth |
| `v0.5.0` | Scheduling |
| `v0.6.0` | AI |
| `v1.0.0` | Producción |

## Archivos prohibidos

Nunca deben aparecer en Git:

```text
.env
.env.*
!.env.example
.venv/
node_modules/
service-account*.json
firebase-adminsdk*.json
.nuxt/
.output/
coverage/
.pytest_cache/
__pycache__/
```
