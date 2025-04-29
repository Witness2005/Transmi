import pandas as pd

import aiohttp

import asyncio

import io

#soy gay
class DataLoader:

    def __init__(self):

        self.dataframe = pd.DataFrame()


    async def fetch_csv(self):

        CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"

        async with aiohttp.ClientSession() as session:

            async with session.get(CSV_URL) as resp:

                if resp.status == 200:

                    content = await resp.read()

                    self.dataframe = pd.read_csv(io.BytesIO(content))

                    print(f"Data loaded successfully, DataFrame size: {len(self.dataframe)}")

                else:

                    print(f"Error downloading data: {resp.status}")


    async def get_data_html(self):

        if self.dataframe.empty:

            return "<p>No data available.</p>", 0

        else:

            df = self.dataframe.head(100)  # Show only the first 100 records

            table_html = df.to_html(classes="table table-striped table-bordered table-hover", 

                                     index=False, 

                                     border=0,

                                     justify="center")

            return table_html, len(self.dataframe)