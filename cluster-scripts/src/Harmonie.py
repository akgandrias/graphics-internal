import os
import io
import bz2
import shutil
import typing
import ftplib
import multiprocessing

import minio
import urllib3
import numpy as np
import pygrib as pgr

from plot import plot_cloud, plot_precip, plot_temp, plot_wind, plot_snow
from plotwaters import plot_wind_waters, plot_wind_waters2, plot_overview_waters, plot_clouds_waters, plot_precipitation_waters, plot_visibility_waters
from helpers import validate_time


def get_save_file_names(file_name: str):
    return {
        "wind": [
            f"{file_name}_wind.png",
            f"{file_name}_wind_opt.jpg",
            f"{file_name}_wind_opt.webp",
        ],
        "cloud": [
            f"{file_name}_cloud.png",
            f"{file_name}_cloud_opt.jpg",
            f"{file_name}_cloud_opt.webp",
        ],
        "temp": [
            f"{file_name}_temp.png",
            f"{file_name}_temp_opt.jpg",
            f"{file_name}_temp_opt.webp",
        ],
        "precip": [
            f"{file_name}_precip.png",
            f"{file_name}_precip_opt.jpg",
            f"{file_name}_precip_opt.webp",
        ],
        "snow": [
            f"{file_name}_snow.png",
            f"{file_name}_snow_opt.jpg",
            f"{file_name}_snow_opt.webp",
        ],
        "wind-waters": [
            f"{file_name}_wind-waters.png",
            f"{file_name}_wind-waters_opt.jpg",
            f"{file_name}_wind-waters_opt.webp",
        ],
        "wind-waters2": [
            f"{file_name}_wind-waters2.png",
            f"{file_name}_wind-waters2_opt.jpg",
            f"{file_name}_wind-waters2_opt.webp",
        ],
        "overview-waters": [
            f"{file_name}_overview-waters.png",
            f"{file_name}_overview-waters_opt.jpg",
            f"{file_name}_overview-waters_opt.webp",
        ],
        "clouds-waters": [
            f"{file_name}_clouds-waters.png",
            f"{file_name}_clouds-waters_opt.jpg",
            f"{file_name}_clouds-waters_opt.webp",
        ],
        "precipitation-waters": [
            f"{file_name}_precipitation-waters.png",
            f"{file_name}_precipitation-waters_opt.jpg",
            f"{file_name}_precipitation-waters_opt.webp",
        ],
        "visibility-waters": [
            f"{file_name}_visibility-waters.png",
            f"{file_name}_visibility-waters_opt.jpg",
            f"{file_name}_visibility-waters_opt.webp",
        ],
        "data": [
            f"{file_name}_data.csv",
        ],
    }

def export(y, x, windspeed, direction, t2, c1, precip, snow, humidity, file_names: list[str]):
    """
    Data Package for Meteogram API.
    """

    y = y[80:135, 200:255]
    x = x[80:135, 200:255]
    windspeed = windspeed[80:135, 200:255]
    direction = direction[80:135, 200:255]
    t2 = t2[80:135, 200:255]
    c1 = c1[80:135, 200:255]
    precip = precip[80:135, 200:255]
    snow = snow[80:135, 200:255]
    humidity = humidity[80:135, 200:255]

    data = np.dstack((
        y.flatten(),
        x.flatten(),
        windspeed.flatten(),
        direction.flatten(),
        t2.flatten(),
        c1.flatten(),
        precip.flatten(),
        snow.flatten(),
        humidity.flatten()
    ))

    np.savetxt(
        file_names[0],
        data[0, :, :],
        delimiter=',',
        comments='',
        header="lat,lon,windSpeed,windDirection,temp,cloud,precip,snow,humidity",
        fmt=['%.4f', '%.4f', '%.2f', '%.2f', '%.2f', '%.2f', '%.2f', '%.2f', '%.2f']
    )

class Harmonie():
    precip_dicts = []
    snow_dicts = []
    names_to_process = []

    def __init__(self):
        self.ftp = ftplib.FTP()

        if os.getenv('PYTHON_ENV') != 'dev':
            self.client = minio.Minio(
                os.getenv('S3_ENDPOINT'),
                access_key=os.getenv('S3_ACCESS_KEY'),
                secret_key=os.getenv('S3_SECRET_KEY'),
                http_client=urllib3.PoolManager(
                    cert_reqs='REQUIRED',
                    ca_certs='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt',
                ),
            )
        else:
            self.client = minio.Minio(
                os.getenv('S3_ENDPOINT'),
                access_key=os.getenv('S3_ACCESS_KEY'),
                secret_key=os.getenv('S3_SECRET_KEY'),
                secure=False,
            )

    def get_s3_names(self) -> typing.List[str]:
        result = []

        for item in self.client.list_objects('nextcloud', prefix='data/harmonie/'):
            file_name: str = item.object_name.split('data/harmonie/')[-1]

            if len(file_name) > 0:
                result.append(file_name)

        return result

    def upload_dz(self, key: str, image_path: str):
      if key == 'data':
        return

      images = []
      for folder, subs, files in os.walk(f"{image_path}_dz"):
        for file in files:
          images.append(f"{folder}/{file}")

      for image in images:
        self.client.fput_object(
            "nextcloud",
            f"data/harmonie/processor/{image}",
            image,
        )

      shutil.rmtree(f"{image_path}_dz")

    def process(self, data: io.BytesIO, name: str, old_file=False):
        file_name = name.split('.bz2')[0]

        #===========================================================================
        #===========================================================================
        # percip-patch -1
        #===========================================================================
        with open(file_name, "wb") as f:
            f.write(bz2.decompress(data.read()))
        
        model_name, time_step = file_name.split('.')

        grbs = pgr.open(file_name)
        total_rain = grbs.message(210).values

        model_dict = {'name':model_name, 'time_steps': {time_step: {'data': total_rain, 'processed': False}}}

        if not any(model_name in d['name'] for d in self.precip_dicts):
            self.precip_dicts.append(model_dict)
        else:
            old_dict = list(filter(lambda model: model['name'] == model_name, self.precip_dicts))[0]
            if not time_step in old_dict['time_steps']:
                old_dict['time_steps'][time_step] = {'data': total_rain, 'processed': False}
        
        if model_dict['time_steps'][time_step]['processed'] == True:
            os.remove(file_name)
            return

        int_time_step = int(time_step)
            
        if int_time_step >= 3:
            previous_time_step = int(time_step) -3

            if previous_time_step < 10:
                previous_time_step = '00' + str(previous_time_step)
            else:
                previous_time_step = '0' + str(previous_time_step)

            previous_dict = list(filter(lambda model: model['name'] == model_name, self.precip_dicts))[0]
            
            if not previous_time_step in previous_dict['time_steps']:
                s3_names_extra_check = self.get_s3_names()
                s3_names_extra_check.sort()
                for last_file_on_s3 in s3_names_extra_check:
                    if 'processor' in last_file_on_s3:
                        continue

                    last_file_name = last_file_on_s3.split('.bz2')[0]
                    last_model_name, last_time_step = last_file_name.split('.')
                    
                    if last_model_name == model_name and last_time_step == previous_time_step:
                        self.names_to_process.append(last_file_on_s3)
                        data = io.BytesIO()
                        self.ftp_connect()
                        self.ftp.retrbinary(f"RETR {last_file_on_s3}", data.write)
                        data.seek(0)
                        self.process(data, last_file_on_s3, True)
                        os.remove(file_name)
                        return

                os.remove(file_name)
                return

            previous_total_rain = previous_dict['time_steps'][previous_time_step]['data']

            # Convert lists to numpy.ndarray for faster processing
            previous_total_array = np.array(previous_total_rain)
            current_total_array = np.array(total_rain)
            current_array = np.subtract(current_total_array, previous_total_array)
            current_rain = current_array
        else:
            current_rain = model_dict['time_steps'][time_step]['data']
        
        current_rain = np.divide(current_rain, 3)


        # after processing set processed to true and remove from names_to_process
        model_dict['time_steps'][time_step]['processed'] = True
        # self.names_to_process.remove(name)
        if old_file:
            os.remove(file_name)
            return

        # print(type(current_rain))


        #===========================================================================
        #===========================================================================
        # percip-patch -1
        #===========================================================================
        #===========================================================================
        #===========================================================================
        # snow-1
        #===========================================================================
        
        # model_name, time_step = file_name.split('.')
        total_snow = grbs.message(225).values
        model_dict = {'name':model_name, 'time_steps': {time_step: {'data': total_snow, 'processed': False}}}

        if not any(model_name in d['name'] for d in self.snow_dicts):
            self.snow_dicts.append(model_dict)
        else:
            old_dict = list(filter(lambda model: model['name'] == model_name, self.snow_dicts))[0]
            if not time_step in old_dict['time_steps']:
                old_dict['time_steps'][time_step] = {'data': total_snow, 'processed': False}
        
        if model_dict['time_steps'][time_step]['processed'] == True:
            os.remove(file_name)
            return

        int_time_step = int(time_step)
            
        if int_time_step >= 3:
            previous_time_step = int(time_step) -3

            if previous_time_step < 10:
                previous_time_step = '00' + str(previous_time_step)
            else:
                previous_time_step = '0' + str(previous_time_step)

            previous_dict = list(filter(lambda model: model['name'] == model_name, self.snow_dicts))[0]
            
            if not previous_time_step in previous_dict['time_steps']:
                s3_names_extra_check = self.get_s3_names()
                s3_names_extra_check.sort()
                for last_file_on_s3 in s3_names_extra_check:
                    if 'processor' in last_file_on_s3:
                        continue

                    last_file_name = last_file_on_s3.split('.bz2')[0]
                    last_model_name, last_time_step = last_file_name.split('.')
                    
                    if last_model_name == model_name and last_time_step == previous_time_step:
                        self.names_to_process.append(last_file_on_s3)
                        data = io.BytesIO()
                        self.ftp_connect()
                        self.ftp.retrbinary(f"RETR {last_file_on_s3}", data.write)
                        data.seek(0)
                        self.process(data, last_file_on_s3, True)
                        os.remove(file_name)
                        return

                os.remove(file_name)
                return

            previous_total_snow = previous_dict['time_steps'][previous_time_step]['data']

            # Convert lists to numpy.ndarray for faster processing
            previous_total_array = np.array(previous_total_snow)
            current_total_array = np.array(total_snow)
            current_array = np.subtract(current_total_array, previous_total_array)
            current_snow = current_array
        else:
            current_snow = model_dict['time_steps'][time_step]['data']
        
        current_snow = np.divide(current_snow, 3)
        # current_snow = current_rain

        # after processing set processed to true and remove from names_to_process
        model_dict['time_steps'][time_step]['processed'] = True
        self.names_to_process.remove(name)
        if old_file:
            os.remove(file_name)
            return

        # print(current_snow)


        #===========================================================================
        #===========================================================================
        # snow-1
        #===========================================================================

        y, x = grbs.message(191).latlons()
        u10 = grbs.message(191).values
        v10 = grbs.message(197).values
        windspeed = np.sqrt(u10 ** 2 + v10 ** 2)
        c1 = grbs.message(215).values   # low clouds
        c2 = grbs.message(216).values   # medium clouds
        c3 = grbs.message(217).values   # high clouds
        t2 = grbs.message(181).values - 273.15
        lon_s = 25
        lat_s = -60
        humidity = grbs.message(209).values
        
        #Additional variables
        mslp=grbs.message(1).values/100 #Sea-level pressure
        temp850 = grbs.message(129).values-273.15 #Airmass Temperature
        visibility = grbs.message(190).values #Visibility
        dewpoint = grbs.message(189).values #Dew-point temperature
        maxtemp = grbs.message(187).values-273.15 #Maximum temperature
        mintemp = grbs.message(188).values-273.15 #Minimum temperature

        #Adjusting wind angles
        #a, b, and c-side of the triangle
        angle = np.ones((386,466))

        #canculating angles
        for i in range(386):
            for j in range(466):
                SB = np.sin(np.radians(x[i,j]-lon_s))*np.cos(np.radians(lat_s))
                CB = -np.sin(np.radians(lat_s))*np.cos(np.radians(y[i,j]))+np.cos(np.radians(lat_s))*np.sin(np.radians(y[i,j]))*np.cos(np.radians(x[i,j]-lon_s))
                angle[i,j] = np.rad2deg(np.arctan2(SB,CB))
            
        #adjusting wind-direction with the b-angle
        # The constant -9 has to be removed when we figure out how to adjust the angle correctly
        direction=np.mod(180+np.rad2deg(np.arctan2(u10, v10)) + angle - 9,360)
        
        #adjusted 10-meter wind speeds (u and v)
        u11 = np.sin(np.radians(direction))*windspeed*(-1)
        v11 = np.cos(np.radians(direction))*windspeed*(-1)
        uquiver = u11 / np.sqrt(u11 ** 2 + v11 ** 2) * 10
        vquiver = v11 / np.sqrt(u11 ** 2 + v11 ** 2) * 10

        file_names = get_save_file_names(file_name)

        threads = [
            multiprocessing.Process(
                target=plot_wind,
                args=(y, x, windspeed, uquiver, vquiver, file_names.get("wind"),)
            ),
            multiprocessing.Process(
                target=plot_cloud,
                args=(y, x, c1, c2, c3, file_names.get("cloud"),)
            ),
            multiprocessing.Process(
                target=plot_temp,
                args=(y, x, t2, file_names.get("temp"),)
            ),
            multiprocessing.Process(
                target=plot_precip,
                args=(y, x, current_rain, file_names.get("precip"),)
            ),
            multiprocessing.Process(
                target=plot_snow,
                args=(y, x, current_snow, file_names.get("snow"),)
            ),
            multiprocessing.Process(
                target=plot_wind_waters,
                args=(y, x, windspeed, uquiver, vquiver, mslp, file_names.get("wind-waters"),)
            ),
            multiprocessing.Process(
                target=plot_wind_waters2,
                args=(y, x, windspeed, uquiver, vquiver, mslp,file_names.get("wind-waters2"),)
            ),
            multiprocessing.Process(
                target=plot_overview_waters,
                args=(y, x, current_rain, current_snow, c1, mslp, temp850, file_names.get("overview-waters"),)
            ),
            multiprocessing.Process(
                target=plot_clouds_waters,
                args=(y, x, c1, c2, c3, mslp, temp850, file_names.get("clouds-waters"),)
            ),
            multiprocessing.Process(
                target=plot_precipitation_waters,
                args=(y, x, current_rain, current_snow, mslp,temp850, file_names.get("precipitation-waters"),)
            ),
            multiprocessing.Process(
                target=plot_visibility_waters,
                args=(y, x, visibility, mslp, file_names.get("visibility-waters"),)
            ),
            multiprocessing.Process(
                target=export,
                args=(y, x, windspeed, direction, t2, c1, current_rain, current_snow, humidity, file_names.get("data"),)
            ),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        
        for value in file_names.values():
            for item in value:
                self.client.fput_object(
                    "nextcloud",
                    f"data/harmonie/processor/{item}",
                    item,
                )
            
                os.remove(item)

        os.remove(file_name)

    def ftp_connect(self):
        self.ftp.connect(os.getenv('FTP_HOST'), int(os.getenv('FTP_PORT')))
        self.ftp.login(os.getenv('FTP_USER'), os.getenv('FTP_PASS'))

    def run(self):
        self.ftp_connect()
        ftp_names: typing.List[str] = []
        for item in self.ftp.nlst():
            if validate_time(item) and '.md5' not in item:
                ftp_names.append(item)

        print(f"Got FTP names")

        s3_names = self.get_s3_names()

        print(f"Got S3 names")
        the_names = list(set(ftp_names) - set(s3_names))
        the_names.sort()

        # for name in list(set(ftp_names) - set(s3_names)).sort():
        for name in the_names:
            # precip-patch-1
            self.names_to_process.append(name)

            data = io.BytesIO()

            self.ftp_connect()
            self.ftp.retrbinary(f"RETR {name}", data.write)
            
            data.seek(0)
            self.process(data, name)

            # precip-patch-1
            if not name in self.names_to_process:
                data.seek(0)
                self.client.put_object('nextcloud', f"data/harmonie/{name}", data, -1, part_size=10*1024*1024)
            else:
                pass

        # precip-patch-1
        for name in self.names_to_process:
            data = io.BytesIO()

            self.ftp_connect()
            self.ftp.retrbinary(f"RETR {name}", data.write)
            
            data.seek(0)
            self.process(data, name)

            if not name in self.names_to_process:
                print(f"debug: precip-patch-1-branch-0")
                data.seek(0)
                self.client.put_object('nextcloud', f"data/harmonie/{name}", data, -1, part_size=10*1024*1024)
        # precip-patch-1

        print(f"Got FTP and S3 diff")

        for name in list(set(s3_names) - set(ftp_names)):
            try:
                self.client.remove_object('nextcloud', f"data/harmonie/{name}")
                
                file_name = name.split(".bz2")[0]
                file_names = get_save_file_names(file_name)

                for value in file_names.values():
                    for item in value:
                        self.client.remove_object(
                            'nextcloud',
                            f"data/harmonie/processor/{item}"
                        )
            except Exception as e:
                print(e)

        print(f"Removed S3 and FTP diff")
        
        # precip-patch-1
        self.names_to_process = []
        self.precip_dicts = []
