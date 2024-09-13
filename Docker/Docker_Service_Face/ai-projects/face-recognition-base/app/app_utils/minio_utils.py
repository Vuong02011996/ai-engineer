import io
import traceback
from datetime import datetime
from io import BytesIO
from PIL import Image
import cv2
import requests
import numpy as np
from sentry_sdk import capture_message

from app.app_utils.file_io_untils import ip_run_service_ai
from connect_db import connect_minio

minio_client, bucket_name, host_domain = connect_minio()


def upload_image(image, bucket=bucket_name, folder_name="group", image_name="test1"):
    """
    Upload image into MinIO Server. Parse the path of image and upload to
    server.
    :param image: numpy array
    :param bucket: bucket name in minio
    :param folder_name: folder in bucket
    :param image_name:
    :param mode_rgb:
    :return:
    """
    # img_name = "{}/{}.jpg".format(folder_name, generate_rand_string(30))
    img_name = "{}/{}.jpeg".format(folder_name, image_name)

    # Make  bucket if not exist.
    found = minio_client.bucket_exists(bucket)
    if not found:
        minio_client.make_bucket(bucket)
    try:
        image = Image.fromarray(image)

        out_img = io.BytesIO()

        image.save(out_img, quality=100, format="jpeg")
        out_img.seek(0)

        minio_client.put_object(
            bucket, img_name, out_img, length=out_img.getbuffer().nbytes, content_type="image/jpeg",
        )

    except Exception as e:
        print(e)
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        return
    url = "{}/{}/{}".format(host_domain, bucket, img_name)
    url = minio_client.presigned_get_object(bucket, img_name)
    return url


def upload_video(path, bucket=bucket_name, folder_name="group", video_name="test1.mp4"):
    """Upload video into MinIO Server. Parse the path of video and upload to
    server.

    Args:
        path (str): video path
    Returns:
        url (str):
    """
    try:
        minio_client.fput_object(bucket_name, video_name, file_path=path, content_type="video/mp4")
    except Exception as e:
        print(e)
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        return

    # return "{}/{}/{}".format(host, bucket, video_name)
    return minio_client.presigned_get_object(bucket, video_name)


def upload_file(path, name, content_type, bucket_name="local", folder_name="statistics"):
    try:
        video_name = f"{folder_name}/{name}"
        minio_client.fput_object(bucket_name, video_name, file_path=path, content_type=content_type)
    except Exception as error:
        logger.critical(error)
        return

    return "{}/{}/{}".format(host, bucket, video_name)


def read_url_img_minio_to_array(url):
    response = requests.get(url)
    img_base64 = Image.open(BytesIO(response.content))
    # if the image mode is not RGB, convert it
    if img_base64.mode != "RGB":
        img_base64 = img_base64.convert("RGB")
    img_arr = np.array(img_base64)
    # cv2.imwrite("/home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Minio/test2.png", img_array)
    return img_arr


def read_stream_img(url, timeout=0.6):
    """
    :param url: url in minio
    :param timeout:
    :return: numpy array
    """
    i = 0
    response = None
    while i < 5:
        try:
            i += 1
            response = requests.get(url, timeout=timeout)
        except Exception as e:
            print(e)
            print("Error read_stream_img")
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")

        if response is not None:
            break

    if response is None:
        return response

    return np.array(Image.open(io.BytesIO(response.content)))


def image_array_from_object_name(bucket="clover", object_name="/group/test1.jpg"):
    data = minio_client.get_object(bucket_name=bucket, object_name=object_name)
    img_base64 = Image.open(BytesIO(data.data))
    # if the image mode is not RGB, convert it
    if img_base64.mode != "RGB":
        img_base64 = img_base64.convert("RGB")
    img_arr = np.array(img_base64)
    # cv2.imwrite("/home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Minio/test.png", img_array)
    return img_arr


def delete_folder(bucket_name, folder_name):
    # Delete using "remove_object"
    objects_to_delete = minio_client.list_objects(bucket_name, prefix=folder_name, recursive=True)
    for obj in objects_to_delete:
        minio_client.remove_object(bucket_name, obj.object_name.replace("+", " "))


def get_info_minio(bucket_name, folder_name):
    objects_info = minio_client.list_objects(bucket_name, prefix=folder_name, recursive=True)
    for obj in objects_info:
        result = minio_client.stat_object(bucket_name, obj.object_name)
        print(
            "last-modified: {0}, size: {1}".format(
                result.last_modified, result.size,
            ),
        )


if __name__ == '__main__':
    img = cv2.imread("/home/gg-greenlab/Downloads/index.jpg")
    url_image = upload_image(img)
    print(url_image)
    url_domain = "https://minio.core.greenlabs.ai" + url_image.split("11039")[1]
    print(url_domain)
    a = 0
    # # url_image = "https://minio.core.greenlabs.ai/local/processed3.jpeg"
    # print(url_image)
    img_array = read_url_img_minio_to_array(url_image)
    print(img_array)
    # delete_folder(bucket_name="local", folder_name="Clover_anh_vung_an_toan")
    # get_info_minio(bucket_name="local", folder_name="clover")