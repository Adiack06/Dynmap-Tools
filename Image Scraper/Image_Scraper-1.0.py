import os
import requests
import threading
from io import BytesIO
from PIL import Image


class downloading:
    def download_tile(self,xl, yl):
        zoom_out = 0
        scaling_factor = 1
        center_x = 0
        center_z = -17
        tile_size = 32
        scaled_x = int((xl - center_x) * scaling_factor + (tile_size / 2))
        scaled_y = int(-(yl - center_z) * scaling_factor + (tile_size / 2))

        divided_x = scaled_x >> 5
        divided_y = scaled_y >> 5
        shifted_x = round(scaled_x / 1024)
        shifted_y = round(scaled_y / 1024)
        zoom_prefix = 'z' * zoom_out
        url = f'http://shenanigans-group.com:8090/tiles/ShenanigansEM_S8v2/flat/{shifted_x}_{shifted_y}/{zoom_prefix}{divided_x}_{divided_y}.png'
        
        image = requests.get(url)
        img = Image.open(BytesIO(image.content))
        folder_path = f"image/line{yl}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        tile_path = f"{folder_path}/{yl}-{xl}.png"
        img.save(tile_path)
    
    def __init__(self, xl, yl):
        t = threading.Thread(target=self.download_tile(xl, yl))
        t.start()

x1 = 2998.66
z1 = -10409
x2 = 4355
z2 = -9429
rangex = int(abs((x1-x2)/32))
rangey = int(abs((z1-z2)/32))


done = 0
todo = rangex * rangey
for yl in range(rangey):
    for xl in range(rangex):
        downloading(xl,yl)
        done += 1
        print(f"{done} out of {todo}")
    images = [Image.open(f'image/line{yl}/{yl}-{xl}.png') for xl in range(rangex)]
    result_width = rangex *128
    result_height = 128
    result = Image.new('RGB', (result_width, result_height))
    for i, im in enumerate(images):
        result.paste(im=im, box=(128 * i, 0, 128 * (i + 1), result_height))
    if not os.path.exists('image/concatenated'):
        os.makedirs('image/concatenated')
    result.save(f'image/concatenated/line{yl}.png')  # Save concatenated image
    line_images.clear()  # Clear the list for the next iteration of the outer loop

images = [Image.open(f'image/concatenated/line{yl}.png') for yl in range(rangey)]
result_width = rangex *128
result_height = rangey *128
result = Image.new('RGB', (result_width, result_height))
for i, im in enumerate(images):
    result.paste(im=im, box=(0, 128 * i, result_width, 128 * (i + 1)))
result.save(f'image/done.png')  # Save concatenated image
line_images.clear()  # Clear the list for the next iteration of the outer loop
