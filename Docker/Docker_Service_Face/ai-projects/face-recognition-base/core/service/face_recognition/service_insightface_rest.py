import time
import requests
from core.main.main_utils.helper import file2base64, read_image_url_reshape_and_to_base64
from glob import glob
import os


def extract_embedding_image_folder(ims):
    """
    :param ims: list img path, example ims = glob(os.path.join(impaths, "*.png"))
    :return: data embedding
    """
    target = [file2base64(path) for path in ims]
    req = {"images": {"data": target}, "embed_only": True}
    start_time = time.time()
    port_model_insight = int(os.getenv("port_model_insight"))
    ip_run_service_insight = os.getenv("ip_run_service_insight")
    resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
    data = resp.json()
    print("Reponse cost: ", time.time() - start_time)
    return data


def extract_embedding_image_minio(list_img_url):
    """
    :param list_img_url: list img url in minio
    :return: data embedding
    """
    target = []
    list_img_url_filter = []
    for i in range(len(list_img_url)):
        img_base64 = read_image_url_reshape_and_to_base64(list_img_url[i])
        if img_base64 is not None:
            target.append(img_base64)
            list_img_url_filter.append(list_img_url[i])
    if len(target) > 0:
        req = {"images": {"data": target}, "embed_only": True}
        start_time = time.time()
        port_model_insight = int(os.getenv("port_model_insight"))
        ip_run_service_insight = os.getenv("ip_run_service_insight")
        resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
        data = resp.json()
        print("Reponse cost: ", time.time() - start_time)

        embedding_vectors = list(map(lambda x: x['vec'], data["data"]))
        return embedding_vectors, list_img_url_filter
    else:
        return None, None


def detect_face_extract_embedding_image_minio(list_img_url):
    """
    :param list_img_url: list img url in minio
    :return: data embedding
    """
    target = []
    list_img_url_filter = []
    for i in range(len(list_img_url)):
        img_base64 = read_image_url_reshape_and_to_base64(list_img_url[i])
        if img_base64 is not None:
            target.append(img_base64)
            list_img_url_filter.append(list_img_url[i])
    if len(target) > 0:
        req = {"images": {"data": target}, "embed_only": True}
        start_time = time.time()
        port_model_insight = int(os.getenv("port_model_insight"))
        ip_run_service_insight = os.getenv("ip_run_service_insight")
        resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
        data = resp.json()
        print("Reponse cost: ", time.time() - start_time)

        embedding_vectors = list(map(lambda x: x['vec'], data["data"]))
        return embedding_vectors, list_img_url_filter
    else:
        return None, None


if __name__ == '__main__':
    images_path = '/home/oryza/Pictures/image_test'
    ims = glob(os.path.join(images_path, "*.jpg"))
    extract_embedding_image_folder(ims)