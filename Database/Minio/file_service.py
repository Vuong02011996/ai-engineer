import os
import io
import logging
from minio import Minio
from PIL import Image
import cv2
import requests
import numpy as np
from minio.error import ResponseError
import random
from app.utils.common import logger_handler
from concurrent.futures import ThreadPoolExecutor

# LOGGER
logger = logging.getLogger("app/utils/file_service")
logger.addHandler(logger_handler())
logger.setLevel(os.getenv("DATABASE_LEVEL"))

host = os.getenv("MINIO_HOST").split("//")[1]
host = "{}:{}".format(host, os.getenv("MINIO_PORT"))
bucket = os.getenv("MINIO_BUCKET")

access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")
is_secure = os.getenv("MINIO_HOST").split(":")[0] == "https"

minio_client = Minio(host, access_key=access_key, secret_key=secret_key, secure=is_secure)

# host = ("https://" if is_secure else "http://") + host
host = "https://minio.core.greenlabs.ai"


def generate_rand_string(length):
    character_str = "qwertyuiopasdfghjklzxcvbnm1234567890"
    characters = [string for string in character_str]

    return "".join(random.choices(characters, k=length))


def upload_image(image, folder_name="avatar", mode_rgb="BRG"):
    """Upload image into MinIO Server. Parse the path of image and upload to
    server.

    Args:
        image (np.array): 1_numpy array image
        folder_name(str): Folder Name on MinIO server
    
    Returns:
        url
    """
    img_name = "{}/{}.jpg".format(folder_name, generate_rand_string(30))

    logger.debug(f"img_name: {img_name}")

    try:
        logger.debug(image.shape)
        logger.debug(type(image))
        if mode_rgb == "BRG":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        out_img = io.BytesIO()

        image.save(out_img, quality=100, format="jpeg")
        out_img.seek(0)

        minio_client.put_object(
            bucket, img_name, out_img, length=out_img.getbuffer().nbytes, content_type="image/jpeg",
        )

    except Exception as error:
        logger.critical(error)
        return

    return "{}/{}/{}".format(host, bucket, img_name)


def download_image(url, bucket_name="local", folder_name="avatar"):
    """Download image from MINIO Server

    Args:
        url (str): full path of image, for example:
        "http://core.greenlabs.ai:11039/local/avatar/rcekco6xkm.jpg"
    """

    file_path = os.path.join(folder_name, os.path.basename(url))
    logger.info(f"File path: {file_path}")
    local_path = "core/avatar/outputs/temp.jpeg"

    data = minio_client.get_object(bucket_name, file_path)
    try:
        with open(local_path, "wb") as file_data:
            file_data.write(data.read())
    except ResponseError as error:
        logger.critical(error)
        return
    return local_path


def upload_video(path, bucket_name="local", folder_name="videos"):
    """Upload video into MinIO Server. Parse the path of video and upload to
    server.

    Args:
        path (str): video path
    Returns:
        url (str): 
    """
    try:
        video_name = f"{folder_name}/{generate_rand_string(10)}.mp4"
        minio_client.fput_object(bucket_name, video_name, file_path=path, content_type="video/mp4")
    except Exception as error:
        logger.critical(error)
        return

    return "{}/{}/{}".format(host, bucket, video_name)


def upload_file(path, name, content_type, bucket_name="local", folder_name="statistics"):
    try:
        video_name = f"{folder_name}/{name}"
        minio_client.fput_object(bucket_name, video_name, file_path=path, content_type=content_type)
    except Exception as error:
        logger.critical(error)
        return

    return "{}/{}/{}".format(host, bucket, video_name)


def read_stream_img(path, timeout=0.6):
    i = 0
    response = None

    while i < 5:
        try:
            i += 1
            response = requests.get(path, timeout=timeout)
        except Exception as e:
            print(e)
            print("Error read_stream_img")
            pass

    if response is None:
        return response

    return np.array(Image.open(io.BytesIO(response.content)))


def parse_img_to_stream(numpy_image):
    img_crop_pil = Image.fromarray(numpy_image)
    byte_io = io.BytesIO()
    img_crop_pil.save(byte_io, format="jpeg")

    return byte_io


def download_one(url, size_img=100):
    arr_image = read_stream_img(url)
    arr_image = cv2.resize(arr_image, (size_img, size_img), interpolation=cv2.INTER_AREA)
    return arr_image


def download_images(urls, size_img=100):
    """
    Create a thread pool and download specified urls
    """
    futures_list = []
    results = []
    size_imgs = [size_img] * len(urls)

    with ThreadPoolExecutor(max_workers=5) as executor:
        for url, size in zip(urls, size_imgs):
            futures = executor.submit(download_one, url, size)
            futures_list.append(futures)

        for future in futures_list:
            try:
                result = future.result(timeout=60)
                results.append(result)
            except Exception:
                results.append(None)
    return results

