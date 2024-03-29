import numpy as np
import numba
from numba import jit, njit
import cv2

"""
Numba syntax
Reference : https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
Method 4 and method 5 return False when all x, y is outside region not good
"""


# @jit(nopython=True)
def point_in_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x, p1y = poly[0]
    for i in numba.prange(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


# @njit(parallel=True, nopython=True)
# @njit(nopython=True)
# @njit
def parallel_point_in_polygon(points, polygon):
    # D = np.empty(len(points), dtype=numba.boolean)
    D = np.empty(len(points))
    for i in numba.prange(0, len(D)):
        D[i] = point_in_polygon(points[i, 0], points[i, 1], polygon)
    return D


# @njit(nopython=True)
def select_bbox_inside_polygon(detections, polygon):
    """

    :param detections: detections [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...]
    :param polygon: [[x1, y1], [x2, x2], ... , [xN, yN]]
    :return:
    """

    list_idx_bbox_del = []
    list_idx_bbox_remain = []
    for idx, bbox in enumerate(detections):
        full_bbox = [[bbox[0], bbox[1]],  # x1, y1
                     [bbox[2], bbox[1]],  # x2, y1
                     [bbox[0], bbox[3]],  # x1, y2
                     [bbox[2], bbox[3]]]  # x2, y2
        full_bbox = np.array(full_bbox)
        inside = parallel_point_in_polygon(full_bbox, polygon)

        if False in inside:
            list_idx_bbox_del.append(idx)
        else:
            list_idx_bbox_remain.append(idx)

    # remove bbox not inside the region track
    if len(list_idx_bbox_del) > 0:
        # print(detections)
        # del detections[idx]  # NumPy arrays are fixed in size. Use np.delete instead.
        detections = np.delete(detections, np.array(list_idx_bbox_del), 0)
        # print(detections)

    return detections, list_idx_bbox_del, list_idx_bbox_remain


def select_bbox_inside_many_resions(detections, polygon):
    """
    Tương tự như hàm select_bbox_inside_polygon ở trên nhưng xử lí 2 trường hợp polygon có nhiều vùng(mảng 3 chiều
    và có một vùng mảng 2 chiều), tức là thay thế hàm select_bbox_inside_polygon = select_bbox_inside_many_resions
    :param detections: detections [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...]
    :param polygon: [[[x1, y1], [x2, x2], ... , [xN, yN]], [[x1, y1], [x2, x2], ... , [xN, yN]]]
    :return:
    """
    regions = np.array(polygon)
    # Nếu trường hợp tọa độ là mảng 3 chiều(nhiều vùng)
    # Ta phải xử lí từng vùng sau đó concat các head từ detections lại với nhau.
    if regions.ndim == 3:
        detections_concat = None
        list_idx_bbox_remain_concat = None
        for region in regions:
            detections_region, list_idx_bbox_del, list_idx_bbox_remain = select_bbox_inside_polygon(detections, region)
            if detections_concat is None:
                detections_concat = detections_region
                list_idx_bbox_remain_concat = list_idx_bbox_remain
            else:
                detections_concat = np.concatenate((detections_region, detections_concat), axis=0)
                list_idx_bbox_remain_concat = np.concatenate((list_idx_bbox_remain, list_idx_bbox_remain_concat), axis=0)
    else:
        # Xóa bớt index nằm ngoài: [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],[x1,y1,x2,y2,score]]
        # Out [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score]]
        detections_concat, list_idx_bbox_del, list_idx_bbox_remain_concat = select_bbox_inside_polygon(detections, polygon)

    # list_idx_bbox_del_concat ở đây concat các list index đã xóa lại sẽ không đúng .
    # Nên dùng cách lấy tổng index - index remain sẽ lấy được index đã xóa.
    arr_set = set(range(len(detections)))
    sub_indices_set = set(list_idx_bbox_remain_concat)
    # Lấy tập hợp chứa các chỉ số còn lại bằng toán tử set difference
    result_set = arr_set - sub_indices_set
    list_idx_bbox_del_concat = list(result_set)
    return detections_concat, list_idx_bbox_del_concat


@jit(nopython=True)
def extend_bbox_track(bbox_trk, time_since_update, w_ext=0.05, h_ext=0.05):
    ext_w = time_since_update * w_ext
    ext_h = time_since_update * h_ext
    trk_w = bbox_trk[2] - bbox_trk[0]
    trk_h = bbox_trk[3] - bbox_trk[1]
    x1_ext = bbox_trk[0] - trk_w * ext_w / 2
    y1_ext = bbox_trk[1] - trk_h * ext_h / 2
    x2_ext = bbox_trk[2] + trk_w * ext_w / 2
    y2_ext = bbox_trk[3] + trk_h * ext_h / 2
    return [x1_ext, y1_ext, x2_ext, y2_ext]



# @jit
@jit(nopython=True)
def iou(bb_det, bb_trk):
    """
  Computes IOU (Intersection Over Union) between two bounding boxes in the form [x1,y1,x2,y2]
  """
    xx1 = np.maximum(bb_det[0], bb_trk[0])
    xx2 = np.minimum(bb_det[2], bb_trk[2])
    w = np.maximum(0., xx2 - xx1)
    if w == 0:
        return 0
    yy1 = np.maximum(bb_det[1], bb_trk[1])
    yy2 = np.minimum(bb_det[3], bb_trk[3])
    h = np.maximum(0., yy2 - yy1)
    if h == 0:
        return 0
    wh = w * h
    area_det = (bb_det[2] - bb_det[0]) * (bb_det[3] - bb_det[1])
    area_trk = (bb_trk[2] - bb_trk[0]) * (bb_trk[3] - bb_trk[1])
    o = wh / (area_det + area_trk - wh)
    return o


def draw_track_bbs_and_det_bbs_to_image(image, track_bbs_ext=None, det_bbs=None, unm_trk_list=None, line_thickness=1):
    if track_bbs_ext is not None:
        for b in track_bbs_ext:
            xmin, ymin, xmax, ymax = list(map(int, b))
            color = (0, 0, 0)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            cv2.putText(image, "track_ext", (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        1)
    if det_bbs is not None:
        for b in det_bbs:
            xmin, ymin, xmax, ymax = list(map(int, b))
            color = (255, 255, 255)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            # put id track to image
            cv2.putText(image, "detect", (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        1)

    if unm_trk_list is not None:
        for b in unm_trk_list:
            xmin, ymin, xmax, ymax = list(map(int, b))
            color = (255, 0, 0)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            # put id track to image
            cv2.putText(image, "track", (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        1)

    return image


def test_function():
    full_bbox = [[2697, 588],
                 [2747, 588],
                 [2697, 664],
                 [2747, 3000]]
    polygon = [[0, 0],
               [1920, 0],
               [1920, 1080],
               [0, 1080]]
    full_bbox = np.array(full_bbox)
    polygon = np.array(polygon)
    inside1 = parallel_point_in_polygon(full_bbox, polygon)
    print(inside1)


if __name__ == '__main__':
    test_function()
