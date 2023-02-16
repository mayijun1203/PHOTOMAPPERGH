import pandas as pd
import geopandas as gpd
import shapely
import exif
import os
import PIL

# path=os.gecwd()
# path='C:/Users/MaY8/Desktop/GITHUB/PHOTOMAPPERGH/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/PHOTOMAPPERGH/'
pd.options.display.max_columns=100



# EXIF list
# imgpath=path+'photo/IMG_0332.JPG'
# with open(imgpath,'rb') as src:
#     img=exif.Image(src)
# img.get_all()



# Extract info
def decimalcoords(orgcoords,ref):
    decimaldegrees=orgcoords[0]+orgcoords[1]/60+orgcoords[2]/3600
    if ref=='S' or ref=='W':
        decimaldegrees=-decimaldegrees
    return decimaldegrees

def imgcoords(imgpath):
    with open(path+'original/'+imgpath,'rb') as src:
        img=exif.Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords=(decimalcoords(img.gps_latitude,
                                  img.gps_latitude_ref),
                    decimalcoords(img.gps_longitude,
                                  img.gps_longitude_ref))
        except AttributeError:
            print(imgpath+' No Coordinates!')
    else:
        print(imgpath+' No EXIF!')
    tp=pd.DataFrame({'photo':[imgpath],
                     'datetime':[img.datetime_original],
                     'lat':[coords[0]],
                     'long':[coords[1]],
                     'bearing':[img.gps_dest_bearing]})
    return(tp)

df=[]
for i in os.listdir(path+'original'):
    df+=[imgcoords(i)]
df=pd.concat(df,axis=0)
df=gpd.GeoDataFrame(df,geometry=[shapely.geometry.Point(xy) for xy in zip(df['long'],df['lat'])],crs=4326)
df.to_file(path+'photoattr.geojson',crs=4326, driver='GeoJSON')



# Compress photos
for i in os.listdir(path+'original'):
    tp=PIL.Image.open(path+'original/'+i)
    tp.save(path+'photo/'+i,optimize=True,quality=30)


