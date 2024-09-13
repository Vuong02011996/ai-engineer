import time
import cv2
import numpy as np
from core.main.mot_tracking import untils_track
from core.main.head_detect import class_names
from core.main.main_utils.draw import draw_boxes_tracking, draw_det_when_track, show_stream, draw_region
from core.main.mot_tracking.untils_track import select_bbox_inside_many_resions


def drawing(cam, show_queue, show_all_queue, frame_final_queue, object_dal):
    pre_track_id = []
    pre_list_name = []
    while cam.cap.isOpened():
        track_bbs_ids, matching_info, frame_count, frame_rgb, boxes_face = show_queue.get()
        image_show = frame_rgb.copy()
        image_show = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)

        list_name = list(map(lambda i: i.get('name', None), matching_info))
        start_time = time.time()
        #
        # track_ids = track_bbs_ids[:, -1]
        # for i in range(len(track_ids)):
        #     if track_ids[i] in pre_track_id:
        #         index_pre_track_id = np.where(pre_track_id == track_ids[i])[0][0]
        #         if list_name[i] == "Unknown" and pre_list_name[index_pre_track_id] != "Unknown":
        #             list_name[i] = pre_list_name[index_pre_track_id]
        #
        # pre_list_name = list_name
        # pre_track_id = track_ids

        # delete track anh list name have bbox out of region
        # track_bbs_ids, list_idx_bbox_del = untils_track.select_bbox_inside_polygon(track_bbs_ids, cam.region_track)
        '''----------------------Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''
        track_bbs_ids, list_idx_bbox_del = select_bbox_inside_many_resions(track_bbs_ids, cam.region_track)
        if len(list_idx_bbox_del) > 0:
            list_name = np.delete(list_name, np.array(list_idx_bbox_del), 0)
        '''----------------------End Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''

        if image_show is not None:
            image_show = draw_region(image_show, cam.region_track)

            if cam.show_all:
                track_bbs_ids, boxes, labels, scores, unm_trk_ext, image_rgb, frame_count = show_all_queue.get()

                list_name = list(map(lambda i: i.get('name', None), matching_info))
                # delete track anh list name have bbox out of region
                # track_bbs_ids, list_idx_bbox_del = untils_track.select_bbox_inside_polygon(track_bbs_ids, cam.region_track)
                '''----------------------Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''
                track_bbs_ids, list_idx_bbox_del = select_bbox_inside_many_resions(track_bbs_ids, cam.region_track)
                if len(list_idx_bbox_del) > 0:
                    list_name = np.delete(list_name, np.array(list_idx_bbox_del), 0)
                '''----------------------End Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''
                print("len(track_bbs_ids): ", len(track_bbs_ids))
                print("len(list_name): ", len(list_name))
                assert len(track_bbs_ids) == len(list_name)

                image_show = draw_boxes_tracking(image_show, track_bbs_ids, boxes_face, list_name,
                                                 track_bbs_ext=unm_trk_ext)
                image_show = draw_det_when_track(image_show, boxes, scores=scores, labels=labels,
                                                 class_names=class_names)
            else:
                image_show = show_stream(image_show, track_bbs_ids, list_name, frame_count, cam.total_frame_video)

        if frame_final_queue.full() is False:
            frame_final_queue.put([image_show, frame_count])
        else:
            time.sleep(0.0001)
        # print("drawing cost", time.time() - start_time)
        # print("##################################")

    cam.cap.release()


def drawing_v2(cam, show_queue, show_all_queue, frame_final_queue, object_dal):
    """
    Add:
    + track have name, no detect face: xoa track khi track da co name(khong xu li face detect)
    Args:
        cam:
        show_queue:
        show_all_queue:
        frame_final_queue:
        object_dal:

    Returns:

    """
    pre_track_id = []
    pre_list_name = []
    while cam.cap.isOpened():
        track_bbs_ids, matching_info, frame_count, frame_, boxes_face = show_queue.get()
        image_show = frame_.copy()
        image_show = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
        start_time = time.time()
        # Dùng để show name nếu track vẫn giống frame trước và Unknown
        # track_ids = track_bbs_ids[:, -1]
        # for i in range(len(track_ids)):
        #     if track_ids[i] in pre_track_id:
        #         index_pre_track_id = np.where(pre_track_id == track_ids[i])[0][0]
        #         if list_name[i] == "Unknown" and pre_list_name[index_pre_track_id] != "Unknown":
        #             list_name[i] = pre_list_name[index_pre_track_id]
        #
        # pre_list_name = list_name
        # pre_track_id = track_ids

        if image_show is not None:
            image_show = draw_region(image_show, cam.region_track)
            if cam.show_all:
                track_bbs_ids, boxes, labels, scores, unm_trk_ext, image_rgb, frame_count = show_all_queue.get()
                list_name = list(map(lambda i: i.get('name', None), matching_info))
                '''----------------------Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''
                track_bbs_ids, list_idx_bbox_del = select_bbox_inside_many_resions(track_bbs_ids, cam.region_track)
                if len(list_idx_bbox_del) > 0:
                    list_name = np.delete(list_name, np.array(list_idx_bbox_del), 0)
                '''----------------------End-------------------------'''

                '''    + track have name, no detect face: xoa track khi track da co name(khong xu li face detect)'''
                # object_data = object_dal.find_all_object_have_name_by_process_name(cam.process_name)
                # if len(object_data) > 0:
                #     list_track_id = list(map(lambda x: x["track_id"], object_data))
                #     # print('******************list_track_id********', list_track_id)
                #     track_bbs_ids = track_bbs_ids[~np.isin(track_bbs_ids[:, -1], list_track_id)]
                #     '''--------------end-------------------------------'''

                # print("len(track_bbs_ids): ", len(track_bbs_ids))
                # print("len(list_name): ", len(list_name))

                assert len(track_bbs_ids) == len(list_name)
                image_show = draw_boxes_tracking(image_show, track_bbs_ids, boxes_face, list_name,
                                                 track_bbs_ext=unm_trk_ext)
                image_show = draw_det_when_track(image_show, boxes, scores=scores, labels=labels,
                                                 class_names=class_names)
            else:
                list_name = list(map(lambda i: i.get('name', None), matching_info))
                # delete track anh list name have bbox out of region
                # track_bbs_ids, list_idx_bbox_del = untils_track.select_bbox_inside_polygon(track_bbs_ids, cam.region_track)
                '''----------------------Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''
                track_bbs_ids, list_idx_bbox_del = select_bbox_inside_many_resions(track_bbs_ids, cam.region_track)

                if len(list_idx_bbox_del) > 0:
                    list_name = np.delete(list_name, np.array(list_idx_bbox_del), 0)
                '''----------------------End Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''

                # print("track_bbs_ids: ", track_bbs_ids)
                # print("list_name: ", list_name)
                image_show = show_stream(image_show, track_bbs_ids, list_name, frame_count, cam.total_frame_video)

        if frame_final_queue.full() is False:
            frame_final_queue.put([image_show, frame_count])
        else:
            time.sleep(0.0001)
        # print("drawing cost", time.time() - start_time)
        # print("##################################")

    cam.cap.release()


def drawing_safe_region(cam, show_all_queue, frame_final_queue):
    while cam.cap.isOpened():
        track_bbs_ids, boxes, labels, scores, unm_trk_ext, image_rgb, frame_count = show_all_queue.get()
        image_show = image_rgb.copy()
        image_show = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)

        if image_show is not None:
            image_show = draw_region(image_show, cam.region_track)
            image_show = draw_det_when_track(image_show, boxes, scores=scores, labels=labels,
                                             class_names=class_names)
            image_show = draw_boxes_tracking(image_show, track_bbs_ids)
        if frame_final_queue.full() is False:
            frame_final_queue.put([image_show, frame_count])
        else:
            time.sleep(0.0001)
        # print("drawing cost", time.time() - start_time)
        # print("##################################")

    cam.cap.release()


if __name__ == '__main__':
    pass
