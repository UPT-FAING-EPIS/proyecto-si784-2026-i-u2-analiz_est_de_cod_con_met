# Estándares de Programación

## 1. OBJETIVO
*   Asegurar la validez de los datos, forzando reglas críticas directamente desde los esquemas de validación (Pydantic) y las restricciones de la base de datos (SQLAlchemy).
*   Centralizar procesos complejos en la **Capa de Negocios (Servicios)** para evitar la duplicidad de código y asegurar que la lógica transaccional se ejecute siempre de manera coherente.
*   Registrar automáticamente todos los cambios y acciones cruciales del sistema (mediante la tabla `user_action_logs`). Esto es vital para fines de auditoría y depuración.
*   Optimizar el código mediante el tipado estricto (Type Hinting) y consultas ORM eficientes para que el sistema maneje grandes volúmenes de análisis sin degradar el rendimiento.
*   Estructurar el sistema por módulos (Clean Architecture) con separación de responsabilidades, simplificando el mantenimiento.

## 2. DECLARACIÓN DE VARIABLES
Se propone que la declaración de las variables se ajuste al motivo para la que se requieran, utilizando el estándar de Python (PEP 8).

### 2.1 Descripción de la Variable
*   La longitud debe ser lo más recomendable posible. Para este caso, establecemos una longitud que sea suficientemente descriptiva sin exceder los límites lógicos.
*   **Formato:** `snake_case` (todo en minúscula separado por guiones bajos).
*   **Alcance:**
    *   **Global:** Se declaran en mayúsculas (`UPPER_SNAKE_CASE`). Ejemplo: `SECRET_KEY`, `MAX_UPLOAD_SIZE`.
    *   **Local:** Se declaran en minúsculas sin prefijos adicionales. Ejemplo: `project_name`, `user_id`.

### 2.2 Variables de Tipo Arreglo
*   Para variables que almacenan arreglos, listas o colecciones de elementos, se debe utilizar el plural del sustantivo que representan.
*   *Ejemplo:* `analysis_reports`, `code_smells`, `users_list`.

## 3. Definición de datos y funciones
Se deben utilizar los siguientes tipos de datos mediante el ORM (SQLAlchemy) para asegurar la consistencia y optimizar el rendimiento.

### 3.1 Tipo de datos

| Uso | Tipo de Dato (ORM) | Razón de la Elección | Ejemplos de Campos |
| :--- | :--- | :--- | :--- |
| Identificadores | `Integer` | Rango suficiente para Claves Primarias y Foráneas. Configurado como `primary_key=True` (Auto-incremental). | `id`, `user_id` |
| Valores Booleanos | `Boolean` | Eficiente para representar estados binarios (Verdadero/Falso). | `active_status`, `is_logged_in` |
| Fechas y Tiempos | `DateTime` | Almacena fecha y hora con precisión para la trazabilidad de análisis y logs. | `analysis_date`, `timestamp` |
| Texto Corto | `String(N)` | Para nombres o identificadores de terceros. El tamaño (N) optimiza el espacio en BD. | `username`, `github_id` |
| Estructuras Complejas | `JSON` | Ideal para almacenar diccionarios de datos dinámicos generados por el motor de análisis. | `code_smells`, `details` |

### 3.2 Declaración de variables
Toda variable debe utilizar **Type Hinting** explícito para facilitar la lectura y el análisis estático.
*   *Ejemplo:* `usuario_id: int`, `codigo_fuente: str`.

### 3.3 Declaración de funciones
*   **Nomenclatura:** Siguen la convención Verbo-Sustantivo en formato `snake_case` (`analizar_codigo`, `registrar_usuario`).
*   **Documentación:** Deben incluir `Docstrings` que expliquen Propósito, Parámetros (`Args`) y Retorno (`Returns`).
*   **Manejo de Errores:** Deben incluir bloques `try...except` para capturar errores específicos y garantizar que el sistema retorne un estado adecuado al frontend sin caerse.

### 3.4 Control de versiones de código fuente
El sistema usa Git para el control de versiones. Las modificaciones se deben regir bajo las siguientes convenciones:
*   Ramas (Branches): `feature/nombre_funcionalidad`, `fix/correccion_error`.
*   Mensajes de Commit: Deben ser claros y en presente imperativo (Ej: `Agregar tabla user_action_logs`).
*   Si se requieren entregables físicos/comprimidos (como dicta el formato base), seguirán el formato: `[NOMBRE_DOCUMENTO]_[FECHA]_[HORA].zip` (Ej. `SGE_Proyecto_20260612_1000.zip`).

## 4. Procedimientos y Funciones definidos por el Usuario
En lugar de depender exclusivamente de la Base de Datos para la lógica, este proyecto delega el flujo de trabajo a la capa de **Negocios (Servicios)** y a la capa del **Motor de Análisis**, garantizando la integridad, el rendimiento y la reutilización del código.

### 4.1. Flujos Transaccionales (Servicios y Repositorios)
Manejan las transacciones de Registro (Insert), Modificación (Update) y Procesos Críticos.
*   Deben encapsularse en métodos que utilicen el contexto de sesión de la base de datos.
*   **Transacciones Seguras:** Si ocurre una falla en el proceso (por ejemplo, al registrar un usuario), el sistema ejecuta un `db.rollback()` para evitar inconsistencias, análogo al `ROLLBACK` de un Procedimiento Almacenado.

### 4.2. Funciones Definidas por el Usuario (Capa Core - Lógica y Consultas)
Se utilizan para los cálculos algorítmicos del análisis estático que no implican alteración directa de los datos hasta que se emite el reporte final.

#### 4.2.1. Funciones Escalares
Funciones puras que procesan una entrada y devuelven un cálculo único.
*   *Ejemplo:* `calcular_complejidad_ciclomatica(ast_tree) -> int`.

#### 4.2.2. Funciones de Colección/Tabla
Funciones dentro de los Repositorios diseñadas para extraer conjuntos de datos complejos o reportes históricos bajo múltiples filtros.
*   *Ejemplo:* `get_reports_by_user(user_id: int, limit: int) -> list[AnalysisReport]`.

## 5. Beneficios
*   **Mantenibilidad:** Separar el código por módulos (Clean Architecture) facilita encontrar y reparar bugs rápidamente.
*   **Seguridad y Fiabilidad:** El uso de Type Hinting y validaciones previas evitan inyecciones y datos corruptos en la base de datos.
*   **Escalabilidad:** Al no acoplar la lógica de negocio puramente en Procedimientos Almacenados de la base de datos, el backend de FastAPI puede escalar horizontalmente con mayor facilidad.
*   **Trabajo en Equipo:** Estandarizar la nomenclatura permite que cualquier integrante del grupo comprenda rápidamente las funciones escritas por sus compañeros.

## 6. Conclusiones
La adopción de estos estándares de programación es una medida fundamental para garantizar que el desarrollo del **Analizador Estático de Código con Métricas** sea disciplinado, coherente y robusto. Su estricta implementación asegura que el código fuente no solo resuelva los requerimientos actuales, sino que posea la calidad técnica necesaria para ser sostenible en el tiempo.
