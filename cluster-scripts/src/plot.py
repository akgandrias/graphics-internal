from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl

from helpers import save_optimized_image


def generate_plot(y, x):
    plot = Basemap(
        resolution='l',
        projection='stere',
        lat_0=62,
        lon_0=353,
        llcrnrlat=60.4,
        llcrnrlon=-11.41,
        urcrnrlat=63,
        urcrnrlon=-2.12,
    )

    plot.readshapefile('shapefiles/Oyggjar', 'Oyggjar')

    return plot(x, y)

def plot_wind(y, x, windspeed, uquiver, vquiver, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    wind_lons, wind_lats = generate_plot(y, x)

    levels = [0, 3.3, 5.4, 7.9, 10.7, 13.8, 17.1, 20.7, 24.4, 28.4, 32.6]

    colorstring=[
        '#e1e1e1',
        '#afafc8',
        '#7d7dc8',
        '#4bc8c8',
        '#4bc84b',
        '#c8c84b',
        '#c89632',
        '#c86432',
        '#c83232',
        '#c83296',
        '#9664c8'
    ]

    contour0 = ax.contourf(wind_lons, wind_lats, windspeed, levels=levels,colors=colorstring)
    
    ax.quiver(
        wind_lons[::2, ::2],
        wind_lats[::2, ::2],
        uquiver[::2, ::2],
        vquiver[::2, ::2],
        color="black",
        scale_units='inches',
        scale=125,
        width=0.0006
    )

    ax.axis('off')

    #Printing Colorbar
    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.45, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Vindur (m/s)',size=10)
    
    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)

def plot_cloud(y, x, c1, c2, c3, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    cloud_lons, cloud_lats = generate_plot(y, x)

    levels = [-0.01, 10, 25, 50, 75, 101]
    colorstring3=['#daf0ff', '#d2d2d2', '#b4b4b4', '#8c8c8c', '#646464']

    #For printing the colorbar
    ax.contourf(cloud_lons, cloud_lats, c2*100, levels=levels, colors=colorstring3, alpha=0.2)
    contour0 = ax.contourf(cloud_lons, cloud_lats, c1*100, levels=levels, colors=colorstring3)
    
    ax.axis('off')

    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.45, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.set_xticklabels(['0', '10', '25', '50', '75', '100'])
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Skýloft (%)',size=10)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)

def plot_precip(y, x, precip, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    precip_lons, precip_lats = generate_plot(y, x)

    levels = [-0.01, 0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15]
    colorstring=['#daf0ff', '#cdcdf7', '#9696c8', '#6060a6', '#6464dc', '#a160a6', '#f04507', '#ff0303']
    contour0 = ax.contourf(precip_lons, precip_lats, precip, levels=levels, colors=colorstring)

    ax.axis('off')

    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.45, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.set_xticklabels([0, 0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15])
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Avfall (mm/t)',size=10)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)

def plot_snow(y, x, snow, file_names: list[str]):
    plt.rcParams['hatch.color'] = 'white'
    plt.rcParams['hatch.linewidth'] = 0.2
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    snow_lons, snow_lats = generate_plot(y, x)

    levels = [-0.01, 0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15]
    colorstring=['#daf0ff', '#cdcdf7', '#9696c8', '#6060a6', '#6464dc', '#a160a6', '#f04507', '#ff0303']
    theHatches = [None, 'oo', 'oo', 'oo', 'oo', 'oo', 'oo', 'oo', 'oo',]
    contour0 = ax.contourf(snow_lons, snow_lats, snow, levels=levels, colors=colorstring, hatches=theHatches)
    

    ax.axis('off')

    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.45, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.set_xticklabels([0, 0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15])
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Kavi (mm/t)',size=10)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)

def plot_temp(y, x, t2, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    temp_lons, temp_lats = generate_plot(y, x)

    levels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    colorstring=[
        '#4b4b96',
        '#646496',
        '#7d7daf',
        '#afafc8',
        '#c8c8e4',
        '#ffffff',
        '#e4e4c8',
        '#e4e496',
        '#e4e464',
        '#e4c832',
        '#e49632',
        '#c87d32',
        '#c8644b',
        '#c85a5a',
        '#c83232',
        '#961919'
    ]

    contour0 = ax.contourf(temp_lons, temp_lats, t2, levels=levels, colors=colorstring)
            
    ax.axis('off')

    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.45, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Hitalag (°C)',size=10)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)
