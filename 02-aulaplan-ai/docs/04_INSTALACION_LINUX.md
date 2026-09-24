[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación macOS](./03_INSTALACION_MACOS.md) · [Instalación Windows →](./05_INSTALACION_WINDOWS.md)

# 04 — Instalación en Linux

Ejemplo Ubuntu/Debian.

## Base

```bash
sudo apt update
sudo apt install -y git curl build-essential
```

## Node 24

Usa NodeSource, nvm o el método institucional del laboratorio. Al terminar:

```bash
node --version
npm --version
```

Debe utilizarse Node 24 LTS durante el curso.

## Python 3.11

Si tu distribución lo incluye:

```bash
sudo apt install -y python3.11 python3.11-venv python3.11-dev
python3.11 --version
```

Si no está disponible en el repositorio de tu versión, instala Python 3.11 mediante el gestor recomendado por tu distribución o `pyenv`; no reemplaces el Python del sistema.

## Java 21

```bash
sudo apt install -y openjdk-21-jdk
java --version
```

## CLIs

```bash
sudo npm install -g firebase-tools netlify-cli
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Instalación macOS](./03_INSTALACION_MACOS.md) · [Instalación Windows →](./05_INSTALACION_WINDOWS.md)
