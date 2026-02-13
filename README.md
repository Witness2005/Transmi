# 🌍 Global Birth Rate Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-FF6384)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Descripción

**Global Birth Rate Analysis Dashboard** es una aplicación web interactiva diseñada para visualizar, analizar y comparar las tasas de natalidad a nivel mundial. Utilizando datos históricos de *Our World in Data*, la aplicación permite a los usuarios explorar tendencias globales, continentales y nacionales.

El proyecto implementa una arquitectura moderna utilizando **FastAPI** para un backend de alto rendimiento y **Chart.js** para la renderización de gráficos dinámicos en el frontend. El procesamiento de datos se realiza de manera asíncrona con **Pandas** y **AIOHTTP**.

## ✨ Características Principales

* **📊 Tablero Interactivo:** Visualización de KPIs (registros totales, países analizados, tasas máximas/mínimas).
* **📈 Análisis de Tendencias:** Gráficos de línea para ver la evolución histórica de la natalidad a nivel global y por continente.
* **🌍 Comparativa entre Países:** Herramienta para comparar la tasa de natalidad de Colombia (u otro país de referencia) frente a otras naciones.
* **🏆 Rankings Dinámicos:** Visualización de los países con mayores y menores tasas de natalidad, filtrable por año.
* **⚡ Carga de Datos Asíncrona:** Obtención y procesamiento de datos CSV en tiempo real sin bloquear el servidor.
* **📱 Diseño Responsivo:** Interfaz construida con Bootstrap 5, adaptable a diferentes dispositivos.

## 🛠️ Stack Tecnológico

### Backend
* **Python**: Lenguaje principal.
* **FastAPI**: Framework web moderno y rápido para construir APIs.
* **Pandas & NumPy**: Manipulación y limpieza de datos.
* **AIOHTTP**: Cliente HTTP asíncrono para la descarga de datasets.
* **Jinja2**: Motor de plantillas para renderizar el HTML.

### Frontend
* **HTML5 / CSS3**: Estructura y estilos.
* **Bootstrap 5**: Framework CSS para el diseño y componentes de UI.
* **Chart.js**: Librería para la creación de gráficos interactivos.
* **jQuery**: Manipulación del DOM y peticiones AJAX.

## 📂 Estructura del Proyecto

```text
├── app/
│   ├── __init__.py
│   ├── data_loader.py    # Lógica de carga y procesamiento de datos (Clase DataLoader)
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/
│       └── index.html    # Plantilla principal del Dashboard
├── main.py               # Punto de entrada de la aplicación FastAPI
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación
