from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.data_loader import DataLoader
from datetime import datetime
import os

app = FastAPI()

# Determine the correct directory structure
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "app", "templates")
static_dir = os.path.join(base_dir, "app", "static")

# Mount static files directory - uncomment if needed
# app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Check for templates directory existence
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    # Fallback to searching in current directory
    templates = Jinja2Templates(directory="templates")

data_loader = DataLoader()

@app.on_event("startup")
async def startup_event():
    # Pre-load data on startup for better performance
    await data_loader.fetch_csv()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Ensure data is loaded
    if data_loader.dataframe.empty:
        success = await data_loader.fetch_csv()
        if not success:
            return HTMLResponse("<h1>Error loading data. Please try again later.</h1>")
    
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
    success = await data_loader.fetch_csv()
    if success:
        return {"status": "success", "message": "Data refreshed"}
    else:
        return {"status": "error", "message": "Failed to refresh data"}

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

# API routes for the additional charts
@app.get("/api/all-countries-latest-year")
async def get_all_countries_latest(limit: int = 50):
    """Returns birth rate data for all countries in the latest available year"""
    data = await data_loader.get_all_countries_latest_year(limit=limit)
    return data

@app.get("/api/continent-trend")
async def get_continent_trend(continent: str = None):
    """Returns birth rate trend by continent"""
    data = await data_loader.get_continent_trend(continent_name=continent)
    return data

@app.get("/api/continents-list")
async def get_continents_list():
    """Returns list of continents available in the dataset"""
    data = await data_loader.get_continents_list()
    return data

# Debugging endpoint to check if FastAPI is running correctly
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "data_loaded": not data_loader.dataframe.empty,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }