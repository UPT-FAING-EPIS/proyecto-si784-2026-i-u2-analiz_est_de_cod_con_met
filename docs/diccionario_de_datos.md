# Diccionario de Datos

## 1. Modelo Entidad Relación

### 1.1. Diseño Lógico

A continuación, se presenta el detalle lógico de cada una de las tablas del sistema del **Analizador Estático de Código**, especificando sus atributos y las restricciones clave (PK, FK, UNIQUE, CHECK, DEFAULT) extraídas directamente del ORM.

**Tabla: users**
*   **Propósito:** Almacenar la información y credenciales de los usuarios registrados, así como su estado de sesión e integraciones con terceros (GitHub/Google).
*   **Restricciones:**
    *   **PK:** `id`
    *   **UNIQUE:** `username`, `github_id`, `google_id`
    *   **DEFAULT:** `active_status` = `True`, `is_logged_in` = `False`

**Tabla: analysis_reports**
*   **Propósito:** Registrar el historial de análisis estáticos realizados por cada usuario, incluyendo métricas y hallazgos.
*   **Restricciones:**
    *   **PK:** `id`
    *   **FK:** `user_id` (referencia a `users.id`)
    *   **DEFAULT:** `analysis_date` = Fecha y hora actual (`datetime.utcnow`), `code_smells` = Diccionario vacío (`{}`)

**Tabla: user_action_logs**
*   **Propósito:** Mantener una bitácora o log de auditoría de las acciones realizadas por los usuarios en la plataforma.
*   **Restricciones:**
    *   **PK:** `id`
    *   **FK:** `user_id` (referencia a `users.id`)
    *   **DEFAULT:** `timestamp` = Fecha y hora actual (`datetime.utcnow`)

#### Relaciones Lógicas (Foreign Keys - FK)
*   **users (1) -> (N) analysis_reports:** Un usuario puede generar múltiples reportes de análisis.
*   **users (1) -> (N) user_action_logs:** Un usuario puede registrar múltiples acciones de log.

---

### 1.2. Diseño Físico

A continuación se detalla la estructura física de la base de datos según los modelos definidos.

#### Tabla: users

| Campo / Atributo | Tipo de Dato | Longitud | Nulo | Restricción / Índice | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | Integer | - | NO | PK, Index | Identificador único del usuario |
| `username` | String | 150 | NO | UNIQUE, Index | Nombre de usuario en la plataforma |
| `password_hash` | String | 255 | SÍ | - | Hash de la contraseña (si usa login tradicional) |
| `github_id` | String | 100 | SÍ | UNIQUE, Index | ID de usuario de GitHub (OAuth) |
| `github_token` | String | 255 | SÍ | - | Token de acceso de GitHub |
| `google_id` | String | 100 | SÍ | UNIQUE, Index | ID de usuario de Google (OAuth) |
| `avatar_url` | String | 255 | SÍ | - | URL de la foto de perfil del usuario |
| `role` | String | 50 | NO | - | Rol del usuario en el sistema (ej. admin, user) |
| `active_status` | Boolean | - | NO | DEFAULT: True | Indica si la cuenta está activa o bloqueada |
| `is_logged_in` | Boolean | - | NO | DEFAULT: False | Estado actual de la sesión del usuario |

#### Tabla: analysis_reports

| Campo / Atributo | Tipo de Dato | Longitud | Nulo | Restricción / Índice | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | Integer | - | NO | PK, Index | Identificador único del reporte |
| `user_id` | Integer | - | NO | FK(users.id), Index| Identificador del usuario que generó el reporte |
| `project_name` | String | 255 | NO | - | Nombre del proyecto o archivo analizado |
| `analysis_date` | DateTime | - | NO | DEFAULT: utcnow | Fecha y hora en la que se realizó el análisis |
| `loc` | Integer | - | NO | - | Líneas de Código (Lines of Code) |
| `complexity` | Integer | - | NO | - | Complejidad ciclomática calculada |
| `code_smells` | JSON | - | NO | DEFAULT: {} | Objeto JSON con los "code smells" detectados |

#### Tabla: user_action_logs

| Campo / Atributo | Tipo de Dato | Longitud | Nulo | Restricción / Índice | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | Integer | - | NO | PK, Index | Identificador único del registro de log |
| `user_id` | Integer | - | NO | FK(users.id), Index| Identificador del usuario que realizó la acción |
| `action` | String | 255 | NO | - | Descripción corta de la acción (ej. "login", "upload")|
| `details` | JSON | - | SÍ | - | Detalles técnicos o metadatos de la acción |
| `timestamp` | DateTime | - | NO | DEFAULT: utcnow | Fecha y hora exacta del evento |
