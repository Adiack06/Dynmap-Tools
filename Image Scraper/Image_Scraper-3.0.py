import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

class DynmapPage:
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.maps = []

class Map:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class ImageProcessingThread(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int)

    def __init__(self, x1, z1, x2, z2, of):
        super().__init__()
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2
        self.of = of

    def run(self):
        x1 = self.x1
        z1 = self.z1
        x2 = self.x2
        z2 = self.z2

        rangex = int(abs((x1 - x2) / 32))
        rangey = int(abs((z1 - z2) / 32))

        todo = rangex * rangey
        done = 0
        for yl in range(rangey):
            for xl in range(rangex):
                self.download_tile(x1 + (32 * xl), z1 + (32 * yl), xl, yl)
                done += 1
                progress = int((done / todo) * 50)
                self.progressSignal.emit(progress)
                print(f"{done} out of {todo}")
        done = 0
        for line in range(rangey):
            self.line_concatinate(line, xl, rangex)
            done += 1
            progress = progress + int((done / rangey) * 50)
            self.progressSignal.emit(progress)
            print(f"{done} out of {rangey}")

        images = [Image.open(f'image/concatenated/line{yl}.png') for yl in range(rangey)]
        result_width = rangex * 128
        result_height = rangey * 128
        result = Image.new('RGB', (result_width, result_height))
        for i, im in enumerate(images):
            result.paste(im=im, box=(0, 128 * i, result_width, 128 * (i + 1)))
        result.save(f'{self.of}/done.png')  # Save concatenated image
        images.clear()  # Clear the list for the next iteration of the outer loop
        folder_path = "image"
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)

        # os.rmdir(folder_path)
        progress = 100
        self.progressSignal.emit(progress)

    def download_tile(self, x, z, xl, yl):
        zoomout = 0
        scaling_factor = 1
        center_x = 0
        center_z = -17
        tile_size = 32
        scaled_x = int((x - center_x) * scaling_factor + (tile_size / 2))
        scaled_y = int(-(z - center_z) * scaling_factor + (tile_size / 2))

        divided_x = scaled_x >> 5
        divided_y = scaled_y >> 5
        shifted_x = scaled_x // 1024
        shifted_y = scaled_y // 1024
        zoom_prefix = 'z' * zoomout
        url = f'http://shenanigans-group.com:8090/tiles/ShenanigansEM_S10/flat/{shifted_x}_{shifted_y}/{zoom_prefix}{divided_x}_{divided_y}.png'
        image = requests.get(url)
        img = Image.open(BytesIO(image.content))
        folder_path = f"image/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        tile_path = f"{folder_path}/{yl}-{xl}.png"
        print(tile_path)
        if not os.path.exists(tile_path):
            img.save(tile_path)
        img.close()

    def line_concatinate(self, line, xl, rangex, ):
        images = [Image.open(f'image/{line}-{xl}.png') for xl in range(rangex)]
        result_width = rangex * 128
        result_height = 128
        result = Image.new('RGB', (result_width, result_height))
        for i, im in enumerate(images):
            result.paste(im=im, box=(128 * i, 0, 128 * (i + 1), result_height))
        if not os.path.exists('image/concatenated'):
            os.makedirs('image/concatenated')
        result.save(f'image/concatenated/line{line}.png')  # Save concatenated image

    def set_output_location(self):
        self.folder_path = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )
        # Perform any necessary processing with the selected folder path

    def start_image_processing(self):
        x1 = int(self.x1_text.text())
        z1 = int(self.y1_text.text())
        x2 = int(self.x2_text.text())
        z2 = int(self.y2_text.text())
        of = self.folder_path

        self.thread = ImageProcessingThread(x1, z1, x2, z2, of)
        self.thread.progressSignal.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
