from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from app.data_loader import DataLoader

from datetime import datetime


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

data_loader = DataLoader()


@app.on_event("startup")

async def startup_event():

    await data_loader.fetch_csv()


@app.get("/", response_class=HTMLResponse)

async def home(request: Request):

    table_html, dataframe_size = await data_loader.get_data_html()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    

    return templates.TemplateResponse("index.html", {

        "request": request,

        "table": table_html,

        "dataframe_size": dataframe_size,

        "current_time": current_time

    })


@app.get("/refresh")

async def refresh_data():

    await data_loader.fetch_csv()

    return {"message": "Data updated successfully"}