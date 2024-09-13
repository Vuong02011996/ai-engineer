import numpy as np
import time
from core.main.head_detect import class_names
from core.main.mot_tracking.mot_sort_tracker import Sort
from core.main.mot_tracking import untils_track
from core.main.mot_tracking.untils_track import select_bbox_inside_many_resions

mot_tracker = Sort(class_names)


def tracking(cam, detections_queue, show_all_queue, head_bbox_queue):
    """
    :param cam:
    :param head_bbox_queue:
    :param detections_queue:
    :param show_all_queue:
    :return:
    Tracking using SORT. Hungary + Kalman Filter.
    Using mot_tracker.update()
    Input: detections [[x1,y1,x2,y2,score,label],[x1,y1,x2,y2,score, label],...], use np.empty((0, 5)) for frames without detections
    Output: [[x1,y1,x2,y2,id1, label],[x1,y1,x2,y2,id2, label],...]
    """

    while cam.cap.isOpened():

        boxes, labels, scores, frame_, detections_sort, frame_count = detections_queue.get()
        frame_rgb = frame_.copy()

        start_time = time.time()
        if len(boxes) == 0:
            detections = np.empty((0, 6))
        else:
            detections = detections_sort
            # check and select the detection is inside region tracking
            detections, list_idx_bbox_del = select_bbox_inside_many_resions(detections, cam.region_track)

        track_bbs_ids, unm_trk_ext = mot_tracker.update(detections, image=frame_rgb)

        # print("unm_trk_ext: ", unm_trk_ext)
        # print("tracking cost: ", time.time() - start_time)
        if cam.frame_step_after_track != 0 and frame_count % cam.frame_step_after_track != 0:
            continue

        cam.frame_step_after_track += 2

        head_bbox_queue.put([track_bbs_ids, frame_rgb, frame_count, boxes, scores])
        # Data for visualize
        if cam.show_all:
            show_all_queue.put([track_bbs_ids, boxes, labels, scores, unm_trk_ext, frame_rgb, frame_count])

    cam.cap.release()


def tracking_safe_region(cam, detections_queue, show_all_queue, database_queue):
    """
    :param cam:
    :param database_queue:
    :param detections_queue:
    :param show_all_queue:
    :return:
    Tracking using SORT. Hungary + Kalman Filter.
    Using mot_tracker.update()
    Input: detections [[x1,y1,x2,y2,score,label],[x1,y1,x2,y2,score, label],...], use np.empty((0, 5)) for frames without detections
    Output: [[x1,y1,x2,y2,id1, label],[x1,y1,x2,y2,id2, label],...]
    """
    while cam.cap.isOpened():

        boxes, labels, scores, frame_rgb, detections_sort, frame_count = detections_queue.get()

        start_time = time.time()
        if len(boxes) == 0:
            detections = np.empty((0, 6))
        else:
            detections = detections_sort
            # check and select the detection is inside region tracking
            detections, list_idx_bbox_del = select_bbox_inside_many_resions(detections, cam.region_track)

        track_bbs_ids, unm_trk_ext = mot_tracker.update(detections, image=frame_rgb)

        # print("tracking cost: ", time.time() - start_time)
        if cam.frame_step_after_track != 0 and frame_count % cam.frame_step_after_track != 0:
            continue

        cam.frame_step_after_track += 2

        database_queue.put([track_bbs_ids, frame_rgb, frame_count])
        # Data for visualize
        if cam.show_all:
            show_all_queue.put([track_bbs_ids, boxes, labels, scores, unm_trk_ext, frame_rgb, frame_count])


    cam.cap.release()


if __name__ == '__main__':
    pass