import cv2
import numpy as np
from unidecode import unidecode
import time


def draw_box_and_landmark(image, boxes, landmark=None):
    color = (0, 255, 0)
    color_landmark = (0, 0, 255)
    for i, b in enumerate(boxes):
        xmin, ymin, xmax, ymax = list(map(int, b[:4]))
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color)
        if landmark is not None:
            for point in landmark[i]:
                x_point, y_point = list(map(int, point))
                cv2.circle(image, (x_point, y_point), 1, color_landmark)

    return image


def draw_box_and_landmark_one_box(image, boxes, landmark=None):
    color = (0, 255, 0)
    color_landmark = (0, 0, 255)

    cv2.rectangle(image, (boxes[0], boxes[1]), (boxes[2], boxes[3]), color)
    if landmark is not None:
        for point in landmark:
            x_point, y_point = list(map(int, point))
            cv2.circle(image, (x_point, y_point), 1, color_landmark)

    return image


def draw_region(image, region):
    """
    region must int number
    :param image:
    :param region: np.array([[0, 0],
        #                               [2560, 0],
        #                               [2560, 1440],
        #                               [0, 1440]])
    :return:
    """
    regions = np.array(region).astype(int)
    # Nếu trường hợp tọa độ là mảng 3 chiều(nhiều vùng) ta phải vẽ từng vùng.
    if regions.ndim == 3:
        for region_item in regions:
            region = np.vstack([region_item, region_item[0]])
            cv2.polylines(image, [region], isClosed=False, color=(0, 0, 255), thickness=2)

    else:
        region = np.vstack([region, region[0]])
        cv2.polylines(image, [region], isClosed=False, color=(0, 0, 255), thickness=2)

    return image


def draw_det_when_track(image, boxes, scores=None, labels=None, class_names=None, line_thickness=2, font_scale=1.0,
               font_thickness=2):
    if scores is not None and labels is not None:
        for b, l, s in zip(boxes, labels, scores):
            if class_names is None:
                class_name = 'person'
                class_id = 0
            elif l not in class_names:
                class_id = int(l)
                class_name = class_names[class_id]
            else:
                class_name = l
                class_id = class_names.index(l)

            xmin, ymin, xmax, ymax = list(map(int, b))
            score = '{:.4f}'.format(s)
            color = (255, 255, 255) # white - box head
            label = '-'.join([class_name, score])
            cv2.rectangle(image, (xmin-3, ymin-3), (xmax+3, ymax+3), color, line_thickness)
    else:
        color = (255, 255, 255) # white - box head
        for b in boxes:
            xmin, ymin, xmax, ymax = list(map(int, b))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
    return image


def draw_boxes_tracking(image, track_bbs_ids, boxes_face=None, list_name=None, track_bbs_ext=None, line_thickness=1, font_scale=1.0,
                        font_thickness=2, color=(255, 0, 0)):
    # cv2.rectangle - For BGR, we pass a tuple. eg: (255, 0, 0) for blue color.
    for idx, b in enumerate(track_bbs_ids):
        xmin, ymin, xmax, ymax, track_id = list(map(int, b))
        color = (255, 0, 0)  # xanh duong dam - box tracking
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
        # draw bbox face
        if boxes_face is not None and len(track_bbs_ids) == len(boxes_face) and np.sum(boxes_face[idx]) > 0 and list_name is not None:
            box_face = list(map(int, boxes_face[idx]))
            # (45, 255, 255) - vang - box face
            cv2.rectangle(image, (box_face[0], box_face[1]), (box_face[2], box_face[3]), (45, 255, 255), line_thickness)
            if list_name[idx] != "Unknown":
                name = unidecode(list_name[idx])
                # (0, 0, 255) - red - ten
                cv2.putText(image, name, (xmin-10, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                            2)

        # put id track to image
        color = (255, 0, 0)  # xanh duong dam - id track
        cv2.putText(image, str(track_id), (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color,
                    2)

    if track_bbs_ext is not None:
        for b in track_bbs_ext:
            xmin, ymin, xmax, ymax = list(map(int, b))
            color = (0, 0, 0)  # den - box track extend khi mat detect
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            cv2.putText(image, "track_ext", (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        1)

    return image


def draw_boxes_one_track_id(image, track_bbs_ids, track_id,  line_thickness=1, font_scale=1.0,
                        font_thickness=2, color=(255, 0, 0)):
    current_track_id = track_bbs_ids[:, -1]
    for idx, b in enumerate(track_bbs_ids):
        if current_track_id[idx] == track_id:
            xmin, ymin, xmax, ymax, track_id = list(map(int, b))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            # draw bbox face
            # put id track to image
            cv2.putText(image, str(track_id), (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color,
                        2)

    return image


def show_stream(image_show, track_bbs_ids, list_name, frame_count, total_frame):
    # print("list_name", list_name)
    # print("track_bbs_ids", track_bbs_ids)
    for idx, b in enumerate(track_bbs_ids):
        xmin, ymin, xmax, ymax, track_id = list(map(int, b))
        color = (0, 0, 255)

        #  Show bounding box and track id
        cv2.rectangle(image_show, (xmin, ymin), (xmax, ymax), color, thickness=1)
        # put id track to image
        cv2.putText(image_show, str(track_id), (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                    2)
        if list_name[idx] != "Unknown":
            name = unidecode(list_name[idx])
            cv2.putText(image_show, name, (xmin - 10, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

    # Show frame/total frame
    # cv2.putText(image_show, "{}/{}".format(frame_count, total_frame ), (0, 0 + 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
    #             5)

    return image_show


def draw_single_pose(frame, pts, joint_format='coco'):
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    CYAN = (255, 255, 0)
    YELLOW = (0, 255, 255)
    ORANGE = (0, 165, 255)
    PURPLE = (255, 0, 255)

    """COCO_PAIR = [(0, 1), (0, 2), (1, 3), (2, 4),  # Head
                 (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
                 (17, 11), (17, 12),  # Body
                 (11, 13), (12, 14), (13, 15), (14, 16)]"""
    COCO_PAIR = [(0, 13), (1, 2), (1, 3), (3, 5), (2, 4), (4, 6), (13, 7), (13, 8),  # Body
                 (7, 9), (8, 10), (9, 11), (10, 12)]
    POINT_COLORS = [(0, 255, 255), (0, 191, 255), (0, 255, 102), (0, 77, 255), (0, 255, 0),
                    # Nose, LEye, REye, LEar, REar
                    (77, 255, 255), (77, 255, 204), (77, 204, 255), (191, 255, 77), (77, 191, 255), (191, 255, 77),
                    # LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
                    (204, 77, 255), (77, 255, 204), (191, 77, 255), (77, 255, 191), (127, 77, 255), (77, 255, 127),
                    (0, 255, 255)]  # LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
    LINE_COLORS = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), (77, 255, 222),
                   (77, 196, 255), (77, 135, 255), (191, 255, 77), (77, 255, 77), (77, 222, 255),
                   (255, 156, 127), (0, 127, 255), (255, 127, 77), (0, 77, 255), (255, 77, 36)]

    MPII_PAIR = [(8, 9), (11, 12), (11, 10), (2, 1), (1, 0), (13, 14), (14, 15), (3, 4), (4, 5),
                 (8, 7), (7, 6), (6, 2), (6, 3), (8, 12), (8, 13)]

    if joint_format == 'coco':
        l_pair = COCO_PAIR
        p_color = POINT_COLORS
        line_color = LINE_COLORS
    elif joint_format == 'mpii':
        l_pair = MPII_PAIR
        p_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, PURPLE, RED, RED,BLUE,BLUE]
    else:
        NotImplementedError

    part_line = {}
    pts = np.concatenate((pts, np.expand_dims((pts[1, :] + pts[2, :]) / 2, 0)), axis=0)
    for n in range(pts.shape[0]):
        if pts[n, 2] <= 0.05:
            continue
        cor_x, cor_y = int(pts[n, 0]), int(pts[n, 1])
        part_line[n] = (cor_x, cor_y)
        cv2.circle(frame, (cor_x, cor_y), 3, p_color[n], -1)

    for i, (start_p, end_p) in enumerate(l_pair):
        if start_p in part_line and end_p in part_line:
            start_xy = part_line[start_p]
            end_xy = part_line[end_p]
            cv2.line(frame, start_xy, end_xy, line_color[i], int(1*(pts[start_p, 2] + pts[end_p, 2]) + 1))
    return frame


def draw_data_action(image, track_bbs_ids, track_bbs_ext=None, data_action=None, line_thickness=1):
    for idx, b in enumerate(track_bbs_ids):
        xmin, ymin, xmax, ymax, track_id = list(map(int, b))
        color = (0, 0, 255)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
        # put id track to image
        cv2.putText(image, str(track_id), (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255),
                    3)
        if len(track_bbs_ids) == len(data_action):
            if data_action is not None and "action_name" in data_action[idx]:
                cv2.putText(image, data_action[idx]["action_name"], (xmin, ymin + 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255),
                            2)
                # if data_action[idx]["action_name"] == "Fall Down":
                #     cv2.putText(image, unidecode("Té Ngã"), (xmin, ymin + 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255),
                #                 2)
                # if data_action[idx]["action_name"] == "Lying Down":
                #     cv2.putText(image, unidecode("Nằm"), (xmin, ymin + 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255),
                #                 2)
                # if data_action[idx]["action_name"] == "Walking" or data_action[idx]["action_name"] == "Standing":
                #     cv2.putText(image, unidecode("Đứng or Đi"), (xmin, ymin + 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255),
                #                 2)
    if track_bbs_ext is not None:
        for b in track_bbs_ext:
            xmin, ymin, xmax, ymax = list(map(int, b))
            color = (0, 0, 0)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            cv2.putText(image, "track_ext", (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        1)

    return image



