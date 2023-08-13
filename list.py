import numpy as np
import os
import pygrib as pgr
import re
import datetime
from datetime import timedelta
from datetime import date
import os
import ftplib
import bz2
from pathlib import Path
import typing


# from helpers import validate_time

# ----------------- Getting model data from the FTP --------------------------


# Define the path of the harmonie data to be processed
treepath = "/home/nea-data/Documents/data/latest/"
# storagepath = "/home/nea-data/Documents/data/past/"
# cloudpath = "/run/user/1000/gvfs/google-drive:host=vedur.fo,user=akg/nea-data/"
storagepath = "/home/nea-data/Documents/data/past/"



# Log on to the DMI FTP and get model data
HOSTNAME = "ftpserver.dmi.dk"
USERNAME = "0700dmi"
PASSWORD = "Fo0809"
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)


# Set to the Harmonie 06:00 model run for the day.
# now = datetime.datetime.now()
model_run_time = datetime.datetime.utcnow()
# model_run_time = datetime.datetime(date.today().year,date.today().month,date.today().day,6,0)
# model_run_time = datetime.datetime(utcnow.today().year,date.today().month,date.today().day,6,0)


# for x in range(55):
#     model_timestep_date = model_run_time + timedelta(hours=x)


#     name = 'NEA_'+str(model_run_time.year).zfill(2)+str(model_run_time.month).zfill(2)+str(model_run_time.day).zfill(2)+str(model_run_time.hour).zfill(2)+'.0'+str(x).zfill(2)+'.bz2'
#     print(name)


ftp_names: typing.List[str] = []
for item in ftp_server.nlst():
#     if validate_time(item) and '.md5' not in item:
    if 'NEA_' in item and '.bz2' in item and '.md5' not in item:
#         print(item.rsplit('.',1[0]))
        base, ext = os.path.splitext(item)
        
        ftp_names.append(base)

server_names: typing.List[str] = []
for top, dirs, files in os.walk(treepath):
    for file in files:
        server_names.append(os.path.join(file))

        
# print(list(set(treepath)))
# print(treepath.nlst())
# print(os.listdir(treepath))
the_names = list(set(ftp_names) - set(server_names))
the_names.sort()
for name in the_names:
    print(name)
# print(the_names)


#Taking backup of the old files not existing on the DMI ftp server anymore.

#Defining name extension for the 3d data
nameextension = '-3d-variables'

the_old_names = list(set(server_names) - set(ftp_names))
unusabe_names = [s for s in the_old_names if s.endswith(nameextension)]
backup_names = list(set(the_old_names) - set(unusabe_names))

backup_names.sort()



for file in backup_names:
    print(file)
    year=os.path.join(file[4:8])
    month=os.path.join(file[8:10])
    day=os.path.join(file[10:12])
    hour=os.path.join(file[12:14])
#         print(year)
#         print(month)
#         print(day)
#         print(hour)
    
    if not os.path.exists(storagepath+year):
        os.makedirs(storagepath+year)
        
    if not os.path.exists(storagepath+year+'/'+month):
        os.makedirs(storagepath+year+'/'+month)
    
    if not os.path.exists(storagepath+year+'/'+month+'/'+day):
        os.makedirs(storagepath+year+'/'+month+'/'+day)
    
    if not os.path.exists(storagepath+year+'/'+month+'/'+day+'/'+hour):
        os.makedirs(storagepath+year+'/'+month+'/'+day+'/'+hour)
    
    os.rename(treepath+file,storagepath+year+'/'+month+'/'+day+'/'+hour+'/'+file)
    os.rename(treepath+file+nameextension,storagepath+year+'/'+month+'/'+day+'/'+hour+'/'+file+nameextension)
#             print(os.path.exists(treepath+year))


download_names: typing.List[str] = []
for name in the_names:
    download_names.append(name+'.bz2')
#     name2 = name
#     name = name2+'.bz2'

# print(download_names)


########--------------------THIS IS THE EXTRA CODE-------------------#############

#Remember to remove this file after each usage
filelist = '/home/nea-data/Documents/data/filelist.txt'
# d02name = '/root/Automatization/d02name.txt'
file = open(filelist,'w')
for item in download_names:
        file.write(item+"\n")
file.close()


########---------------------------------------#############










# for name in download_names:
#     #ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    
#     with open(name, "wb") as file:
#         ftp_server.retrbinary(f"RETR {name}", file.write)
        
#     filepath = treepath+name
    
#     # Move the downloaded folder to file destination
#     os.rename(name, filepath)

#     # Decompress the .bz2 extension
#     zipfile = bz2.BZ2File(filepath) # open the file
#     data = zipfile.read() # get the decompressed data
#     newfilepath = filepath[:-4]+'.temp' # assuming the filepath ends with .bz2
#     open(newfilepath, 'wb').write(data) # write a uncompressed file
    
#     # Get rid of the old file
#     os.remove(filepath)
    
    
    
    
    
#     grbs = pgr.open(newfilepath)
    
    
#     base2, ext2 = os.path.splitext(newfilepath)
    
#     #     grbout = open(Destinationname[x1],'wb')

#     # Storing surface variables
#     grbout = open(base2,'wb')


#     grbout.write(grbs.message(1).tostring())   #mslp
#     grbout.write(grbs.message(178).tostring()) #Surface Pressure

#     grbout.write(grbs.message(191).tostring()) #u10
#     grbout.write(grbs.message(197).tostring()) #v10
#     grbout.write(grbs.message(215).tostring()) #low cloud
#     grbout.write(grbs.message(216).tostring()) #Medium cloud
#     grbout.write(grbs.message(217).tostring()) #High cloud
#     grbout.write(grbs.message(214).tostring()) #Fog
#     grbout.write(grbs.message(181).tostring()) #2m temp

#     grbout.write(grbs.message(17).tostring()) #Accumulated Rain
#     grbout.write(grbs.message(210).tostring()) #Total Precipitation
#     grbout.write(grbs.message(224).tostring()) #Accumulated Snow
#     grbout.write(grbs.message(225).tostring()) #Total Solid Precipitation
#     grbout.write(grbs.message(10).tostring()) #Accumulated Graupel

#     grbout.write(grbs.message(190).tostring()) #Visibility
#     grbout.write(grbs.message(3).tostring())  #CAPE
#     grbout.write(grbs.message(4).tostring())  #CIN

#     grbout.write(grbs.message(222).tostring()) #Gust U-component 
#     grbout.write(grbs.message(223).tostring()) #Gust V-component
#     grbout.write(grbs.message(129).tostring()) #850 hPa Temperature
#     grbout.write(grbs.message(209).tostring()) #Relative Humidity
#     grbout.write(grbs.message(226).tostring()) #Cloud Base
#     grbout.write(grbs.message(227).tostring()) #Cloud Top
#     grbout.write(grbs.message(187).tostring()) #Max Temperature
#     grbout.write(grbs.message(188).tostring()) #MinTemperature
#     grbout.write(grbs.message(189).tostring()) #Dew Point Temperature


#     grbout.write(grbs.message(218).tostring()) #Land-sea Mask (LSM)
#     grbout.write(grbs.message(180).tostring()) #SST
#     grbout.write(grbs.message(211).tostring()) #Snow-depth water equivalent


#     grbout.close

#     # Storing 3d-variables
#     datavariables3d = base2+nameextension
#     grbout = open(datavariables3d,'wb')


#     #50 hPa
#     grbout.write(grbs.message(18).tostring()) #Geopotential
#     grbout.write(grbs.message(19).tostring()) #Temperature
#     grbout.write(grbs.message(21).tostring()) #U
#     grbout.write(grbs.message(22).tostring()) #V
#     grbout.write(grbs.message(25).tostring()) #Relative Humidity

#     #100 hPa
#     grbout.write(grbs.message(28).tostring()) #Geopotential
#     grbout.write(grbs.message(29).tostring()) #Temperature
#     grbout.write(grbs.message(31).tostring()) #U
#     grbout.write(grbs.message(32).tostring()) #V
#     grbout.write(grbs.message(35).tostring()) #Relative Humidity


#     #150 hPa
#     grbout.write(grbs.message(38).tostring()) #Geopotential
#     grbout.write(grbs.message(39).tostring()) #Temperature
#     grbout.write(grbs.message(41).tostring()) #U
#     grbout.write(grbs.message(42).tostring()) #V
#     grbout.write(grbs.message(45).tostring()) #Relative Humidity


#     #200 hPa
#     grbout.write(grbs.message(48).tostring()) #Geopotential
#     grbout.write(grbs.message(49).tostring()) #Temperature
#     grbout.write(grbs.message(51).tostring()) #U
#     grbout.write(grbs.message(52).tostring()) #V
#     grbout.write(grbs.message(55).tostring()) #Relative Humidity

#     #250 hPa
#     grbout.write(grbs.message(58).tostring()) #Geopotential
#     grbout.write(grbs.message(59).tostring()) #Temperature
#     grbout.write(grbs.message(61).tostring()) #U
#     grbout.write(grbs.message(62).tostring()) #V
#     grbout.write(grbs.message(65).tostring()) #Relative Humidity

#     #300 hPa
#     grbout.write(grbs.message(68).tostring()) #Geopotential
#     grbout.write(grbs.message(69).tostring()) #Temperature
#     grbout.write(grbs.message(71).tostring()) #U
#     grbout.write(grbs.message(72).tostring()) #V
#     grbout.write(grbs.message(75).tostring()) #Relative Humidity

#     #400 hPa
#     grbout.write(grbs.message(78).tostring()) #Geopotential
#     grbout.write(grbs.message(79).tostring()) #Temperature
#     grbout.write(grbs.message(81).tostring()) #U
#     grbout.write(grbs.message(82).tostring()) #V
#     grbout.write(grbs.message(85).tostring()) #Relative Humidity

#     #500 hPa
#     grbout.write(grbs.message(88).tostring()) #Geopotential
#     grbout.write(grbs.message(89).tostring()) #Temperature
#     grbout.write(grbs.message(91).tostring()) #U
#     grbout.write(grbs.message(92).tostring()) #V
#     grbout.write(grbs.message(95).tostring()) #Relative Humidity

#     #600 hPa
#     grbout.write(grbs.message(98).tostring()) #Geopotential
#     grbout.write(grbs.message(99).tostring()) #Temperature
#     grbout.write(grbs.message(101).tostring()) #U
#     grbout.write(grbs.message(102).tostring()) #V
#     grbout.write(grbs.message(105).tostring()) #Relative Humidity

#     #700 hPa
#     grbout.write(grbs.message(108).tostring()) #Geopotential
#     grbout.write(grbs.message(109).tostring()) #Temperature
#     grbout.write(grbs.message(111).tostring()) #U
#     grbout.write(grbs.message(112).tostring()) #V
#     grbout.write(grbs.message(115).tostring()) #Relative Humidity

#     #800 hPa
#     grbout.write(grbs.message(118).tostring()) #Geopotential
#     grbout.write(grbs.message(119).tostring()) #Temperature
#     grbout.write(grbs.message(121).tostring()) #U
#     grbout.write(grbs.message(122).tostring()) #V
#     grbout.write(grbs.message(125).tostring()) #Relative Humidity

#     #850 hPa
#     grbout.write(grbs.message(128).tostring()) #Geopotential
#     grbout.write(grbs.message(129).tostring()) #Temperature
#     grbout.write(grbs.message(131).tostring()) #U
#     grbout.write(grbs.message(132).tostring()) #V
#     grbout.write(grbs.message(135).tostring()) #Relative Humidity

#     #900 hPa
#     grbout.write(grbs.message(138).tostring()) #Geopotential
#     grbout.write(grbs.message(139).tostring()) #Temperature
#     grbout.write(grbs.message(141).tostring()) #U
#     grbout.write(grbs.message(142).tostring()) #V
#     grbout.write(grbs.message(145).tostring()) #Relative Humidity

#     #925 hPa
#     grbout.write(grbs.message(148).tostring()) #Geopotential
#     grbout.write(grbs.message(149).tostring()) #Temperature
#     grbout.write(grbs.message(151).tostring()) #U
#     grbout.write(grbs.message(152).tostring()) #V
#     grbout.write(grbs.message(155).tostring()) #Relative Humidity

#     #950 hPa
#     grbout.write(grbs.message(158).tostring()) #Geopotential
#     grbout.write(grbs.message(159).tostring()) #Temperature
#     grbout.write(grbs.message(161).tostring()) #U
#     grbout.write(grbs.message(162).tostring()) #V

#     grbout.write(grbs.message(165).tostring()) #Relative Humidity

#     #1000 hPa
#     grbout.write(grbs.message(168).tostring()) #Geopotential
#     grbout.write(grbs.message(169).tostring()) #Temperature
#     grbout.write(grbs.message(171).tostring()) #U
#     grbout.write(grbs.message(172).tostring()) #V
#     grbout.write(grbs.message(175).tostring()) #Relative Humidity

#     grbout.close

#     os.remove(newfilepath)
    
    




# # for top, dirs, files in os.walk(treepath):
# #     for file in files:
# #         if file in backup_names:
# #             print(file)



