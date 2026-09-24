[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Firebase](./07_FIREBASE_SETUP.md) · [Frontend setup →](./09_FRONTEND_NUXT4_SETUP.md)

# 08 — GitHub

## Primer commit

```bash
git add .
git commit -m "chore: initialize AulaPlan AI monorepo"
git branch -M main
```

## Con GitHub CLI

```bash
gh repo create aulaplan-ai --public --source=. --remote=origin --push
```

## O manual

```bash
git remote add origin https://github.com/TU_USUARIO/aulaplan-ai.git
git push -u origin main
```

## Flujo posterior

```bash
git switch -c feature/session-01-python-foundation
# cambios
git add .
git commit -m "feat: complete backend session 01"
git push -u origin feature/session-01-python-foundation
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Firebase](./07_FIREBASE_SETUP.md) · [Frontend setup →](./09_FRONTEND_NUXT4_SETUP.md)
