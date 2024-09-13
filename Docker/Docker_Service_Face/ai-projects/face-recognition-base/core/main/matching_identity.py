import time
from app.mongo_dal.identity_dal import IdentityDAL
from app.milvus_dal.clover_dal import MilvusCloverDAL


identity_dal = IdentityDAL()
milvus_staging_dal = MilvusCloverDAL()


def matching_identity(cam, matching_queue, database_queue, show_queue):
    while cam.cap.isOpened():
        face_embeddings, track_bbs_ids, frame_count, frame_, boxes_face, landmarks_face = matching_queue.get()
        frame_rgb = frame_.copy()
        matching_info = [{
                        "name": "Unknown",
                        "url_match": None,
                        "identity_id": None,
                        "distance": None
                    }] * len(track_bbs_ids)

        start_time = time.time()
        if len(face_embeddings) > 0:
            match_identity = milvus_staging_dal.search_vector(face_embeddings.tolist())
            for idx in range(len(match_identity)):
                if match_identity[idx]["distance"] < 0.6:  # 0.45
                    print("distance: < 0.6", match_identity[idx]["distance"])
                    name, url_match, identity_id = identity_dal.find_identity_info_with_face_id(match_identity[idx]["id"])
                    if identity_id is not None:
                        print("####################name, distance################: ",name, match_identity[idx]["distance"])
                        identity_info = {
                            "name": name,
                            "url_match": url_match,
                            "identity_id": identity_id,
                            "distance": match_identity[idx]["distance"]
                        }
                        matching_info[idx] = identity_info
                        
        # print("matching cost", time.time() - start_time)
        assert len(matching_info) == len(track_bbs_ids) == len(boxes_face)
        database_queue.put([track_bbs_ids, matching_info, frame_count, frame_rgb, boxes_face, landmarks_face])
        show_queue.put([track_bbs_ids, matching_info, frame_count, frame_rgb, boxes_face])
        # show_queue.put([frame_rgb, frame_count])

    cam.cap.release()


def matching_identity_video_offline(cam, matching_queue, database_queue, show_queue, milvus_dal, face_search_dal):
    while cam.cap.isOpened():
        face_embeddings, track_bbs_ids, frame_count, frame_, boxes_face, landmarks_face = matching_queue.get()
        frame_rgb = frame_.copy()
        matching_info = [{
            "name": "Unknown",
            "url_match": None,
            "identity_id": None,
            "distance": None
        }] * len(track_bbs_ids)

        start_time = time.time()
        if len(face_embeddings) > 0:
            match_identity = milvus_dal.search_vector(face_embeddings.tolist())
            for idx in range(len(match_identity)):
                if match_identity[idx]["distance"] < 0.6:  # 0.45
                    print("distance: < 0.6", match_identity[idx]["distance"])
                    name, url_match, identity_id = face_search_dal.find_identity_info_with_face_id(
                        match_identity[idx]["id"])
                    if identity_id is not None:
                        print("####################name, distance################: ", name,
                              match_identity[idx]["distance"])
                        identity_info = {
                            "name": name,
                            "url_match": url_match,
                            "identity_id": identity_id,
                            "distance": match_identity[idx]["distance"]
                        }
                        matching_info[idx] = identity_info

        # print("matching cost", time.time() - start_time)
        assert len(matching_info) == len(track_bbs_ids) == len(boxes_face)
        database_queue.put([track_bbs_ids, matching_info, frame_count, frame_rgb, boxes_face, landmarks_face])
        show_queue.put([track_bbs_ids, matching_info, frame_count, frame_rgb, boxes_face])
        # show_queue.put([frame_rgb, frame_count])

    cam.cap.release()
