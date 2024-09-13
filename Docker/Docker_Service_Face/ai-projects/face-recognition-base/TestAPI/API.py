import requests
import cv2
import io
import PIL.Image as Image


def get_list(limit,page):
    '''
    get list of objects
    input: 
        - limit:
        - page:
    ouput:
        - result of file json
        we can filter necessary imformation for face recognition module
    '''
    params = {'limit': limit, 'page': page}
    url = "https://gsdl-dev-api.greenglobal.vn/api/v1/ai/tour-guides"
    response = requests.get(url=url, params=params)
    result = response.json()
    # print(result)
    return result


def post_image(img_path):
    '''
    post an image
    input:
        - img_path: path of image
    output:
        - path: response a path of image on server
        this path is used for post general data and get image from server
    '''
    url = "https://gsdl-dev-api.greenglobal.vn/api/v1/upload"
    files = {'file': open(img_path, 'rb')}

    post = requests.post(url=url, files=files)
    res = post.json()
    # print(res)
    path = res['path']
    return path


def post_video():
    url = "https://gsdl-dev-api.greenglobal.vn/api/v1/upload?file"

    payload = {}
    files = [
        ('file', ('test_post.mp4', open('/home/gg-greenlab/Downloads/test_post.mp4', 'rb'), 'application/octet-stream'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    a = 0


def post_data(payload):
    '''
    post data
    input:  
        - payload
            event_type_id:          id loại sự kiện
            tourist_destination_id: id khu điểm
            warning_level:          mức độ cảnh báo (LOW, MEDIUM, HIGH, EMERGENCY)
            time:                   thời gian diễn ra sự kiện
            tour_guide_id:          id đối tượng
            camera_id:              id camera quan sát
            image_path:             hình ảnh quan sát
            video_path:             video quan sát
    example:
        payload = {
            "event_type_id": "4aa58748-a62b-4b31-b303-7f5f6e03d037",
            "tourist_destination_id": "55ef5ba5-b5a7-482b-a513-85594ff99266",
            "warning_level": "HIGH",
            "time": "2021-01-01 08:00:01",
            "tour_guide_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
            "camera_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
            "image_path": "files/ATykenGixiTYfdhNvm7RV7H9CWPWeDrS5KFZ44Ak.jpg",
            "video_path": "files/ATykenGixiTYfdhNvm7RV7H9CWPWeDrS5KFZ44Ak.jpg"
            }
    output: 
        - response of request
    '''
    url = "https://gsdl-dev-api.greenglobal.vn/api/v1/ai/events"
    result = requests.post(url=url, data=payload)
    # print(result.json())
    return result.json()


def get_image(path):
    '''
    get image
    input:
        - path: path of image on server
    output:
        - image: image
    '''
    url = "https://gsdl-dev-storage.greenglobal.vn/dltm/" + path
    response = requests.get(url=url).content
    image = Image.open(io.BytesIO(response))
    # image.save("image.jpg")
    return image


def test_get_list_info():
    item_in_page = 10
    result = get_list(limit=1, page=1)
    total_page = result["meta"]["pagination"]["total"]
    num_page = int(total_page / item_in_page) + 1
    for i in range(num_page):
        result = get_list(limit=item_in_page, page=i + 1)
        print(result)


if __name__ == '__main__':
    # ### get list info ###
    # test_get_list_info()

    # ### post image ###
    # img_path = "index.jpg"
    # path = post_image(img_path)
    # print(path)
    # #
    # # ### post data ###
    # payload = {
    #     "event_type_id": "4aa58748-a62b-4b31-b303-7f5f6e03d037",
    #     "tourist_destination_id": "55ef5ba5-b5a7-482b-a513-85594ff99266",
    #     "warning_level": "MEDIUM",
    #     "time": "2021-01-01 08:00:01",
    #     "tour_guide_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
    #     "camera_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
    #     "image_path": path,
    #     "video_path": path
    # }
    # res = post_data(payload= payload)
    # print(res)
    # #
    # ### get_image ###
    # image = get_image(path= path)
    # image.save("image.jpg")
    # post_video()

    url_in_out_roll_call = "https://erp-clover-dev-api-laravel.demo.greenglobal.vn/api/v1/ai/in-out-histories"
    payload = {
        "studentId": "3a015f9d-9e3e-d62c-fe18-3394ae8018a3",
        "attendedAt": "2022-02-14T07:27:00Z",
        "fileImage": "https://erp-clover-file.demo.greenglobal.com.vn/file-storage/2022/02/20220214/3a02094d-821f-a495-7b8e-4d9aa85e9943.png"
    }
    result = requests.post(url=url_in_out_roll_call, data=payload)
    print(result.json())
    print(result.json()["status"])