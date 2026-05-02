# 🔍 Analizador Estático de Código con Métricas

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Backend-Python%203.12%2B-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED.svg)](https://www.docker.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-success.svg)]()

> **Analizador Estático de Código con Métricas** es una plataforma integral diseñada para evaluar la calidad del código fuente mediante técnicas avanzadas de compilación. Implementando una Arquitectura Limpia (Clean Architecture), el sistema tokeniza el código, valida su gramática y construye un Árbol de Sintaxis Abstracta (AST) para calcular métricas de complejidad. Desarrollado como proyecto académico para la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

---

## 📋 Descripción

Este sistema permite a los desarrolladores someter fragmentos de código para auditoría sin necesidad de ejecutarlos. Está estructurado en cuatro capas principales (Presentación, Negocios, Motor Core y Persistencia) lo que garantiza un acoplamiento nulo entre la interfaz web y el motor de análisis puro.

### ✨ Características Principales

| Módulo | Descripción |
|:-------|:------------|
| ⚙️ **Motor de Análisis** | Ejecuta las fases léxica y sintáctica, generando tokens y construyendo el AST en memoria para calcular métricas estáticas. |
| 📊 **Dashboard Interactivo** | Interfaz gráfica (`dashboard.html`) que renderiza estadísticas, gráficos de complejidad y detalla los posibles errores gramaticales detectados. |
| 🛡️ **Arquitectura Limpia** | Separación estricta de responsabilidades mediante coordinadores (`analysis_coordinator.py`) y repositorios, facilitando la escalabilidad y el testing. |
| 🐳 **Despliegue Contenerizado** | Orquestación completa del backend y la base de datos utilizando `docker-compose.yml` para asegurar la portabilidad. |

---

## 🛠️ Tecnologías Utilizadas

El proyecto define sus dependencias en el archivo `requirements.txt` y está preparado para entornos Docker:

*   **Lenguaje Core:** Python 3.12+
*   **Frontend:** HTML5, JS (Renderizado dinámico en cliente)
*   **Orquestación:** Docker & Docker Compose
*   **Arquitectura:** Clean Architecture modular

---

## 🚀 Ejecución del Sistema

Puedes desplegar el proyecto localmente o mediante contenedores. A continuación, el método de ejecución local estándar:

### 1. Instalar dependencias
Asegúrate de tener Python instalado y ejecuta el siguiente comando en la raíz del proyecto para instalar las librerías necesarias:
```bash
pip install -r requirements.txt

## Iniciar la aplicación
Dependiendo del framework configurado en main.py (ej. FastAPI/Flask), inicia el servidor ejecutando el archivo principal de la aplicación:
python app/main.py


##📁 Estructura del Proyecto
proyecto-analizador-estatico/
├── 📂 app/
│   ├── 📄 main.py                     # Punto de entrada de la aplicación
│   ├── 📂 motor_analisis/             # [Capa Core] Lógica pura de evaluación
│   │   ├── 📂 ast/                    # Construcción del Árbol de Sintaxis Abstracta
│   │   ├── 📂 lexical/                # Analizador léxico (Tokenización)
│   │   └── 📂 syntactic/              # Analizador sintáctico
│   ├── 📂 negocios/                   # [Capa de Negocios] Reglas y orquestación
│   │   ├── 📂 security/               # Manejo de autenticación
│   │   └── 📂 services/               # Coordinador de análisis (`analysis_coordinator.py`)
│   ├── 📂 persistencia/               # [Capa de Datos] Acceso a base de datos
│   │   ├── 📂 database/               # Conexiones y dependencias
│   │   ├── 📂 models/                 # Modelos ORM
│   │   └── 📂 repositories/           # Repositorios (`user_repository`, `analysis_repository`)
│   └── 📂 presentacion/               # [Capa Web] Interfaz y controladores
│       ├── 📂 routers/                # Enrutadores de la API (`analysis_router`, `auth_router`)
│       ├── 📂 static/                 # Archivos estáticos (`dashboard.html`, `index.html`)
│       └── 📂 templates/              # Plantillas base
│
├── 📄 docker-compose.yml              # Orquestación de contenedores y servicios
├── 📄 requirements.txt                # Dependencias del proyecto Python
├── 📄 contexto_arq.md                 # Notas de contexto de arquitectura
├── 📄 contexto_req.md                 # Notas de contexto de requerimientos
├── 📂 docs/                           # Documentación formal del proyecto
│   └── 📄 FD01 a FD06 (Informes de Factibilidad, Visión, Requerimientos, Arquitectura, Proyecto Final)
└── 📂 media/                          # Recursos gráficos
    └── 🖼️ logo-upt.png                # Logotipo institucional de la universidad

##👥 Equipo de Desarrollo
Integrantes:
Colque Quispe, Rodrigo Sídney (2023077078)
Ramos Atahuachi, Fabricio Farid Edmilson (2023076798)
Docente: Mag. Patrick Cuadros Quiroga — Curso: Calidad y Pruebas de Software
Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
