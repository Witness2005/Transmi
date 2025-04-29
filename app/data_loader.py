import pandas as pd

import aiohttp

import asyncio

import io


async def fetch_csv():

    CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"

    async with aiohttp.ClientSession() as session:

        async with session.get(CSV_URL) as resp:

            if resp.status == 200:

                content = await resp.read()

                try:

                    df = pd.read_csv(io.BytesIO(content))

                    print(f"Data loaded successfully, DataFrame size: {len(df)}")

                except Exception as e:

                    print(f"Error processing CSV data: {e}")

            else:

                print(f"Error downloading data: {resp.status}")


asyncio.run(fetch_csv())