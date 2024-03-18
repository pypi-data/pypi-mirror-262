# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import YW_download




# Copernicus Data Space Credential
credentials = ["abc", "123"]

images = '/Users/yw/Desktop/230306 ODW_OSW/231205 Galen geotiff/images.csv'

out_folder = '/Volumes/San2T/test_download'


YW_download.run(credentials, images, out_folder)













