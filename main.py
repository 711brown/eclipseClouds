import cartopy.crs as ccrs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
from cartopy.feature import ShapelyFeature
import xarray as xr
import cartopy.feature as cf
import numpy as np
from helper import adjust_longitude, download_gfs, get_closest_model_run, get_eclipse_forecast_hour

projection = ccrs.Mercator()
crs = ccrs.PlateCarree()


# CONUS
lon_min = -67.0
lon_max = -125.0
lat_min = 50.0
lat_max = 23.0

add_counties = False

plt.figure(dpi=300)
ax = plt.axes(projection=projection, frameon=True)

model_run = get_closest_model_run()
forecast_hour = get_eclipse_forecast_hour(model_run)
data_path = download_gfs(model_run, forecast_hour)



ds = xr.open_dataset(data_path, filter_by_keys={'typeOfLevel': 'atmosphere', 'stepType': 'avg'})
ds = adjust_longitude(ds).sel(
        latitude=slice(lat_min, lat_max), 
        longitude=slice(lon_max, lon_min)
    )


forecast_time_hr = ds['step'].values.astype('timedelta64[h]') / np.timedelta64(1, 'h')
initialized_time = ds['time'].values
plt.title(f'F{forecast_time_hr} -- Initialized {initialized_time} UTC') 



ax.add_feature(cf.COASTLINE.with_scale("50m"), lw=0.5)
ax.add_feature(cf.BORDERS.with_scale("50m"), lw=0.3)
ax.add_feature(cf.STATES.with_scale("50m"), lw=0.3)
if add_counties:
    counties = cf.NaturalEarthFeature('cultural', 'admin_2_counties', '10m',
                                  edgecolor='grey', facecolor='none')
    ax.add_feature(counties)


# crs is PlateCarree -> we are explicitly telling axes, that we are creating bounds that are in degrees
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=crs)

# Add Eclipse ppath 
reader = shpreader.FionaReader('2024eclipse_shapefiles/upath_lo.shp')
ax.add_feature(ShapelyFeature(reader.geometries(), crs=crs, facecolor='none', edgecolor='black'))
reader = shpreader.FionaReader('2024eclipse_shapefiles/center.shp')
ax.add_feature(ShapelyFeature(reader.geometries(), crs=crs, facecolor='none', edgecolor='black'))


# Model Data 
cbar_kwargs = {'orientation':'horizontal', 'label':'Total Cloud Cover %', 'ticks':[10,20,30,40,50,60,70,80,90,100]}
colors = matplotlib.colors.ListedColormap(colors=['#FFFFFF', '#F3F3F1', '#E7E6E4', '#DBDAD6', '#CBCAC6', 
                                                  '#B7B6B5', '#A2A1A3', '#7E7D82', '#747780', '#555D6A',
                                                  '#3F4B5D', '#2B425D', '#1D4670', '#0E4983', '#004D96',
                                                  '#1062A9', '#2177BB', '#318CCE', '#4CA2DC', '#72B8E7', '#98CEF2'
                                                 ])

levels = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105]
ds['tcc'].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cbar_kwargs=cbar_kwargs, levels=levels, cmap=colors)

plt.title(f'F{forecast_time_hr} -- Initialized {initialized_time} UTC') 

plt.savefig(f'f{forecast_hour}.jpg')
# plt.show()
