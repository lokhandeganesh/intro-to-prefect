# import json

import httpx

# import pandas as pd
import polars as pl
from prefect import flow, task
from prefect.artifacts import create_table_artifact

# from utils.logger import logger

csv_data_path = "src/102/weather-data.csv"


@task(name="fetch-weather", log_prints=True)
def fetch_weather(
    lat: float = 17.51, lon: float = 74.51,
    parameter: str = "temperature_2m"
):
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
        df = pl.from_dict(weather.json()["hourly"])
        return df


@task
def inspect_and_log_data(df: pl.DataFrame):
    df_preview = df.head(10)

    table_data = df_preview.to_dict(as_series=False)

    create_table_artifact(
        key="weather-data-preview",
        table=table_data,
        description="Preview of the weather data fetched from the API",
    )


@task(name="save-weather", log_prints=True)
def save_weather(df: pl.DataFrame, path: str = csv_data_path):
    df.write_csv(path)
    return f"Weather data saved to CSV at {path}"


@flow(name="fetch-weather-pipeline", log_prints=True)
def pipeline(
    lat: float = 17.51, lon: float = 74.51,
    parameter: str = "temperature_2m"
):

    df = fetch_weather(lat, lon, parameter)

    # create table artifact in UI
    inspect_and_log_data(df)
    # logger.info("Weather data fetched successfully")

    # saving DataFrame to CSV
    save_weather(df)


    return "Weather flow run successfully"


if __name__ == "__main__":
    # fetch_weather.serve(name="deploy-1")
    pipeline()
