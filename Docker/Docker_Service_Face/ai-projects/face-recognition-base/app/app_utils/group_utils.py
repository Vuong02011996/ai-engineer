import numpy as np


def cosine_distance(a, b, data_is_normalized=False):
    if not data_is_normalized:
        a = np.asarray(a) / np.linalg.norm(a, axis=1, keepdims=True)
        b = np.asarray(b) / np.linalg.norm(b, axis=1, keepdims=True)
    return 1. - np.dot(a, b.T)


def matching_unidentified(all_features, biometric_threshold):
    group_similar = []

    for id_track in range(len(all_features)):
        features_id_track = all_features[id_track]
        all_features_compare = all_features[id_track + 1:]
        arr_similar_id_track_features = []

        for id_track_compare in range(len(all_features_compare)):
            arr_vector_compare = all_features_compare[id_track_compare]
            matrix_similar = cosine_distance(features_id_track, arr_vector_compare, data_is_normalized=True)
            arr_min_similar_features = np.min(matrix_similar, axis=0)
            arr_similar_id_track_features.append(np.mean(arr_min_similar_features))

        arr_similar_id_track_features = np.asarray(arr_similar_id_track_features)
        index_similar = np.where(arr_similar_id_track_features < biometric_threshold)[0] + id_track + 1
        index_similar = np.insert(index_similar, 0, id_track)

        if len(index_similar) > 0:
            group_similar.append(list(index_similar))

    return group_similar


def group_unidentified(group_similar):
    groups = []
    for i_group in range(len(group_similar)):
        id_track_group = group_similar[i_group]
        # check element in next group already total groups
        if len(groups) > 0:
            element_the_same_next_group = np.intersect1d(id_track_group, np.hstack(np.asarray(groups)))
            if len(element_the_same_next_group) > 0:
                continue
        group_similar_next = group_similar[i_group + 1:]
        new_groups = []
        for i_group_compare in range(len(group_similar_next)):
            id_track_group_compare = group_similar_next[i_group_compare]

            """
            Xem group hien tai voi nhung group ke tiep 
            Neu co vector giong nhau 
            thi tao new group la combine khong lap lai cua hai group.
            Neu khong co bo qua.
            """
            arr_the_same = np.intersect1d(id_track_group, id_track_group_compare)
            if len(arr_the_same) > 0:
                new_groups.append(arr_the_same)
                arr_diff = np.setdiff1d(id_track_group, id_track_group_compare)
                arr_diff_compare = np.setdiff1d(id_track_group_compare, id_track_group)
                if len(arr_diff) > 0:
                    new_groups.append(arr_diff)
                if len(arr_diff_compare) > 0:
                    new_groups.append(arr_diff_compare)
        # check id_track not group
        if len(new_groups) == 0:
            new_groups.append(id_track_group)
        new_groups = np.unique(np.hstack(np.asarray(new_groups)))
        groups.append(new_groups)
    return groups

