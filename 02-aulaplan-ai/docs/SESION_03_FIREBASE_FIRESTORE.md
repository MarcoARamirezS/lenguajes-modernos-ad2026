# Sesión 03 — Firebase Admin, Firestore y Emulator Suite

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Integrar Firebase Admin en Python, configurar Firestore local mediante Emulator Suite y crear un repositorio base reutilizable.

## Resultado esperado

FastAPI puede escribir y leer un documento de prueba contra Firestore Emulator sin utilizar credenciales de producción.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Modelo Firebase |
| 15–30 | Firebase CLI |
| 30–45 | Emulator Suite |
| 45–60 | Firebase Admin Python |
| 60–75 | Repository base |
| 75–90 | Prueba E2E local |

## Instalar SDK

```bash
cd apps/api
pip install firebase-admin
```

## Inicializar Firebase

Desde raíz:

```bash
firebase login
firebase init firestore emulators
```

Seleccionar Firestore y Auth Emulator. Puertos sugeridos:

```text
Firestore 8080
Auth      9099
UI        4000
```

## Variables locales para emuladores

### macOS / Linux

```bash
export FIRESTORE_EMULATOR_HOST=127.0.0.1:8080
export FIREBASE_AUTH_EMULATOR_HOST=127.0.0.1:9099
export GCLOUD_PROJECT=aulaplan-local
```

### Windows PowerShell

```powershell
$env:FIRESTORE_EMULATOR_HOST="127.0.0.1:8080"
$env:FIREBASE_AUTH_EMULATOR_HOST="127.0.0.1:9099"
$env:GCLOUD_PROJECT="aulaplan-local"
```

## `app/core/firebase.py`

```python
import firebase_admin
from firebase_admin import firestore
from app.core.config import get_settings


def init_firebase() -> None:
    if firebase_admin._apps:
        return
    settings = get_settings()
    options = {"projectId": settings.firebase_project_id or "aulaplan-local"}
    firebase_admin.initialize_app(options=options)


def get_db():
    init_firebase()
    return firestore.client()
```

## Arranque del emulador

Terminal independiente:

```bash
firebase emulators:start --only firestore,auth
```

## Regla de seguridad

El backend usa Admin SDK y, por tanto, las reglas cliente no sustituyen la autorización del backend. Aun así, bloquear acceso directo de cliente a datos sensibles:

`firebase/firestore.rules`:

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

## Prueba conceptual

Crear temporalmente un script `apps/api/scripts/firestore_smoke.py` que escriba `smoke/test` y lo lea. El objetivo es verificar infraestructura, no añadir lógica de negocio.

## Seguridad

En local, para producción real fuera de Google Cloud, usar Application Default Credentials mediante `GOOGLE_APPLICATION_CREDENTIALS`. Nunca copiar el contenido de la cuenta de servicio al repositorio.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: integrate Firebase Admin and emulators"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
