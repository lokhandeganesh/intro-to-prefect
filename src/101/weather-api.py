# import json

import httpx

# import pandas as pd
import polars as pl
from prefect import flow, task
from prefect.artifacts import create_table_artifact


@task
def inspect_and_log_data(df: pl.DataFrame):
    df_preview = df.head()

    table_data = df_preview.to_dict(as_series=False)

    create_table_artifact(
        key="weather-data-preview",
        table=table_data,
        description="Preview of the weather data fetched from the API",
    )


@flow(name="fetch-weather", log_prints=True)
def fetch_weather(lat: float = 17.51, lon: float = 74.51, parameter: str = "rain", unit: str = "ms"):
    base_url = "https://api.open-meteo.com/v1/forecast/"

    weather = httpx.get(
        base_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": parameter,
        }
    )

    if weather.status_code != 200:
        raise Exception("Failed to fetch the weather data")
    else:
        # df = pd.DataFrame.from_dict(weather.json()["hourly"])
        df = pl.from_dict(weather.json()["hourly"])
        # print(df.head())
        # print(weather.json()["hourly"])

        # Convert to column-oriented JSON without newlines
        # json_data = json.dumps(df.to_dict(as_series=False), separators=(',', ':'))
        # print(json_data)
        # return json_data

        print(
            f"Forecasted rain for time: {weather.json()["hourly"]["time"][0]}",
            f"is: {weather.json()["hourly"]["rain"][0]}"
            )

        inspect_and_log_data(df)

        return weather.json()["hourly"]


if __name__ == "__main__":
    # fetch_weather.serve(name="deploy-1")
    fetch_weather()
