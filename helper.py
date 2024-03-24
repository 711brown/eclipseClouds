import xarray as xr
from datetime import datetime, timezone, timedelta
import os.path
import requests 
from requests.exceptions import HTTPError


def adjust_longitude(dataset: xr.Dataset) -> xr.Dataset:
    """Swaps longitude coordinates from range (0, 360) to (-180, 180)
    Args:
        dataset (xr.Dataset): xarray Dataset
    Returns:
        xr.Dataset: xarray Dataset with swapped longitude dimensions
    """
    lon_name = "longitude"  # whatever name is in the data

    # Adjust lon values to make sure they are within (-180, 180)
    dataset["_longitude_adjusted"] = xr.where(
        dataset[lon_name] > 180, dataset[lon_name] - 360, dataset[lon_name]
    )
    dataset = (
        dataset.swap_dims({lon_name: "_longitude_adjusted"})
        .sel(**{"_longitude_adjusted": sorted(dataset._longitude_adjusted)})
        .drop(lon_name)
    )

    dataset = dataset.rename({"_longitude_adjusted": lon_name})
    return dataset

def get_closest_model_run():
    currentTime = datetime.now(timezone.utc)
    deltaHour = currentTime.hour % 6
    return (currentTime - timedelta(hours=deltaHour)).replace(minute=0, second=0, microsecond=0)

def get_eclipse_forecast_hour(model_run_time):
    eclipseDate = datetime(2024, 4, 8, 18, 0, 0, tzinfo=timezone.utc)
    return (eclipseDate - model_run_time).days * 24

def download_gfs(modelDateTime, forecastHour):
    modelRunYear = modelDateTime.strftime('%Y')
    modelRunMonth = modelDateTime.strftime('%m')
    modelRunDay = modelDateTime.strftime('%d')
    modelRunHour = modelDateTime.strftime('%H')
    forecastHourPadded = str(forecastHour).zfill(3)

    outputFileName = f'{modelRunYear}{modelRunMonth}{modelRunDay}{modelRunHour}{forecastHourPadded}.grib'

    if not os.path.isfile(outputFileName):
        print('Must Download')
        url = f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{modelRunYear}{modelRunMonth}{modelRunDay}/{modelRunHour}/atmos/gfs.t{modelRunHour}z.pgrb2.0p25.f{forecastHourPadded}'
        print(url)
        session = requests.Session()
        try: 
            response = session.get(url)
            response.raise_for_status
            with open(outputFileName, 'wb') as f:
                f.write(response.content)
        except HTTPError:
            print('Failed to download!')
            raise Exception('Data not downloaded -- may not be ready')

    else: 
        print('Already Downloaded File')
    return outputFileName

