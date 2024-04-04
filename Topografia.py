# Importando bibliotecas
from ncBuilder import ncBuilder, ncHelper
import pandas as pd
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import numpy as np
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import pygmt


# Definindo dimensões
minlon, maxlon = -47.5, -41
minlat, maxlat = -24.2, -18.5
i = 5.5
inset_region = [minlon-i, maxlon+1, minlat-1, maxlat+i]
inset_projection = "M3.5c"
region=[minlon, maxlon, minlat, maxlat]


# Dados de elevação
grid = pygmt.datasets.load_earth_relief(resolution="03s", region=[minlon, maxlon, minlat, maxlat]) #03s
frame =  ["xa1f0.25","ya1f0.25", "z2000+lMetros", "wSEnZ"]
pygmt.makecpt(
        cmap='geo',
        series=f'-6000/4000/100',
        continuous=True
    )


fig = pygmt.Figure()
fig.grdview(
    grid=grid,
    region=[minlon, maxlon, minlat, maxlat, -6000, 4000],
    perspective=[150, 30],
    frame=frame,
    projection="M15c",
    zsize="4c",
    surftype="i",
    plane="-6000+gazure",
    shading=0,
    # Set the contour pen thickness to "1p"
    contourpen="1p",
)

with fig.inset(position="jBR+w3.5c+o13.5c/9.2c", margin=0, box="+pblack"):
    fig.coast(
        region=inset_region,
        shorelines="thin",
        projection=inset_projection,
        land="lightyellow",
        water="lightblue",
        frame="a",
        borders=["1/0.5p,black", "2/1p,red", "3/0.5p,blue"]
    )
    rectangle = [[region[0], region[2], region[1], region[3]]]
    fig.plot(data=rectangle, style="r+s", pen="1p,blue")

# Gerando colorbar
fig.colorbar(perspective=True, frame=["a2000", "x+lElevação (m)", "y+lm"])
fig.savefig("topo-plot_3d.png", crop=True, dpi=300)

fig.show()


fig.savefig("topo-defesa.png", crop=True, dpi=300)
