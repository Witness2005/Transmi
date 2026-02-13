# 🌍 Global Birth Rate Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-High_Performance-009688)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-FF6384)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

**Global Birth Rate Analysis Dashboard** is a high-performance web application designed to visualize, analyze, and compare birth rate trends worldwide. Leveraging historical data from *Our World in Data*, the application provides interactive insights at global, continental, and national levels.

This project features a modern architecture using **FastAPI** for a robust, asynchronous backend and **Chart.js** for dynamic, responsive frontend visualizations. Data processing is handled efficiently using **Pandas** and **NumPy**.

## ✨ Key Features

* **📊 Interactive Dashboard:** Real-time visualization of KPIs (Total Records, Countries Analyzed, Highest/Lowest Rates).
* **📈 Trend Analysis:** Comprehensive line charts tracking historical birth rate evolution globally and by continent.
* **🌍 Comparative Tools:** Compare specific countries (e.g., Colombia vs. others) to analyze regional differences.
* **🏆 Dynamic Rankings:** Filterable bar charts displaying top and bottom countries by birth rate for any given year.
* **⚡ Asynchronous Data Loading:** Non-blocking CSV fetching and processing using `aiohttp` for optimal server performance.
* **📱 Responsive Design:** Built with **Bootstrap 5**, ensuring a seamless experience across desktop and mobile devices.

## 🛠️ Tech Stack

### Backend
* **Python**: Core programming language.
* **FastAPI**: Modern, high-performance web framework for building APIs.
* **Pandas & NumPy**: Data manipulation, cleaning, and statistical analysis.
* **AIOHTTP**: Asynchronous HTTP client for fetching external datasets.
* **Jinja2**: Templating engine for server-side rendering.

### Frontend
* **HTML5 / CSS3**: Structure and styling.
* **Bootstrap 5**: UI framework for responsive layout and components.
* **Chart.js**: JavaScript library for interactive data visualization.
* **jQuery**: DOM manipulation and AJAX requests.

<img width="1645" height="950" alt="image" src="https://github.com/user-attachments/assets/2e29ca41-3871-45a9-9fce-b2e88e88f633" />

## 📂 Project Structure

```text
Transmi/
├── app/                  # Código fuente de la aplicación
│   ├── templates/        # Archivos HTML (Frontend)
│   │   └── index.html
│   ├── data_loader.py    # Lógica de carga y procesamiento de datos
│   └── main.py           # Punto de entrada de la API (FastAPI)
├── README.md             # Documentación del proyecto
├── render.yaml           # Configuración para despliegue en Render
└── requirements.txt      # Lista de dependencias
