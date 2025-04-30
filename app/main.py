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

@app.on_event("startup")
async def startup_event():
    await data_loader.fetch_csv()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    table_html, dataframe_size = await data_loader.get_data_html()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    countries = await data_loader.get_countries_list()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": table_html,
        "dataframe_size": dataframe_size,
        "current_time": current_time,
        "countries": countries
    })

@app.get("/refresh")
async def refresh_data():
    await data_loader.fetch_csv()
    return {"message": "Data updated successfully"}

@app.get("/api/yearly-birth-rates")
async def get_yearly_birth_rates():
    data = await data_loader.get_birth_rate_by_year()
    return JSONResponse(content=data)

@app.get("/api/top-countries")
async def get_top_countries(year: int = None, top_n: int = 10, lowest: bool = False):
    data = await data_loader.get_top_countries_by_birth_rate(
        year=year, 
        top_n=top_n, 
        ascending=lowest
    )
    return JSONResponse(content=data)

@app.get("/api/country-trend/{country_name}")
async def get_country_trend(country_name: str):
    data = await data_loader.get_country_trend(country_name)
    return JSONResponse(content=data)

@app.get("/api/comparative-data")
async def get_comparative_data(
    reference: str = "Colombia", 
    countries: str = None,
    latest_only: bool = False
):
    comparison_countries = countries.split(",") if countries else None
    data = await data_loader.get_comparative_data(
        reference_country=reference,
        comparison_countries=comparison_countries,
        latest_only=latest_only
    )
    return JSONResponse(content=data)