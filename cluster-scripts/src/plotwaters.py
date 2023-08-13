import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


from helpers import save_optimized_image




def generate_waters_plot(y, x):
    plot = Basemap(
        resolution='l',
        projection='stere',
        lat_0=62,
        lon_0=353,
        llcrnrlat=58.4,
        llcrnrlon=-16.41,
        urcrnrlat=65,
        urcrnrlon=3,
    )
    
    plot.drawcoastlines()
    plot.readshapefile('shapefiles/Oyggjar', 'Oyggjar')
    plot.readshapefile('shapefiles/Ytribanki', 'Ytribanki',color='blue')
    plot.readshapefile('shapefiles/Munkagrunnur', 'Munkagrunnur',color='blue')
    plot.readshapefile('shapefiles/Fugloyarbanki', 'Fugloyarbanki',color='blue')
    plot.readshapefile('shapefiles/Islandsryggur', 'Islandsryggur',color='blue')
    plot.readshapefile('shapefiles/Fiskimark1','Fiskimark1',color='red')
    plot.readshapefile('shapefiles/Fiskimark2','Fiskimark2',color='red')
    return plot(x, y)



def plot_wind_waters(y, x, windspeed, uquiver, vquiver, mslp, file_names: list[str]):

    fig, ax = plt.subplots(
    figsize=(21, 9),
    dpi=410.1,
    frameon=False
    )
    wind_lons, wind_lats = generate_waters_plot(y, x)

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
    
    k = 8
    ax.quiver(
        wind_lons[::k, ::k],
        wind_lats[::k, ::k],
        uquiver[::k, ::k],
        vquiver[::k, ::k],
        color="black",
        scale_units='inches',
        scale=85,
        width=0.0010,
        pivot='mid'
    )
    
    #Attempted to display windspeed numbers. It became a very ugly solution, but it works somewhat for now..
    ilen = np.floor_divide(386,k)
    jlen = np.floor_divide(386,k)

    for i in range(1,ilen-23):
        
        for j in range(40,jlen):
            plt.text(wind_lons[i*k+4, j*k], wind_lats[i*k+4, j*k], round(windspeed[i*k, j*k]),fontsize=5, ha='center', va='center', color='black')

    for i in range(1,ilen-20):
        
        for j in range(35,jlen-(jlen-40)):
            plt.text(wind_lons[i*k+4, j*k], wind_lats[i*k+4, j*k], round(windspeed[i*k, j*k]),fontsize=5, ha='center', va='center', color='black')
            
    for i in range(1,ilen-18):
        
        for j in range(25,jlen-(jlen-35)):
            plt.text(wind_lons[i*k+4, j*k], wind_lats[i*k+4, j*k], round(windspeed[i*k, j*k]),fontsize=5, ha='center', va='center', color='black')

    for i in range(1,ilen-15):
        
        for j in range(15,jlen-(jlen-25)):
            plt.text(wind_lons[i*k+4, j*k], wind_lats[i*k+4, j*k], round(windspeed[i*k, j*k]),fontsize=5, ha='center', va='center', color='black')
            
    for i in range(5,ilen-15):
        
        for j in range(7,jlen-(jlen-15)):
            plt.text(wind_lons[i*k+4, j*k], wind_lats[i*k+4, j*k], round(windspeed[i*k, j*k]),fontsize=5, ha='center', va='center', color='black')            

    #Contouring pressure levels        
    levels = range(800,1100,4)
    contour3 = ax.contour(wind_lons,wind_lats,mslp,levels=levels,colors='black')
    
    ax.axis('off')

    #Printing Colorbar
    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.2, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Vindur (m/s)',size=10)
    
    #Assigning contour label for pressure
    contourlabel1 = ax.clabel(contour3, contour3.levels, inline=1, fontsize=12,inline_spacing=100)
    
    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)


def plot_wind_waters2(y, x, windspeed, uquiver, vquiver, mslp, file_names: list[str]):

    fig, ax = plt.subplots(
    figsize=(21, 9),
    dpi=410.1,
    frameon=False
    )
    wind_lons, wind_lats = generate_waters_plot(y, x)

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
    
    k = 8
    ax.quiver(
        wind_lons[::k, ::k],
        wind_lats[::k, ::k],
        uquiver[::k, ::k],
        vquiver[::k, ::k],
        color="black",
        scale_units='inches',
        scale=85,
        width=0.0010,
        pivot='mid'
    )
    

    #Contouring pressure levels        
    levels = range(800,1100,4)
    contour3 = ax.contour(wind_lons,wind_lats,mslp,levels=levels,colors='black')
    
    ax.axis('off')

    #Printing Colorbar
    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.2, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Vindur (m/s)',size=10)
    
    #Assigning contour label for pressure
    contourlabel1 = ax.clabel(contour3, contour3.levels, inline=1, fontsize=12,inline_spacing=100)
    
    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)



def plot_overview_waters(y, x, precip, snow, c1, mslp, temp850, file_names: list[str]):
    
    fig, ax = plt.subplots(
    figsize=(21, 9),
    dpi=410.1,
    frameon=False
    )
    overvie_lons, overview_lats = generate_waters_plot(y, x)

    #Plotting clouds
    
    levels = [-0.01, 35, 55, 70, 95, 101]
    
    #Plotting Low Clouds
    colorstring3=['#daf0ff','#d2d2d2', '#b4b4b4', '#8c8c8c', '#646464']
    contour0 = ax.contourf(overvie_lons, overview_lats, c1*100, levels=levels, colors=colorstring3)
    
    #Plotting Rain
    levels = [0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15]
    colorstring=['#8589ff', '#8589ff', '#7275db', '#6568c7', '#4c4fad', '#dbbf6b', '#f5e767']
    contour1 = ax.contourf(overvie_lons, overview_lats, precip, levels=levels, colors=colorstring)

    
    #Plotting Snow
    levels = [0.17, 0.33, 0.83, 1.67, 2.5, 10]
    colorstring=['#e6d0f2', '#c091d9', '#9a63b8', '#7c419c', '#750c42']
    contour2 = ax.contourf(overvie_lons, overview_lats, snow, levels=levels, colors=colorstring)

    levels = range(800,1100,4)
    contour3 = ax.contour(overvie_lons,overview_lats,mslp,levels=levels,colors='black')
    
    
    #Plotting Airmass Temperature (850 hPa) in different color intervals
    levels = range(-40,-6,2)
    contour4 = ax.contour(overvie_lons,overview_lats,temp850,levels=levels,colors='#3232e1',linestyles='solid')
    
    levels = [-4, -2, 0]
    contour5 =ax.contour(overvie_lons,overview_lats,temp850,levels=levels,colors='#960096',linestyles='solid')
    
    levels = range(2,40,2)
    contour6 =ax.contour(overvie_lons,overview_lats,temp850,levels=levels,colors='#e13232',linestyles='solid')
    
    
    ax.axis('off')
    
    
    #Printing Colorbars
    cbar2 = plt.colorbar(contour2, ax=ax, extend="neither",location="right", pad=-0.07, fraction=0.021, shrink=0.3, orientation='vertical')
    cbar2.ax.set_yticklabels([0.17, 0.33, 0.83, 1.67, 2.5, 10])
    cbar2.ax.tick_params(labelsize=10)
    cbar2.set_label(label='Kavi (cm/t)',size=10)

    cbar1 = plt.colorbar(contour1, ax=ax, extend="neither",location="right", pad=-0.47, fraction=0.021, shrink=0.3, orientation='vertical')
    cbar1.ax.set_yticklabels([0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15])
    cbar1.ax.tick_params(labelsize=10)
    cbar1.set_label(label='Regn (mm/t)',size=10)
    
    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.2, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.set_xticklabels(['0', '10', '25', '50', '75', '100'])
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Skýloft (%)',size=10)
    
    #Placing text on contour labels
    contourlabel1 = ax.clabel(contour3, contour3.levels, inline=1, fontsize=12,inline_spacing=100)
    contourlabel2 = ax.clabel(contour4, contour4.levels, inline=1, fontsize=12,inline_spacing=75)
    contourlabel3 = ax.clabel(contour5, contour5.levels, inline=1, fontsize=12,inline_spacing=75)
    contourlabel4 = ax.clabel(contour6, contour6.levels, inline=1, fontsize=12,inline_spacing=75)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)


    

    
def plot_clouds_waters(y, x, c1, c2, c3, mslp, temp850, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    clouds_lons, clouds_lats = generate_waters_plot(y, x)

    
    #Plotting clouds
    
    #High clouds
    levels = [-0.01, 25, 35, 70, 90, 101]
    colorstring1=['#daf0ff', '#c7c7ff', '#aeaefc', '#9696fa', '#5454ff']
    ax.contourf(clouds_lons, clouds_lats, c3*100, levels=levels, colors=colorstring1,alpha=0.7)
    
    levels = [35, 55, 70, 95, 101]
    
    #Medium Clouds
    colorstring2=['#c7fa9b', '#b9fa50', '#82fa19', '#7efa19']    
    ax.contourf(clouds_lons, clouds_lats, c2*100, levels=levels, colors=colorstring2,alpha=0.8)
    
    #Low Clouds
    colorstring3=['#d2d2d2', '#b4b4b4', '#8c8c8c', '#646464']
    contour0 = ax.contourf(clouds_lons, clouds_lats, c1*100, levels=levels, colors=colorstring3)

    levels = range(800,1100,4)
    contour3 = ax.contour(clouds_lons,clouds_lats,mslp,levels=levels,colors='black')
    
    
    #Plotting airmass temperature in different color intervals
    levels = range(-40,-6,2)
    contour4 = ax.contour(clouds_lons,clouds_lats,temp850,levels=levels,colors='#3232e1',linestyles='solid')
    
    levels = [-4, -2, 0]
    contour5 =ax.contour(clouds_lons,clouds_lats,temp850,levels=levels,colors='#960096',linestyles='solid')
    
    levels = range(2,40,2)
    contour6 =ax.contour(clouds_lons,clouds_lats,temp850,levels=levels,colors='#e13232',linestyles='solid')
    
    
    ax.axis('off')
    
    #Drawing the colormap of low clouds
    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.2, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.set_xticklabels(['10', '25', '50', '75', '100'])
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Skýloft (%)',size=10)
    
    #Placing text on contour labels
    contourlabel1 = ax.clabel(contour3, contour3.levels, inline=True, fontsize=12,inline_spacing=100)
    contourlabel2 = ax.clabel(contour4, contour4.levels, inline=True, fontsize=12,inline_spacing=75)
    contourlabel3 = ax.clabel(contour5, contour5.levels, inline=True, fontsize=12,inline_spacing=75)
    contourlabel4 = ax.clabel(contour6, contour6.levels, inline=True, fontsize=12,inline_spacing=75)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)




def plot_precipitation_waters(y, x, precip, snow, mslp,temp850, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    precip_lons, precip_lats = generate_waters_plot(y, x)

    
    #Plotting rain
    levels = [-0.01, 0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15]
    colorstring=['#daf0ff','#8589ff', '#8589ff', '#7275db', '#6568c7', '#4c4fad', '#dbbf6b', '#f5e767']
    contour1 = ax.contourf(precip_lons, precip_lats, precip, levels=levels, colors=colorstring)

    
    #Plotting snow
    levels = [0.17, 0.33, 0.83, 1.67, 2.5, 10]
    colorstring=['#e6d0f2', '#c091d9', '#9a63b8', '#7c419c', '#750c42']
    contour2 = ax.contourf(precip_lons, precip_lats, snow, levels=levels, colors=colorstring)

    levels = range(800,1100,4)
    contour3 = ax.contour(precip_lons,precip_lats,mslp,levels=levels,colors='black')
    
    
    #Plotting airmass temperature in different color intervals
    levels = range(-40,-6,2)
    contour4 = ax.contour(precip_lons,precip_lats,temp850,levels=levels,colors='#3232e1',linestyles='solid')
    
    levels = [-4, -2, 0]
    contour5 =ax.contour(precip_lons,precip_lats,temp850,levels=levels,colors='#960096',linestyles='solid')
    
    levels = range(2,40,2)
    contour6 =ax.contour(precip_lons,precip_lats,temp850,levels=levels,colors='#e13232',linestyles='solid')
    
    
    ax.axis('off')
    
    
    
    cbar2 = plt.colorbar(contour2, ax=ax, extend="neither",location="right", pad=-0.07, fraction=0.021, shrink=0.3, orientation='vertical')
    cbar2.ax.set_yticklabels([0.17, 0.33, 0.83, 1.67, 2.5, 10])
    cbar2.ax.tick_params(labelsize=10)
    cbar2.set_label(label='Kavi (cm/t)',size=10)

    cbar1 = plt.colorbar(contour1, ax=ax, extend="neither",location="right", pad=-0.05, fraction=0.021, shrink=0.3, orientation='vertical')
    cbar1.ax.set_yticklabels([0, 0.08, 0.17, 0.33, 0.83, 1.67, 4, 8, 15])
    cbar1.ax.tick_params(labelsize=10)
    cbar1.set_label(label='Regn (mm/t)',size=10)
    
    #Placing text on contour labels
    contourlabel1 = ax.clabel(contour3, contour3.levels, inline=True, fontsize=12,inline_spacing=100)
    contourlabel2 = ax.clabel(contour4, contour4.levels, inline=True, fontsize=12,inline_spacing=75)
    contourlabel3 = ax.clabel(contour5, contour5.levels, inline=True, fontsize=12,inline_spacing=75)
    contourlabel4 = ax.clabel(contour6, contour6.levels, inline=True, fontsize=12,inline_spacing=75)

    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)



def plot_visibility_waters(y, x, visibility, mslp, file_names: list[str]):
    fig, ax = plt.subplots(
        figsize=(21, 9),
        dpi=410.1,
        frameon=False
    )
    vis_lons, vis_lats = generate_waters_plot(y, x)

    
    #Plotting visibility
    levels = [-0.01, 1000, 4000, 8000, 999999999999]
    colorstring1=['#464646','#964b96', '#e8e248','#daf0ff']
    contour0 = ax.contourf(vis_lons, vis_lats, visibility, levels=levels, colors=colorstring1)
    
    #Plotting pressure
    levels = range(800,1100,4)
    contour1 = ax.contour(vis_lons,vis_lats,mslp,levels=levels,colors='black')
        
    ax.axis('off')
    
    #Drawing the colormap of visibility
    cbar = plt.colorbar(contour0, ax=ax, extend="neither",location="bottom", pad=-0.22, fraction=0.021, shrink=0.3, orientation='horizontal')
    cbar.ax.set_xticklabels(['0km','1km', '4km', '8km', 'Gott sýni'])
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label(label='Sýni',size=10)
    
    #Placing text on contour labels
    contourlabel1 = ax.clabel(contour1, contour1.levels, inline=True, fontsize=12,inline_spacing=100)


    fig.savefig(file_names[0], bbox_inches='tight', pad_inches = 0)
    save_optimized_image(file_names)


