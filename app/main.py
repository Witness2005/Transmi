from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

import asyncio

from datetime import datetime


from app.data_loader import fetch_csv, DATAFRAME


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")

async def startup_event():

    await fetch_csv()


@app.get("/", response_class=HTMLResponse)

async def home(request: Request):

    if DATAFRAME.empty:

        table_html = "<p>No data available.</p>"

    else:

        df = DATAFRAME.head(100)  # Show only the first 100 records

        table_html = df.to_html(classes="table table-striped table-bordered table-hover", 

                                index=False, 

                                border=0,

                                justify="center")

    

    return templates.TemplateResponse("index.html", {

        "request": request,

        "table": table_html,

        "dataframe_size": len(DATAFRAME),

        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    })


@app.get("/refresh")

async def refresh_data():

    await fetch_csv()

    return {"message": "Data updated successfully"}