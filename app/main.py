from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.data_loader import DataLoader
from datetime import datetime

app = FastAPI()

# Mount static files directory
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

data_loader = DataLoader()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    await data_loader.fetch_csv()
    table, dataframe_size = await data_loader.get_data_html()
    countries = await data_loader.get_countries_list()
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "table": table, 
            "countries": countries,
            "dataframe_size": dataframe_size,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

@app.get("/refresh")
async def refresh_data():
    await data_loader.fetch_csv()
    return {"status": "success", "message": "Data refreshed"}

@app.get("/api/yearly-birth-rates")
async def get_yearly_rates():
    data = await data_loader.get_birth_rate_by_year()
    return data

@app.get("/api/top-countries")
async def get_top_countries(lowest: bool = False, year: int = None):
    if lowest:
        data = await data_loader.get_top_countries_by_birth_rate(year=year, ascending=True)
    else:
        data = await data_loader.get_top_countries_by_birth_rate(year=year)
    return data

@app.get("/api/country-trend/{country_name}")
async def get_country_trend(country_name: str):
    data = await data_loader.get_country_trend(country_name)
    return data

@app.get("/api/comparative-data")
async def get_comparative_data(reference: str = "Colombia", countries: str = None):
    comparison_countries = countries.split(",") if countries else None
    data = await data_loader.get_comparative_data(reference_country=reference, comparison_countries=comparison_countries)
    return data

# Nuevas rutas API para las gráficas adicionales
@app.get("/api/all-countries-latest-year")
async def get_all_countries_latest():
    """Devuelve datos de tasa de natalidad para todos los países en el último año disponible"""
    data = await data_loader.get_all_countries_latest_year()
    return data

@app.get("/api/continent-trend")
async def get_continent_trend(continent: str = None):
    """Devuelve tendencia de tasa de natalidad por continente"""
    data = await data_loader.get_continent_trend(continent_name=continent)
    return data

@app.get("/api/continents-list")
async def get_continents_list():
    """Devuelve la lista de continentes disponibles en el dataset"""
    data = await data_loader.get_continents_list()
    return data