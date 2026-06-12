![./media/logo-upt.png](./media/logo-upt.png)

__UNIVERSIDAD PRIVADA DE TACNA__

__FACULTAD DE INGENIERÍA__

__Escuela Profesional de Ingeniería de Sistemas__

__Proyecto Analizador Estático de Código con Métricas__

__Curso: Calidad y Pruebas de Software__

__Docente: Mag\. Patrick Cuadros Quiroga__

Integrantes:

__*Ramos Atahuachi, Fabricio Farid Edmilson \(2023076798\)*__

__*Colque Quispe, Rodrigo Sídney \(2023077078\)*__

__Tacna – Perú__

__*2026*__

CONTROL DE VERSIONES

Versión

Hecha por

Revisada por

Aprobada por

Fecha

Motivo

1\.0

RF

PCQ

PCQ

01/05/2026

Versión Original

Sistema de Analizador Estático de Código con Métricas

Versión *\{1\.0\}*

CONTROL DE VERSIONES

Versión

Hecha por

Revisada por

Aprobada por

Fecha

Motivo

1\.0

MPV

ELV

ARV

10/10/2020

Versión Original

ÍNDICE GENERAL

[__1\. Antecedentes	4__](#_aui1eswuynyu)

[__2\. Planteamiento del Problema	4__](#_5hxbzr7m7sjg)

[2\.1\. Problema	4](#_zbt56v4g2htp)

[2\.2\. Justificación	4](#_o9sagyd31i73)

[2\.3\. Alcance	4](#_y6dto4doo1mt)

[__3\. Objetivos	4__](#_1iu92hduvb8e)

[3\.1\. General	4](#_wdcsn4ytxi9y)

[3\.2\. Específicos	5](#_983wv6gnubm9)

[__4\. Marco Teórico	5__](#_q32njbspks0j)

[__5\. Desarrollo de la Solución	5__](#_q40hq4yadow7)

[5\.1\. Análisis de Factibilidad	5](#_6xfmsswi9qqi)

[5\.2\. Tecnología de Desarrollo	5](#_hadm2adm7guk)

[5\.3\. Metodología de Implementación \(Documento de Visión, SRS, SAD\)	5](#_2i0siyvujcdg)

[__6\. Cronograma	5__](#_ky5a5rkbvak0)

[__7\. Presupuesto	5__](#_s1zk58pbw2st)

[__8\. Conclusiones	5__](#_wm7pb926mff5)

[__9\. Recomendaciones	5__](#_etop304u6u0z)

[__10\. Bibliografía	5__](#_r2wl4p1pt1k9)

[__11\. Anexos	5__](#_i0mbzwtqshb2)

# <a id="_aui1eswuynyu"></a>Antecedentes

En la actualidad, el desarrollo de software es un proceso colaborativo y dinámico que exige la constante modificación y evolución del código fuente\. A medida que los proyectos crecen, es común que la calidad del código se degrade si no se aplican prácticas adecuadas de revisión, generando lo que se conoce como "deuda técnica"\. Herramientas de análisis estático comerciales y de código abierto \(como SonarQube o ESLint\) han demostrado ser fundamentales para mitigar este problema en la industria\. Sin embargo, estas herramientas empresariales suelen requerir configuraciones complejas, servidores dedicados y consumen una cantidad considerable de recursos\. En el ámbito académico y en equipos de desarrollo ágil que buscan soluciones rápidas, existe la necesidad de contar con plataformas ligeras y accesibles que brinden retroalimentación inmediata sobre la calidad estructural del código y la presencia de malos olores \(code smells\) sin la necesidad de desplegar infraestructuras pesadas\.

# <a id="_5hxbzr7m7sjg"></a>Planteamiento del Problema

## <a id="_zbt56v4g2htp"></a>Problema

- Los equipos de desarrollo y estudiantes de ingeniería de software a menudo enfrentan dificultades para mantener un código limpio y estructurado\. La falta de control sobre métricas como la complejidad ciclomática, la longitud excesiva de los métodos o el número desproporcionado de parámetros \(Code Smells\) resulta en sistemas difíciles de mantener, propensos a errores y costosos de escalar\. La carencia de una herramienta de análisis rápida, centralizada y de fácil acceso que consolide estos reportes visualmente, dificulta que los programadores puedan evaluar la evolución temporal y el impacto de la deuda técnica en sus proyectos\.

## <a id="_o9sagyd31i73"></a>Justificación

- El desarrollo del "Analizador Estático de Código" se justifica por la necesidad de proveer a los desarrolladores una herramienta automatizada e intuitiva que promueva las buenas prácticas de programación\. Al automatizar la extracción de métricas estructurales \(LOC, NOM, NOA, NPM\) y la detección de Code Smells específicos en lenguajes populares \(Java, C\#, Python\), se reduce drásticamente el tiempo de revisión manual\. Además, la incorporación de un Dashboard visual con el historial de análisis permite observar empíricamente si la calidad del código está mejorando o empeorando con cada iteración, facilitando la toma de decisiones preventivas antes de que la deuda técnica sea insostenible\.

## <a id="_y6dto4doo1mt"></a>Alcance

El proyecto abarca el diseño, desarrollo e implementación de una aplicación web funcional con las siguientes delimitaciones:

- Lenguajes Soportados: Análisis exclusivo de código fuente escrito en Java, C\# y Python\.
- Métricas a evaluar: Líneas de Código \(LOC\), Líneas de Comentarios \(CLOC\), Complejidad Ciclomática, Número de Métodos \(NOM\), Número de Métodos Públicos \(NPM\) y Número de Atributos \(NOA\)\.
- Detección de Code Smells: Se limitará a la identificación de "Long Method" \(métodos que excedan las 50 líneas\) y "Long Parameter List" \(métodos con más de 5 parámetros\)\.
- Entradas: El sistema aceptará la carga de archivos locales individuales o el análisis de repositorios públicos mediante URLs de GitHub\.
- Visualización: Se incluye un Dashboard con gráficos estadísticos \(Chart\.js\) y persistencia del historial por usuario, con capacidad de exportación a CSV\.
- Limitaciones: El sistema realiza un análisis puramente estático \(lexical y sintáctico mediante expresiones regulares y árboles AST\); no compila ni ejecuta el código \(análisis dinámico\), ni tampoco corrige automáticamente los errores encontrados\.

# <a id="_1iu92hduvb8e"></a>Objetivos

## <a id="_wdcsn4ytxi9y"></a>General

Desarrollar una aplicación web para el análisis estático de código fuente que permita evaluar métricas de calidad de software, detectar deuda técnica y visualizar la evolución histórica de proyectos desarrollados en Java, C\# y Python\.

## <a id="_983wv6gnubm9"></a>Específicos

- Implementar un motor de análisis backend en Python que utilice árboles de sintaxis abstracta \(AST\) y expresiones regulares para procesar y desglosar el código fuente de manera precisa\.
- Desarrollar algoritmos de cálculo para extraer métricas estructurales clave \(LOC, CLOC, Complejidad Ciclomática, NOM, NOA, NPM\)\.
- Automatizar la detección de Code Smells estableciendo umbrales de advertencia para parámetros extensos \("Long Parameter List"\) y métodos sobredimensionados \("Long Method"\)\.
- Construir una interfaz de usuario interactiva y responsiva que integre la ingesta de código \(archivos y repositorios de GitHub\) y presente los resultados de forma amigable\.
- Diseñar un Dashboard de evolución técnica que genere gráficos comparativos y almacene el historial de los análisis de cada usuario en una base de datos relacional para su posterior consulta y exportación\.

# <a id="_q32njbspks0j"></a>Marco Teórico

## <a id="_9vw5q2hj6j61"></a>Análisis Estático de Código

El análisis estático de código es el proceso de evaluar un programa informático sin necesidad de ejecutarlo\. Se realiza directamente sobre el código fuente para encontrar errores tempranos, vulnerabilidades de seguridad y asegurar el cumplimiento de estándares de codificación\. A diferencia del análisis dinámico \(que requiere compilación y un entorno de ejecución\), el estático es extremadamente rápido y permite una revisión exhaustiva de las ramificaciones lógicas del software\.

## <a id="_ov1ibpprg23"></a>Métricas de Calidad de Software

Las métricas estructurales permiten cuantificar la complejidad y la mantenibilidad de un programa:

- Líneas de Código \(LOC\): Medida básica que cuenta la cantidad de instrucciones\. Ayuda a dimensionar el tamaño de una clase o archivo\.
- Líneas de Comentarios \(CLOC\): Indica qué tan documentado está el código\.
- Complejidad Ciclomática \(McCabe\): Mide la cantidad de caminos linealmente independientes dentro de un fragmento de código \(usualmente contando sentencias de control como if, for, while, catch\)\. Una complejidad alta indica que el código es difícil de probar y propenso a errores\.
- Métricas Orientadas a Objetos:
	- NOM \(Number of Methods\): Cantidad de métodos en una clase\.
	- NPM \(Number of Public Methods\): Métodos expuestos públicamente\.
	- NOA \(Number of Attributes\): Cantidad de variables/propiedades de estado en la clase\.

## <a id="_9tsbedcz7yyo"></a>Deuda Técnica y Code Smells

La "Deuda Técnica" es una metáfora que describe el costo implícito de un rediseño futuro provocado por haber elegido una solución fácil pero limitada en el presente\. Los Code Smells \(malos olores de código\) son síntomas en el código fuente que posiblemente indican un problema más profundo en el diseño\.

- Long Method: Métodos demasiado extensos \(en nuestro caso, definidos como >50 líneas\) que rompen el principio de responsabilidad única\.
- Long Parameter List: Funciones que requieren más de 5 parámetros, lo cual las hace difíciles de comprender, usar y probar\.

## <a id="_gnbyh3mwmvy"></a>Árboles de Sintaxis Abstracta \(AST\)

Un AST es una representación en forma de árbol de la estructura sintáctica del código fuente\. Los analizadores modernos parsean el texto plano del código y lo transforman en un AST, permitiendo navegar jerárquicamente por clases, funciones y variables de forma determinista, siendo mucho más preciso que las simples búsquedas por expresiones regulares\.

# <a id="_q40hq4yadow7"></a>Desarrollo de la Solución

## <a id="_6xfmsswi9qqi"></a>Análisis de Factibilidad

- Factibilidad Técnica: El desarrollo es completamente viable\. Existen librerías nativas \(ast en Python\) y de terceros \(javalang para Java\) maduras que permiten la generación de árboles sintácticos\. El procesamiento de expresiones regulares de alto rendimiento permite la extracción de métricas en lenguajes estructurados\.
- Factibilidad Económica: El proyecto utiliza tecnologías Open Source y frameworks gratuitos \(Python, Bootstrap, Chart\.js\)\. Por lo tanto, el costo de licenciamiento de software es nulo\. El costo principal radica únicamente en las horas\-hombre invertidas en el desarrollo\.
- Factibilidad Operativa: La herramienta está diseñada como una aplicación web \(cliente\-servidor\)\. Esto garantiza que los desarrolladores finales no requieran instalaciones complejas en sus máquinas locales; basta con tener un navegador moderno\.

## <a id="_hadm2adm7guk"></a>Tecnología de Desarrollo

El proyecto adopta una arquitectura multicapa \(Presentación, Negocios, Persistencia y Motor de Análisis\) utilizando las siguientes tecnologías:

- Backend \(Servidor y API\): Python \(se asume uso de FastAPI o Flask para manejar subidas asíncronas\)\. Python se eligió por su excelente capacidad para manipulación de textos \(regex\) y librerías AST\.
- Motor de Análisis Estático: Módulos integrados re \(Expresiones regulares\), ast \(para análisis léxico de Python\) y javalang \(parser de Java\)\.
- Frontend \(Interfaz de Usuario\): HTML5 Semántico, CSS3 estructurado mediante el framework Bootstrap 5 \(para responsividad y diseño de tarjetas glassmorphism\), y JavaScript Vanilla\.
- Visualización de Datos: Librería Chart\.js para la renderización de gráficos dinámicos \(líneas y barras\) del dashboard de evolución\.
- Base de Datos / Persistencia: Base de datos relacional para guardar métricas por usuario, identificadores, repositorios analizados y el histórico de deuda técnica\.

## <a id="_2i0siyvujcdg"></a>Metodología de Implementación \(Documento de Visión, SRS, SAD\)

Se implementó mediante un ciclo de vida ágil/iterativo para asegurar entregas funcionales\. La documentación sigue lineamientos estándar de ingeniería de software:

- Documento VISION: Establece el alcance general, los stakeholders y la promesa de valor: proveer retroalimentación instantánea de la calidad del código\.
- Documento SRS \(Software Requirements Specification\): Define rigurosamente las reglas de negocio \(ej\. cómo calcular la complejidad, límite de parámetros, soporte a ZIPs de GitHub\) y casos de uso del usuario y administrador\.
- Documento SAD \(Software Architecture Document\): Detalla el flujo de datos desde que el cliente sube un archivo local hasta que el motor backend lo parsea, calcula el AST, extrae los code smells y persiste el resultado en la base de datos para la generación estadística\.

# <a id="_ky5a5rkbvak0"></a>Cronograma

A continuación se presenta un cronograma estimado de las iteraciones de desarrollo del proyecto, dividido en semanas:

| Fase | Actividad Principal | Duración Estimada | Entregables |
| :--- | :--- | :--- | :--- |
| Fase 1: Planificación y Diseño | Levantamiento de Requerimientos (SRS, VISION). Diseño de interfaces (Wireframes). Definición de Arquitectura (SAD). | Semana 1 | Documentos VISION, SRS, SAD. Prototipos de UI. |
| Fase 2: Motor Core (Backend) | Desarrollo del motor de análisis en Python. Integración de ast para Python y javalang para Java. Creación de Expresiones Regulares para C#. | Semanas 2 y 3 | Módulo services.py con analyze_code. Detección de Code Smells. |
| Fase 3: Desarrollo Web / API | Creación de endpoints de subida (/upload y /github). Implementación de la capa de persistencia y modelos de BD. | Semana 4 | API funcional conectada a Base de Datos. Funciones de guardado. |
| Fase 4: Frontend y Dashboard | Maquetado HTML/CSS con Bootstrap. Conexión de UI con API. Integración de Chart.js para histórico de evolución. | Semana 5 | Vistas de Subida, Dashboard Interactivo y Comparador de Archivos (A vs B). |
| Fase 5: Pruebas y Cierre | Pruebas unitarias de parsing, pruebas de carga de repositorios pesados en ZIP. Generación del informe FD05. | Semana 6 | Aplicación estable, manuales y presentación final. |

# <a id="_s1zk58pbw2st"></a>Presupuesto

Dado que el proyecto fue desarrollado en un entorno académico, el costo principal recae en las horas\-hombre dedicadas a la investigación y codificación\. El uso de tecnologías de código abierto ha reducido los costos de licenciamiento a cero\. A continuación se presenta un presupuesto referencial \(estimado\) del proyecto:

| Categoría | Descripción / Recurso | Cantidad | Costo Unitario Estimado (S/.) | Total (S/.) |
| :--- | :--- | :--- | :--- | :--- |
| **Software** | Python, FastAPI, Bootstrap 5, Chart.js, GitHub | N/A (Open Source) | S/. 0.00 | S/. 0.00 |
| **Hardware** | Depreciación por uso de Laptops personales de desarrollo | 1 - 2 equipos | S/. 150.00 (por mes) | S/. 300.00 |
| **Recursos Humanos** | Rol: Desarrollador / Analista (Horas invertidas estimadas) | 80 horas | S/. 25.00 / hora | S/. 2,000.00 |
| **Servicios** | Internet y consumo eléctrico proporcional | 1.5 meses | S/. 80.00 / mes | S/. 120.00 |
| | | | **Total Estimado** | **S/. 2,420.00** |

# <a id="_wm7pb926mff5"></a>Conclusiones

- Cumplimiento de Objetivos: Se logró desarrollar e implementar con éxito una aplicación web funcional capaz de realizar un análisis estático profundo sobre código fuente escrito en lenguajes populares como Java, C\# 		y Python, cumpliendo con todos los objetivos planteados inicialmente\.
- Eficacia del Análisis Estático: Se demostró que la combinación de parsing nativo \(mediante el módulo ast para Python y javalang para Java\) junto con expresiones regulares optimizadas \(para C\#\), constituye un enfoque altamente performante\. Permite extraer métricas estructurales complejas sin la necesidad de compilar los proyectos\.
- Visibilidad de la Deuda Técnica: La detección automatizada de Code Smells específicos, como métodos excesivamente largos \(Long Method\) o listas de parámetros desproporcionadas \(Long Parameter List\), ha comprobado ser una herramienta eficaz para alertar a los programadores sobre malas prácticas de diseño en tiempo real\.
- Valor de la Visualización: La integración de un Dashboard interactivo con Chart\.js superó las expectativas en cuanto a experiencia de usuario, permitiendo a los desarrolladores comprender fácilmente si la complejidad ciclomática de sus proyectos está aumentando o disminuyendo con el tiempo, fomentando la refactorización continua\.

# <a id="_etop304u6u0z"></a>Recomendaciones

- Soporte a Nuevos Lenguajes: Se recomienda extender el motor de análisis en futuras versiones para incluir soporte a lenguajes altamente demandados en desarrollo web, tales como JavaScript, TypeScript y PHP, utilizando sus respectivos parsers AST\.
- Ampliación de Reglas de "Code Smells": Sugerimos implementar algoritmos para detectar otros malos olores estructurales comunes, tales como Large Class \(Clases con demasiadas responsabilidades/métodos\), God Object y la detección de código duplicado \(Copy\-Paste\)\.
- Containerización y Despliegue: Para facilitar su distribución y asegurar que funcione exactamente igual en cualquier entorno, se recomienda empaquetar la solución completa utilizando contenedores de Docker\. Posteriormente, se podría considerar alojar la aplicación en un servicio Cloud \(como AWS o Heroku\) para ofrecerla como Software as a Service \(SaaS\)\.
- Integración Continua \(CI/CD\): A futuro, la herramienta podría proporcionar un endpoint o un "Webhook" para integrarse directamente a los pipelines de GitHub Actions o Jenkins\. De esta manera, se bloquearían los commits o Pull Requests de forma automática si el código no supera los umbrales mínimos de calidad y complejidad estipulados\.	

# <a id="_r2wl4p1pt1k9"></a>Bibliografía

- Fowler, M\. \(1999\)\. Refactoring: Improving the Design of Existing Code\. Addison\-Wesley\.
- McCabe, T\. J\. \(1976\)\. A Complexity Measure\. IEEE Transactions on Software Engineering\.
- Anexos: Documento VISION, Documento SRS, SAD y Capturas de pantalla de tu Dashboard funcionando \(incluyendo la advertencia del "Long method" que corregimos hoy\)\.

# <a id="_i0mbzwtqshb2"></a>Anexos

## <a id="_ket0cpj5va0w"></a>Anexo 01: Informe de Factibilidad

- Factibilidad Técnica: El proyecto es altamente factible desde el punto de vista tecnológico\. Se validó la capacidad de extraer métricas sin necesidad de compilar mediante el uso de Árboles de Sintaxis Abstracta \(módulo ast nativo en Python y librería javalang para Java\) y el uso de expresiones regulares \(módulo re\) para C\#\. Las capacidades de procesamiento concurrente permiten descargar y desempaquetar archivos ZIP de GitHub \(urllib, zipfile\) eficientemente\.
- Factibilidad Económica: Viabilidad del 100%\. Las herramientas base utilizadas \(Python, HTML, JS, Bootstrap, Chart\.js\) son de código abierto \(gratuitas\)\. El alojamiento local para desarrollo no representa costos\. El único valor es el tiempo invertido por los desarrolladores\.
- Factibilidad Operativa: El sistema es accesible y de rápida adopción\. Al tener una interfaz web, cualquier usuario puede utilizarlo sin conocimientos previos de despliegue ni necesidad de instalar dependencias locales pesadas, mitigando la curva de aprendizaje frente a herramientas como SonarQube\.

## <a id="_hzwdq7qfu182"></a>Anexo 02: Resumen del Documento de Visión

Planteamiento del Problema: Los estudiantes y equipos de desarrollo de software pierden agilidad y calidad debido a la acumulación de deuda técnica oculta en el código \(mala estructuración, métodos gigantes, demasiados parámetros\)\.

Solución Propuesta: Un "Analizador Estático de Código" en plataforma web que automatiza la inspección estructural de programas en Java, C\# y Python, brindando retroalimentación visual inmediata mediante dashboards\.

Perfiles de Usuarios \(Stakeholders\):

- Desarrolladores/Estudiantes: Suben código buscando evaluar la limpieza, modularidad e identificar Code Smells para refactorizar\.
- Líderes Técnicos/Docentes: Pueden visualizar el reporte histórico en CSV o a través de los gráficos del Dashboard para evaluar el progreso o degradación técnica de un proyecto a lo largo del tiempo\.

## <a id="_trxwf8q9wwh4"></a>Anexo 03: Resumen del Documento SRS \(Especificación de Requisitos\)

Requisitos Funcionales \(RF\):

- RF\-01: El sistema debe permitir la subida individual de archivos con extensiones \.java, \.cs y \.py\.
- RF\-02: El sistema debe permitir el escaneo masivo ingresando una URL pública de un repositorio de GitHub\.
- RF\-03: El sistema debe calcular y mostrar las métricas: LOC, CLOC, Complejidad Ciclomática, NOM \(Métodos\), NPM \(Públicos\) y NOA \(Atributos\)\.
- RF\-04: El sistema debe emitir alertas descriptivas \(Code Smells\) si un método excede 50 líneas \(Long Method\) o recibe más de 5 parámetros \(Long Parameter List\)\.
- RF\-05: El sistema debe almacenar el resultado en la cuenta del usuario para graficar la evolución histórica de su complejidad\.

Requisitos No Funcionales \(RNF\):

- RNF\-01 \(Desempeño\): El análisis de archivos individuales debe procesarse en tiempo real \(< 2 segundos\)\.
- RNF\-02 \(Usabilidad\): La interfaz debe ser intuitiva y responsiva \(Mobile\-First\) gracias a Bootstrap 5\.

## <a id="_j9jasptnsef1"></a>Anexo 04: Resumen del Documento SAD \(Arquitectura\)

La aplicación sigue un Patrón de Arquitectura por Capas combinado con un enfoque de arquitectura Cliente\-Servidor\.

- Capa de Presentación \(Frontend\): Vistas estáticas \(dashboard\.html\) alimentadas por JavaScript asíncrono \(API REST Fetch\) para actualizar los componentes visuales e instanciar Chart\.js\.
- Capa de Negocio \(Backend\): Módulo Coordinador \(AnalysisCoordinator\) que orquesta las peticiones, desempaqueta los archivos de GitHub y prepara los payloads JSON\.
- Capa del Motor Core \(Análisis\): Archivo services\.py, encargado de instanciar los parsers AST, ejecutar el balanceo de llaves para C\# y generar las listas de "Code Smells"\.
- Capa de Persistencia: Módulo AnalysisRepository conectado a una base de datos relacional para el registro de los reportes por user\_id\.

## <a id="_3e624ibf26zs"></a>Anexo 05: Resumen de Manuales \(Guía Rápida de Usuario\)

Flujo de Trabajo Básico:

- Ingreso: El usuario inicia sesión y es dirigido al Dashboard principal\.
- Análisis Local: En la pestaña "Archivo Local", selecciona un archivo \.java, \.cs o \.py desde su PC y presiona "Analizar y Guardar"\.
- Análisis por Repositorio: En la pestaña "Repositorio GitHub", pega la URL del proyecto y presiona "Analizar Repositorio"\.
- Visualización de Resultados:
	- La zona central mostrará los gráficos actualizados de Histórico LOC vs Complejidad \(Evolución temporal en línea\) y Estructura del Último Análisis \(Gráfico de barras NOM, NPM, NOA\)\.
	- En la tabla inferior \("Detalle por Archivos"\), el usuario puede dar Clic Izquierdo sobre un archivo analizado para visualizar sus problemas detallados en el "Archivo A", y Clic Derecho en otro para hacer una comparativa en el "Archivo B"\.
- Exportación: Presionar el botón verde "Exportar Historial a CSV" descargará un archivo excel\-compatible con el histórico para reportes formales\.

