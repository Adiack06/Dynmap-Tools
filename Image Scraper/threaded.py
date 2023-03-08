import os
import requests
import concurrent.futures
from io import BytesIO
from PIL import Image

def download_tile(x, z,xl, yl):
    zoomout = 0
    scaling_factor = 1
    center_x = 0
    center_z = -17
    tile_size = 32
    scaled_x = int((x - center_x) * scaling_factor + (tile_size / 2))
    scaled_y = int(-(z - center_z) * scaling_factor + (tile_size / 2))


    divided_x = scaled_x >> 5
    divided_y = scaled_y >> 5
    shifted_x = round(scaled_x / 1024)
    shifted_y = round(scaled_y / 1024)
    zoom_prefix = 'z' * zoomout
    print(shifted_x)
    print(shifted_y)
    print(zoom_prefix)
    print(divided_x)
    print(divided_y)
    url = f'http://shenanigans-group.com:8090/tiles/ShenanigansEM_S8v2/flat/{shifted_x}_{shifted_y}/{zoom_prefix}{divided_x}_{divided_y}.png'
    print(url)
    image = requests.get(url)
    img = Image.open(BytesIO(image.content))
    folder_path = f"image/line{yl}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    tile_path = f"{folder_path}/{yl}-{xl}.png"
    if not os.path.exists(tile_path):
        img.save(tile_path)
    img.close()

x1 = 2998.66
z1 = -10409
x2 = 4355
z2 = -9429
rangex = int(abs((x1-x2)/32))
rangey = int(abs((z1-z2)/32))


done = 0
todo = rangex * rangey
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    for yl in range(rangey):
        for xl in range(rangex):
            executor.submit(download_tile(x1+(32*xl), z1+(32*yl), xl, yl))
            done += 1
            print(f"{done} out of {todo}")