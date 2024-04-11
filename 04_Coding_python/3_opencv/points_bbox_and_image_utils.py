import cv2


def convert_point_follow_image_resize(boxes, w_img_ori, h_img_ori):
    """
    :param boxes:
    Ex: [[  10   10]
         [1910   10]
         [1910 1070]
         [  10 1070]]
    :param w_img_ori: cam.width
    :param h_img_ori: cam.height
    :return:
    """
    resize_shape = (500, 300)
    w_scale = resize_shape[0] / w_img_ori
    h_scale = resize_shape[1] / h_img_ori
    for point in boxes:
        point[0] *= w_scale
        point[1] *= h_scale
    return boxes
