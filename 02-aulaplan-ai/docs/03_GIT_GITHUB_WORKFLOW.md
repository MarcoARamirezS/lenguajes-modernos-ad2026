# 03 — Git y GitHub Workflow

## Repositorio

Un repositorio GitHub contiene frontend, API serverless, contratos, Firebase y documentación.

## Ramas sugeridas

```text
main
├── feature/session-01-foundation
├── feature/session-02-functions
├── feature/session-03-firebase
├── feature/session-04-academic-core
├── feature/session-05-resources
├── feature/session-06-constraints
├── feature/session-07-auth
├── feature/session-08-domain
├── feature/session-09-backtracking
├── feature/session-10-scoring
├── feature/session-11-ai
├── feature/session-12-versioning
├── test/session-13-qa
└── ci/session-14-netlify
```

## Inicio de sesión

```bash
git switch main
git pull
git switch -c feature/session-XX-topic
```

## Cierre

```bash
git status
git add .
git commit -m "feat: complete session XX topic"
git push -u origin feature/session-XX-topic
```

## Convención de commits

- `feat:` funcionalidad.
- `fix:` corrección.
- `refactor:` reorganización sin cambio funcional.
- `test:` pruebas.
- `docs:` documentación.
- `chore:` configuración.
- `ci:` automatización.

## Versiones sugeridas

```text
v0.1.0 foundation
v0.2.0 firebase
v0.3.0 academic-core
v0.4.0 auth-rbac
v0.5.0 scheduler
v0.6.0 ai
v0.9.0 qa
v1.0.0 production
```

## Pull Request

Cada PR debe documentar:

1. objetivo;
2. archivos principales;
3. endpoint o flujo agregado;
4. evidencia de prueba;
5. variables nuevas;
6. riesgos o deuda técnica.
