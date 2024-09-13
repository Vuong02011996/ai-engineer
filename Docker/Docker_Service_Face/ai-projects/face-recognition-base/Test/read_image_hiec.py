from PIL import Image
from pillow_heif import register_heif_opener
import pillow_heif
import pyheif
import io
import whatimage
import requests
import numpy as np

url_test = "https://file.erp.clover.edu.vn/file-storage/2022/08/20220812/3a05a43c-47a5-b1b6-229a-3a4b1e1ec313.HEIC"

def read1():
    register_heif_opener()
    image = Image.open('https://file.erp.clover.edu.vn/file-storage/2022/08/20220812/3a05a43c-475a-406b-daf8-7fbbe5614697.HEIC')
    print(image)


def read2():
    heif_file = pillow_heif.read_heif("https://file.erp.clover.edu.vn/file-storage/2022/08/20220812/3a05a43c-475a-406b-daf8-7fbbe5614697.HEIC")
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )


def read3():
    from PIL import Image
    import pyheif

    heif_file = pyheif.read("/home/gg_greenlab/Downloads/3a05a43c-47a5-b1b6-229a-3a4b1e1ec313.HEIC")
    # heif_file = pyheif.read(open("/home/gg_greenlab/Downloads/3a05a43c-47a5-b1b6-229a-3a4b1e1ec313.HEIC", "rb").read())

    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    a = 0


def decodeImage(bytesIo):
    response = requests.get(bytesIo)
    # img = io.BytesIO(response.content)
    bytesIo = response.content
    fmt = whatimage.identify_image(response.content)
    if fmt in ['heic', 'avif']:
        i = pyheif.read(bytesIo)

        # Extract metadata etc
        for metadata in i.metadata or []:
            if metadata['type'] == 'Exif':
                a = 0
        # do whatever

        # Convert to other file format like jpeg
        s = io.BytesIO()
        pi = Image.frombytes(
            mode=i.mode, size=i.size, data=i.data)

        pi.save(s, format="jpeg")


if __name__ == '__main__':
    decodeImage(url_test)