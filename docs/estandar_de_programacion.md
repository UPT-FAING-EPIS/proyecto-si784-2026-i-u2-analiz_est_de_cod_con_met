# Estándar de Programación

Este documento establece las reglas, lineamientos y convenciones de codificación para el desarrollo del **Analizador Estático de Código**. El objetivo es mantener un código limpio, legible, mantenible y estandarizado entre todos los miembros del equipo.

## 1. Arquitectura y Estructura del Proyecto
El proyecto implementa los principios de **Clean Architecture**, dividiendo las responsabilidades en capas. 
Ninguna capa interna debe depender de las capas externas. La estructura es:
*   **Capa de Presentación (`app/presentacion/`):** Controladores (Routers de FastAPI), vistas estáticas y plantillas HTML.
*   **Capa de Negocios (`app/negocios/`):** Lógica de negocio y casos de uso (`services`, `security`).
*   **Capa Motor Core (`app/motor_analisis/`):** Lógica pura de evaluación (análisis léxico, sintáctico, y AST). Es el corazón del sistema.
*   **Capa de Persistencia (`app/persistencia/`):** Modelos ORM, repositorios y configuración de la base de datos.

## 2. Convenciones de Nomenclatura (Naming Conventions)

Se sigue estrictamente el estándar **PEP 8** para Python.

### 2.1. Variables, Funciones y Métodos
*   **Formato:** `snake_case` (todo en minúsculas separado por guiones bajos).
*   *Ejemplo Correcto:* `analizar_codigo()`, `project_name`, `user_id`.
*   *Ejemplo Incorrecto:* `AnalizarCodigo()`, `projectName`.

### 2.2. Clases y Excepciones
*   **Formato:** `PascalCase` (cada palabra inicia con mayúscula, sin guiones bajos).
*   *Ejemplo Correcto:* `AnalysisReport`, `UserRepository`, `InvalidSyntaxError`.
*   *Ejemplo Incorrecto:* `analysis_report`, `user_repository`.

### 2.3. Constantes y Variables de Entorno
*   **Formato:** `UPPER_SNAKE_CASE` (todo en mayúsculas separado por guiones bajos).
*   *Ejemplo Correcto:* `MAX_UPLOAD_SIZE`, `SECRET_KEY`, `DATABASE_URL`.
*   *Ejemplo Incorrecto:* `MaxUploadSize`, `secret_key`.

## 3. Tipado Estricto (Type Hinting)

Para mejorar el análisis estático y autocompletado en el IDE, es **obligatorio** definir los tipos de datos de los argumentos y del retorno en todas las funciones y métodos.

```python
# EJEMPLO CORRECTO
def calcular_complejidad(codigo_fuente: str, es_estricto: bool = False) -> int:
    return 10

# EJEMPLO INCORRECTO
def calcular_complejidad(codigo_fuente, es_estricto):
    return 10
```

## 4. Documentación y Comentarios (Docstrings)

Se debe utilizar docstrings triples (`"""`) para documentar módulos, clases y funciones importantes. Se sugiere el estilo de Google o Sphinx.

```python
def tokenizar_codigo(codigo: str) -> list[dict]:
    """
    Analiza el código fuente y genera una lista de tokens.

    Args:
        codigo (str): El código fuente a evaluar.

    Returns:
        list[dict]: Lista de diccionarios representando los tokens.
    """
    pass
```
*   **Regla General:** El código debe ser autodescriptivo. Evita comentarios redundantes como `# Esto suma 1 a i`. Usa los comentarios para explicar el **POR QUÉ** se toma una decisión técnica, no el **QUÉ** hace el código.

## 5. Manejo de Errores y Excepciones
*   No silencies excepciones genéricas usando `except Exception: pass`.
*   Captura excepciones específicas (e.g., `except ValueError:` o `except SQLAlchemyError:`).
*   Lanza excepciones HTTP con mensajes descriptivos en la capa de presentación (Routers de FastAPI).

## 6. Formateo de Código y Calidad (Linter)
*   La longitud máxima de una línea es de **120 caracteres**.
*   Utiliza una herramienta de auto-formateo como **Black** para mantener consistencia.
*   Utiliza **Ruff** o **Flake8** para verificar que no haya "code smells" o violaciones al PEP 8 antes de hacer un commit.

## 7. Control de Versiones (Git)
*   **Mensajes de Commit:** Los mensajes deben estar en infinitivo o presente imperativo y ser claros.
    *   *Correcto:* `Agregar soporte para lectura de archivos .php`
    *   *Incorrecto:* `agregado php` o `cambios en el index`
*   **Ramas (Branches):** Trabaja en ramas específicas para cada funcionalidad (feature branches) antes de hacer "Merge" a `main`. Ej: `feature/analizador-php` o `fix/login-error`.
