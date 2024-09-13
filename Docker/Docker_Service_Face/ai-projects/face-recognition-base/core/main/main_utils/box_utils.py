import cv2

# https://christianbernecker.medium.com/convert-bounding-boxes-from-coco-to-pascal-voc-to-yolo-and-back-660dc6178742


def bbox2points(bbox):
    """
    From bounding box yolo format: x_center, y_center, w, h
    to corner points cv2 rectangle
    """
    x, y, w, h = bbox
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def to_tlwh(tlbr):
    """Convert bounding box to format `(min x, min y, max x, max y)`, i.e.,
    `(top left, bottom right)`.
    """
    ret = tlbr.copy()
    # ret[2:] += ret[:2]
    box = []
    for bbox in ret:
        w = int(bbox[2]) - int(bbox[0])
        h = int(bbox[3]) - int(bbox[1])
        box.append([int(bbox[0]) + w/2, int(bbox[1]) + h/2, w, h])
    return box


def tlwh_to_pascal_voc(top, left, w, h,  image_w, image_h):
    w = w * image_w
    h = h * image_h
    x = top * image_w
    y = left * image_h
    x1 = int(round(x))
    x2 = int(round(x + w))
    y1 = int(round(y))
    y2 = int(round(y + h))
    return [x1, y1, x2, y2]

def xywh2xyxy(bbox):
    """
    From bounding box yolo format x_center, y_center, w, h
    to corner points cv2 rectangle
    """
    x, y, w, h = bbox
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def extend_bbox(box, shape_image, ext_w=10, ext_h=10):
    h, w, _ = shape_image
    x1_ext = max(0, box[0] - ext_w)
    y1_ext = max(0, box[1] - ext_h)
    x2_ext = min(w, box[2] + ext_w)
    y2_ext = min(h, box[3] + ext_h)
    return [x1_ext, y1_ext, x2_ext, y2_ext]


def extend_bbox_percent(box, shape_image, ext_w=0.5, ext_h=0.5):
    h, w, _ = shape_image
    w_box = box[2] - box[0]
    h_box = box[3] - box[1]
    x1_ext = max(0, box[0] - int(w_box*ext_w))
    y1_ext = max(0, box[1] - int(h_box*ext_h))
    x2_ext = min(w, box[2] + int(w_box*ext_w))
    y2_ext = min(h, box[3] + int(h_box*ext_h))
    return [x1_ext, y1_ext, x2_ext, y2_ext]


def save_bbox_head(image, boxes, frame_count, path):
    for i, box in enumerate(boxes):
        box = extend_bbox(box, image.shape)
        image_head = image[box[1]:box[3], box[0]:box[2]]
        cv2.imwrite(path + "head_" + str(frame_count) + "_" + str(i) + ".png", image_head)


def save_debug_image(frame_count, image):
    cv2.imwrite("/home/vuong/Desktop/Project/GG_Project/green-clover-montessori/new_core/debug_image/test_" + str(
        frame_count) + ".png", image)