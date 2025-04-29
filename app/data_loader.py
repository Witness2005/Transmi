import pandas as pd

import aiohttp

import io


CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"

DATAFRAME = pd.DataFrame()


async def fetch_csv():

    global DATAFRAME

    async with aiohttp.ClientSession() as session:

        async with session.get(CSV_URL) as resp:

            if resp.status == 200:

                content = await resp.read()

                try:

                    df = pd.read_csv(io.BytesIO(content))

                    DATAFRAME = df

                    print(f"Data loaded successfully, DataFrame size: {len(DATAFRAME)}")

                except Exception as e:

                    print(f"Error processing CSV data: {e}")

            else:

                print(f"Error downloading data: {resp.status}")