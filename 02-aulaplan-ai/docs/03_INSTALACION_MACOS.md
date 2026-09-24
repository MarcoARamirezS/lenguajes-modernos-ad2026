[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Requisitos](./02_REQUISITOS.md) · [Instalación Linux →](./04_INSTALACION_LINUX.md)

# 03 — Instalación en macOS

## Homebrew

Si ya existe:

```bash
brew --version
```

Si no existe:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Git

```bash
brew install git
```

## Node 24

```bash
brew install node@24
```

## Python 3.11

```bash
brew install python@3.11
python3.11 --version
```

Aunque `python3 --version` muestre 3.13.x, el proyecto utilizará `python3.11` al crear el entorno virtual.

## Java 21

```bash
brew install openjdk@21
java --version
```

Si Homebrew solicita enlazar Java, sigue la instrucción que imprime `brew info openjdk@21`.

## Firebase y Netlify CLI

```bash
npm install -g firebase-tools netlify-cli
firebase --version
netlify --version
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Requisitos](./02_REQUISITOS.md) · [Instalación Linux →](./04_INSTALACION_LINUX.md)
