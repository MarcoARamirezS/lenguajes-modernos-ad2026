[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación Linux](./04_INSTALACION_LINUX.md) · [Creación monorepo →](./06_CREACION_MONOREPO.md)

# 05 — Instalación en Windows

Usa PowerShell.

## Git

```powershell
winget install -e --id Git.Git
```

## Node.js 24 LTS

```powershell
winget install -e --id OpenJS.NodeJS.LTS
```

Verifica que la versión instalada corresponda a Node 24 para el curso.

## Python 3.11

```powershell
winget install -e --id Python.Python.3.11
py -3.11 --version
```

## Java 21

```powershell
winget install -e --id EclipseAdoptium.Temurin.21.JDK
```

## CLIs

```powershell
npm install -g firebase-tools netlify-cli
```

Cierra y abre PowerShell si un ejecutable nuevo no aparece en `PATH`.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación Linux](./04_INSTALACION_LINUX.md) · [Creación monorepo →](./06_CREACION_MONOREPO.md)
