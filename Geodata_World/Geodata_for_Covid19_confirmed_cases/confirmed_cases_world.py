import pandas as pd
import geopandas as gpd
from PIL import Image, ImageDraw
import io
import pylab
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

data = pd.read_csv(url)


# Grouping the data by country
data = data.groupby('Country/Region').sum()

# Removing Latitudes and Longitudes
data = data.drop(columns = ['Lat','Long'])

#Transpose of data frame
data_transposed = data.T

# Read shapefile
world = gpd.read_file('World_Map.shp')

# Remove discrepancies
world.replace('Viet Nam','Vietnam', inplace = True)
world.replace('Brunei Darussalam','Brunei', inplace = True)
world.replace('Cape Verde','Cabo Verde', inplace = True)
world.replace('Palestine','West Bank and Gaza', inplace = True)
world.replace('United States','US', inplace = True)
world.replace('Taiwan','Taiwan*', inplace = True)
world.replace('Syrian Arab Republic','Syria', inplace = True)
world.replace('Democratic Republic of the Congo','Congo (Kinshasa)', inplace = True)
world.replace('Congo','Congo (Brazzaville)', inplace = True)
world.replace('Czech Republic','Czechia', inplace = True)
world.replace('Swaziland','Eswatini', inplace = True)
world.replace('Iran (Islamic Republic of)','Iran', inplace = True)
world.replace('Korea, Republic of','Korea, South', inplace = True)
world.replace("Lao People's Democratic Republic",'Laos', inplace = True)
world.replace('Libyan Arab Jamahiriya','Libya', inplace = True)
world.replace('Republic of Moldova','Moldova', inplace = True)
world.replace('The former Yugoslav Republic of Macedonia','North Macedonia', inplace = True)
world.replace('United Republic of Tanzania','Tanzania', inplace = True)



# Merge data with world
merge = world.join(data, on = 'NAME', how= 'right')

img_frames = []
lenth = len(merge.columns.to_list())
for dates in merge.columns.to_list()[2:lenth]:

    ax = merge.plot(column = dates,
                    cmap = 'pink', #OrRd
                    figsize = (14,14),
                    legend = True,
                    scheme ='user_defined',
                    classification_kwds = {'bins':[10,20,50,500,1000,5000,10000,500000]},
                    edgecolor = 'black',
                    linewidth = 0.4)

    ax.set_title("Total confirmed Covid19 Cases Worldover : " + dates,
             fontdict = {'fontsize': 20}, pad = 12, color = 'white') 
    ax.set_axis_off()


    ax.get_legend().set_bbox_to_anchor((0.16,0.6))
   
    fig = plt.gcf()
    fig.patch.set_facecolor('black')
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png', bbox_inches = 'tight')
    buf.seek(0)
    im = Image.open(buf)
   
    img_frames.append(im)
    pylab.close()


#Create gif
img_frames[0].save('covid19_world_confirmed_theme1.gif', format = 'GIF',
                  save_all = True, append_images = img_frames[1:], duration = 300,loop = 1)

buf.close()
