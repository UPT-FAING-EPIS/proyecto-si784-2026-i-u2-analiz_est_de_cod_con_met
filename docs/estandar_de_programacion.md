# Estándares de Programación

## 1. OBJETIVO
El presente estándar de programación tiene como finalidad establecer directrices técnicas y metodológicas para el desarrollo del **Analizador Estático de Código con Métricas**. Los objetivos específicos son:
*   **Asegurar la validez y consistencia de los datos:** Forzar reglas críticas directamente desde la entrada del usuario usando esquemas de validación (ej. Pydantic) y mapearlas a restricciones estrictas en la base de datos mediante el ORM (SQLAlchemy), previniendo inyecciones SQL y datos corruptos.
*   **Centralizar la lógica de negocio:** Agrupar procesos complejos y transaccionales en la **Capa de Negocios (Servicios)**. Esto evita la duplicidad de código, asegura el principio de responsabilidad única (SRP) y garantiza que las reglas transaccionales se ejecuten de manera coherente en toda la aplicación.
*   **Trazabilidad y Auditoría:** Registrar automáticamente todos los cambios, accesos y acciones cruciales del sistema en la tabla `user_action_logs`. Este historial inmutable es vital para fines de auditoría, depuración y monitoreo de seguridad.
*   **Optimización y Rendimiento:** Estructurar el código mediante tipado estricto (Type Hinting) y construir consultas ORM optimizadas (evitando el problema N+1) para que el sistema mantenga tiempos de respuesta bajos incluso al procesar y almacenar análisis de archivos fuente de gran tamaño.
*   **Desacoplamiento Tecnológico:** Aplicar estrictamente **Clean Architecture**, dividiendo el sistema en módulos independientes (Presentación, Negocios, Core de Análisis y Persistencia) para que las modificaciones en la interfaz o en la base de datos no afecten el motor central.

## 2. DECLARACIÓN DE VARIABLES
La declaración de variables en el proyecto se rige por el estándar oficial de Python (PEP 8), priorizando la legibilidad humana por encima de la brevedad técnica.

### 2.1 Descripción de la Variable
*   **Longitud y Claridad:** El nombre de la variable debe describir inequívocamente su contenido o propósito. No debe ser tan corta que pierda significado (`c`, `x`, `p`), ni tan larga que dificulte la lectura (máximo recomendado: 20-25 caracteres).
*   **Formato de Nomenclatura:** Se utilizará `snake_case` (palabras en minúsculas separadas por guiones bajos) para todas las variables y atributos de clase.
*   **Alcance (Scope):**
    *   **Global (Constantes):** Variables que no cambian de valor durante la ejecución. Se declaran en el nivel superior del módulo utilizando `UPPER_SNAKE_CASE`. 
        *   *Ejemplo Correcto:* `MAX_UPLOAD_SIZE = 50000`, `DEFAULT_ROLE = "user"`
    *   **Local (Variables de Bloque/Función):** Se declaran explícitamente en el lugar donde se necesitan por primera vez, usando `snake_case`.
        *   *Ejemplo Correcto:* `project_name = "mi_proyecto"`, `is_valid = True`

### 2.2 Variables de Tipo Arreglo (Colecciones)
*   Toda variable que almacene una colección (Listas, Tuplas, Diccionarios o Sets) debe nombrarse obligatoriamente en **plural**, refiriéndose a los elementos que contiene.
*   Si la colección almacena objetos complejos, se puede usar un sufijo descriptivo como `_list` o `_map` si mejora la claridad, aunque el plural suele ser suficiente.
    *   *Ejemplo de Lista:* `code_smells: list[str] = []`, `analysis_reports: list[AnalysisReport]`
    *   *Ejemplo de Diccionario:* `user_sessions_map: dict[int, str] = {}`

## 3. Definición de datos y funciones
Para interactuar con la base de datos relacional sin perder las ventajas orientadas a objetos, se utilizará SQLAlchemy como puente.

### 3.1 Tipo de datos
La elección del tipo de dato debe ser lo más restrictiva posible para conservar memoria y mejorar los tiempos de indexación:

| Uso | Tipo de Dato (SQLAlchemy / Python) | Razón de la Elección | Ejemplos de Campos |
| :--- | :--- | :--- | :--- |
| **Identificadores (PK/FK)** | `Integer` / `int` | Ocupa solo 4 bytes, ofrece rango suficiente (hasta 2 mil millones) y la indexación B-Tree es extremadamente rápida. | `id`, `user_id`, `report_id` |
| **Valores Booleanos** | `Boolean` / `bool` | Eficiente para comprobaciones condicionales (0/1 a nivel físico). | `active_status`, `is_logged_in` |
| **Fechas y Tiempos** | `DateTime` / `datetime` | Almacena fechas absolutas. Siempre se debe guardar en formato UTC para evitar conflictos de zona horaria. | `analysis_date`, `timestamp` |
| **Texto Corto/Indexado** | `String(N)` / `str` | Limita físicamente la memoria del campo. Indispensable para campos `UNIQUE` o aquellos usados en búsquedas (`WHERE`). | `username` (150), `github_id` (100) |
| **Estructuras Dinámicas** | `JSON` / `dict` | Permite guardar el resultado del AST (Árbol de Sintaxis Abstracta) o métricas sin necesidad de normalizar tablas secundarias infinitas. | `code_smells`, `details` |

### 3.2 Declaración de variables (Type Hinting)
Toda declaración, tanto de variables locales como de atributos de clase, debe incorporar anotaciones de tipo (Type Hinting) introducidas en Python 3.5+. Esto permite que el IDE (ej. VS Code) detecte errores de compatibilidad de tipos antes de la ejecución.
```python
# Declaración correcta
total_loc: int = 150
es_valido: bool = False
nombres_archivos: list[str] = ["main.py", "utils.py"]
```

### 3.3 Declaración de funciones
El sistema requiere que cada función encapsule una sola responsabilidad.
*   **Nomenclatura:** Convención Verbo-Sustantivo en formato `snake_case` (ej. `calcular_complejidad`, `validar_token_acceso`).
*   **Documentación (Docstrings):** Es obligatorio incluir Docstrings bajo el formato "Google Style" para describir el propósito, los argumentos y el retorno esperado.
*   **Manejo de Errores:** Las funciones no deben imprimir errores en consola crudos (`print`). Deben utilizar estructuras `try...except` e interactuar con el módulo `logging` y retornar excepciones controladas (`HTTPException` en la capa web).
```python
def analizar_codigo_fuente(codigo: str, estricto: bool = False) -> dict[str, Any]:
    """
    Parsea el código fuente ingresado y genera un reporte de complejidad.

    Args:
        codigo (str): El contenido del archivo en texto plano.
        estricto (bool): Si es True, falla ante la mínima advertencia sintáctica.

    Returns:
        dict[str, Any]: Diccionario conteniendo métricas y hallazgos.
        
    Raises:
        SyntaxParsingError: Si el código fuente tiene sintaxis inválida.
    """
    try:
        # Lógica de análisis
        pass
    except Exception as e:
        # Manejo centralizado
        pass
```

### 3.4 Control de versiones de código fuente
El código se gestionará en GitHub bajo los principios simplificados de GitFlow:
*   **Ramas (Branches):** Nunca se trabaja directamente en `main`.
    *   Nuevas funcionalidades: `feature/breve-descripcion`
    *   Corrección de errores: `bugfix/nombre-del-error`
*   **Mensajes de Commit:** Seguirán la convención "Semantic Commits" para rastrear los cambios automáticamente:
    *   `feat: agregar autenticación por GitHub`
    *   `fix: resolver caída del servidor al subir archivos vacíos`
    *   `docs: actualizar diccionario de datos`
*   **Entregables empaquetados:** Si por rúbrica o respaldo se requieren archivos físicos, el formato estricto de empaquetado es:
    `[NOMBRE_PROYECTO]_[MODULO]_[YYYYMMDD]_[HHMM].zip` 
    (Ejemplo: `AnalizadorEstatico_Core_20260612_1530.zip`).

## 4. Procedimientos y Funciones definidos por el Usuario
En arquitecturas modernas basadas en micro-frameworks (FastAPI) y ORMs (SQLAlchemy), la lógica transaccional y procedimental que históricamente recaía en la Base de Datos (Stored Procedures, Triggers), se traslada a la **Capa de Servicios y Core**. Esto asegura que la base de datos sea agnóstica y todo el código sea testeable.

### 4.1. Flujos Transaccionales (Reemplazo de SPs)
Manejan el flujo completo de vida de un dato (Insert, Update, Delete) garantizando su consistencia. Se implementan en clases de tipo "Service".
*   **Atomicidad (BEGIN / COMMIT / ROLLBACK):** Cada operación transaccional abre una sesión de base de datos. Si todos los pasos se cumplen, se hace `session.commit()`. Si falla una validación de negocio intermedia o hay un error de conexión, el sistema captura el error y lanza un `session.rollback()` automático para mantener la integridad de las tablas.

### 4.2. Funciones Definidas por el Usuario (UDFs) - Lógica y Consultas
Se dividen en la capa Core de Negocios y la capa de Acceso a Datos.

#### 4.2.1. Funciones Escalares (Funciones Puras)
Ubicadas en la carpeta `motor_analisis/`. Reciben parámetros de entrada, procesan cálculos complejos (ej. conteo de nodos AST, cálculo de complejidad ciclomática) y retornan un único valor o diccionario escalar.
*   **Regla de Oro:** Son funciones sin "efectos secundarios" (Side-effects free). No modifican la base de datos, no envían correos, ni alteran variables globales. Solo calculan y devuelven.

#### 4.2.2. Funciones de Tabla (Repositorios y Vistas)
Ubicadas en la carpeta `persistencia/repositories/`. Consisten en consultas complejas diseñadas para extraer conjuntos de datos.
*   Actúan como "Vistas" programáticas. 
*   **Propósito:** Filtrar historiales de usuario, generar reportes paginados de auditoría o cruzar datos entre la tabla `users` y `analysis_reports` utilizando métodos como `session.query().join().filter()`, retornando siempre listas de objetos tipados (`list[Model]`).

## 5. Beneficios
La adherencia estricta a este estándar de programación aporta las siguientes ventajas clave:
*   **Calidad de Código y Legibilidad:** Las convenciones PEP 8 y el Type Hinting hacen que el código sea auto-documentado, reduciendo la fricción para que cualquier integrante del equipo lea, entienda y modifique funciones desarrolladas por otros.
*   **Prevención Temprana de Errores:** Al validar tipos estáticos antes del despliegue y al usar bloques de transacciones controladas (Rollbacks), el número de errores en producción (bugs críticos) se reduce hasta en un 60%.
*   **Mantenimiento y Escalabilidad:** Al utilizar la Arquitectura Limpia, si en el futuro se desea cambiar la base de datos (de SQLite a PostgreSQL) o el frontend, el impacto en el *Motor de Análisis Core* es cero. 
*   **Auditoría y Seguridad:** Todos los accesos quedan documentados sistemáticamente sin requerir triggers ocultos en la base de datos, ofreciendo transparencia técnica total.

## 6. Conclusiones
La programación no es solo dar instrucciones a una máquina, sino comunicarse con otros desarrolladores. La implementación de este **Estándar de Programación** trasciende el cumplimiento académico; se posiciona como el pilar fundamental que transforma un código de nivel estudiante en un **producto de software de nivel profesional, mantenible, escalable y robusto**. El seguimiento riguroso de estas directrices garantiza la integridad del sistema a largo plazo, consolidando un entorno de trabajo colaborativo altamente eficiente.
