import cv2
import numpy as np
from core.main.mot_tracking.hungrary_linear_assignment import associate_detections_to_trackers, iou_batch, linear_assignment
from core.main.mot_tracking.kalman_filters import KalmanBoxTracker
from core.main.mot_tracking.untils_track import extend_bbox_track, iou, draw_track_bbs_and_det_bbs_to_image
import matplotlib.pyplot as plt
import matplotlib

#matplotlib.use('TkAgg')


class Sort(object):
    def __init__(self, class_names=None, max_age=15, min_hits=3, iou_threshold=0.3):
        """
        Sets key parameters for SORT
        """
        # num frame wait for 1 track no detection, kalman filter vẫn predict , history append new , càng lâu thì khả
        # năng dự đoán của KF càng sai số (do không có measurement),
        # dẫn đến associate giữa track với dets không còn đúng
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.trackers = []
        self.frame_count = 0
        self.class_names = class_names

    def update(self, dets=np.empty((0, 6)), image=None):
        """
        Params:
          dets - a numpy array of detections in the format [[x1,y1,x2,y2,score, label],[x1,y1,x2,y2,score, label],...]
        Requires: this method must be called once for each frame even with empty detections (use np.empty((0, 5)) for frames without detections).
        Returns: the a similar array, where the last column is the object ID.
        [[x1,y1,x2,y2,id1, label],[x1,y1,x2,y2,id2, label],...]

        NOTE: The number of objects returned may differ from the number of detections provided.
        """
        self.frame_count += 1
        if self.frame_count == 1627:
            a = 0
        # get predicted locations from existing trackers
        # print('len(self.trackers)', len(self.trackers))
        trks = np.zeros((len(self.trackers), 6))
        to_del = []
        ret = []
        time_since_update_track = []
        for t, trk in enumerate(trks):
            pos = self.trackers[t].predict()[0]
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0, 0]
            time_since_update_track.append(self.trackers[t].time_since_update)
            if np.any(np.isnan(pos)):
                to_del.append(t)
        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))
        for t in reversed(to_del):
            self.trackers.pop(t)
            time_since_update_track.pop(t)
        matched, unmatched_dets, unmatched_trks, iou_match = associate_detections_to_trackers(detections=dets, trackers=trks,
                                                                                   time_since_update_track=time_since_update_track,
                                                                                   iou_threshold=self.iou_threshold)
        # test
        # for i, m in enumerate(matched):
        #     print("track_id:{}, state: {}, matched:{}, iou_match: {}".format(self.trackers[m[1]].track_id + 1, self.trackers[m[1]].state,
        #                                                                       matched[i], iou_match[i]))

        """
        Add more idea from paper libs_sort_oh/2103.04147.pdf
        + Add state occluded for unmatched_trks
        + Extend bounding box  unmatched_trks
        + Reid track occluded with unmatched_dets
        + Delete unmatched_dets match with extend.
        """
        unm_trk_ext = np.zeros((len(trks), 4))
        unm_trk_list = np.zeros((len(trks), 4))
        flag_unm_trk_ext = False
        for ut in unmatched_trks:
            unm_trk = self.trackers[ut]
            # convert to occluded if track no update 3 frame and extend its bounding box follow time_since_update
            #  unm_trk.time_since_update > 3 maybe
            if unm_trk.time_since_update > 3:
                if unm_trk.is_confirmed():
                    unm_trk.convert_state(state="occluded")
                bbox_trk = unm_trk.get_curr_bbox_estimate()[0]
                unm_trk_list[ut] = bbox_trk
                bbox_trk_ext = extend_bbox_track(bbox_trk, unm_trk.time_since_update, w_ext=0.1, h_ext=0.1)
                unm_trk_ext[ut] = np.array(bbox_trk_ext)
                flag_unm_trk_ext = True
                # image = draw_track_bbs_and_det_bbs_to_image(image, track_bbs_ext=unm_trk_ext, unm_trk_list=unm_trk_list)
                # cv2.imwrite("test_track_ext.png", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                # a = 0
        if len(unmatched_dets) > 0 and flag_unm_trk_ext:
            unm_det_ext = np.zeros((len(dets), 4))
            for ud in unmatched_dets:
                unm_det_ext[ud] = dets[ud, :4]
            unm_trk_ext = np.array(unm_trk_ext)
            unm_det_ext = np.array(unm_det_ext)
            matched_ext, unmatched_det_ext, unmatched_trk_ext, iou_match_ext = associate_detections_to_trackers(detections=unm_det_ext,
                                                                                                 trackers=unm_trk_ext,
                                                                                                 tracker_origin=unm_trk_list,
                                                                                                 iou_threshold=self.iou_threshold)
            # test
            # for i, m_ext in enumerate(matched_ext):
            #     print("track_id_ext:{}, state: {}, matched_ext:{}, iou_match_ext: {}".format(self.trackers[m_ext[1]].track_id + 1, self.trackers[m_ext[1]].state,
            #                                                                       matched_ext[i], iou_match_ext[i]))

            if len(matched_ext) > 0:
                matched = np.concatenate((matched, matched_ext), axis=0)
                for m_ext in matched_ext:
                    unmatched_dets = np.delete(unmatched_dets, np.where(unmatched_dets == m_ext[0])[0])

            # print(trks[i])

        # update matched trackers with assigned detections
        for m in matched:
            self.trackers[m[1]].update(dets[m[0], :])

        # create and initialise new trackers for unmatched detections
        #
        for i in unmatched_dets:
            trk = KalmanBoxTracker(dets[i, :], self.min_hits, self.max_age)
            self.trackers.append(trk)
        i = len(self.trackers)
        for trk in reversed(self.trackers):
            bbox = trk.get_curr_bbox_estimate()[0]
            # if trk.time_since_update < 1: # and (trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
            if trk.is_confirmed() or trk.is_occluded():
                ret.append(np.concatenate((bbox, [trk.track_id + 1])).reshape(1,
                                                                              -1))  # +1 as MOT benchmark requires positive
            i -= 1
            # remove dead tracklet
            # if trk.time_since_update > self.max_age:
            if trk.is_deleted():
                self.trackers.pop(i)
            if trk.is_finished():
                # print("Bien bao: ", self.class_names[trk.class_id])
                # maybe not delete trk not confirmed
                self.trackers.pop(i)

        if len(ret) > 0:
            return np.concatenate(ret), unm_trk_ext
        return np.empty((0, 6)), unm_trk_ext
