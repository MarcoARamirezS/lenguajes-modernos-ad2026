[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Frontend Nuxt 4](./03_FRONTEND_NUXT4_ENTREGA_UNICA.md) · [Modelo Firestore →](./05_MODELO_FIRESTORE.md)

# 04 — Git y GitHub

## Estrategia

```text
main
 ├── feature/session-01-foundation
 ├── feature/session-02-python-api
 ├── feature/session-03-firebase
 ├── feature/session-09-scheduler
 └── feature/session-11-gemini
```

## Flujo por sesión

```bash
git switch -c feature/session-01-foundation
git status
git add .
git commit -m "feat: complete AulaPlan session 01"
git push -u origin feature/session-01-foundation
```

## Commits sugeridos

```text
chore: initialize monorepo
feat: add python api foundation
feat: integrate firebase firestore
feat: add teacher repository
feat: implement schedule backtracking
feat: integrate gemini parser
test: add scheduler coverage
ci: deploy web and python functions
```

## Pull Request

Antes del merge:

- tests verdes;
- secretos fuera del repo;
- documentación actualizada;
- endpoints probados;
- checklist de la sesión completo.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Frontend Nuxt 4](./03_FRONTEND_NUXT4_ENTREGA_UNICA.md) · [Modelo Firestore →](./05_MODELO_FIRESTORE.md)
