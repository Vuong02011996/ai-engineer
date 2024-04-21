import cv2
import numpy as np
from unidecode import unidecode


def extend_bbox(box, shape_image, ext_w=10, ext_h=10):
    h, w, _ = shape_image
    x1_ext = max(0, box[0] - ext_w)
    y1_ext = max(0, box[1] - ext_h)
    x2_ext = min(w, box[2] + ext_w)
    y2_ext = min(h, box[3] + ext_h)
    return [x1_ext, y1_ext, x2_ext, y2_ext]


def draw_boxes_tracking(image, track_bbs_ids, boxes_face=None, list_name=None, track_bbs_ext=None, line_thickness=1, font_scale=1.0,
                        font_thickness=2, color=(255, 0, 0)):

    for idx, b in enumerate(track_bbs_ids):
        xmin, ymin, xmax, ymax, track_id = list(map(int, b))
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
        # draw bbox face
        if boxes_face is not None and len(track_bbs_ids) == len(boxes_face) and np.sum(boxes_face[idx]) > 0 and list_name is not None:
            box_face = list(map(int, boxes_face[idx]))
            cv2.rectangle(image, (box_face[0], box_face[1]), (box_face[2], box_face[3]), (45, 255, 255), line_thickness)
            if list_name[idx] != "Unknown":
                name = unidecode(list_name[idx])
                cv2.putText(image, name, (xmin-10, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                            2)

        # put id track to image
        cv2.putText(image, str(track_id), (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color,
                    2)

    if track_bbs_ext is not None:
        for b in track_bbs_ext:
            xmin, ymin, xmax, ymax = list(map(int, b))
            color = (0, 0, 0)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            cv2.putText(image, "track_ext", (xmin, ymin + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        1)

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
            color = (255, 255, 255)
            label = '-'.join([class_name, score])
            cv2.rectangle(image, (xmin-3, ymin-3), (xmax+3, ymax+3), color, line_thickness)
    else:
        color = (0, 255, 0)
        for b in boxes:
            xmin, ymin, xmax, ymax = list(map(int, b))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
    return image