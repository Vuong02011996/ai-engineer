import numpy as np


def linear_assignment(cost_matrix):
    try:
        import lap
        _, x, y = lap.lapjv(cost_matrix, extend_cost=True)
        return np.array([[y[i], i] for i in x if i >= 0])  #
    except ImportError:
        from scipy.optimize import linear_sum_assignment
        x, y = linear_sum_assignment(cost_matrix)
        return np.array(list(zip(x, y)))


def iou_batch(bb_test, bb_gt, tracker_origin=None):
    """
    From SORT: Computes IOU between two bboxes in the form [x1,y1,x2,y2]
    """
    bb_gt = np.expand_dims(bb_gt, 0)
    bb_test = np.expand_dims(bb_test, 1)

    xx1 = np.maximum(bb_test[..., 0], bb_gt[..., 0])
    yy1 = np.maximum(bb_test[..., 1], bb_gt[..., 1])
    xx2 = np.minimum(bb_test[..., 2], bb_gt[..., 2])
    yy2 = np.minimum(bb_test[..., 3], bb_gt[..., 3])
    # [xx1, xx2, yy1, yy2] bbox of region intersection
    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h  # Area IoU
    # Iou extend
    if tracker_origin is not None:
        bb_gt = np.expand_dims(tracker_origin, 0)
        o = wh / ((bb_test[..., 2] - bb_test[..., 0]) * (bb_test[..., 3] - bb_test[..., 1])
                  + (bb_gt[..., 2] - bb_gt[..., 0]) * (bb_gt[..., 3] - bb_gt[..., 1]) - wh)
    else:  # normal Iou
        o = wh / ((bb_test[..., 2] - bb_test[..., 0]) * (bb_test[..., 3] - bb_test[..., 1])
                  + (bb_gt[..., 2] - bb_gt[..., 0]) * (bb_gt[..., 3] - bb_gt[..., 1]) - wh)

    return (o)


def associate_detections_to_trackers(detections, trackers, time_since_update_track=None, tracker_origin=None,
                                     iou_threshold=0.3):
    """
    Assigns detections to tracked object (both represented as bounding boxes)
    Returns 3 lists of matches, unmatched_detections and unmatched_trackers
    :param detections:(M,6)[[x1, x2, y1, y2, score, label],...M]
    :param trackers:(N,6)[[x1, x2, y1, y2, score, label],...N]
    :param tracker_origin:
    :param iou_threshold:
    :return:
    """
    if len(trackers) == 0:
        return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 6), dtype=int), []

    iou_matrix = iou_batch(detections, trackers, tracker_origin)

    if min(iou_matrix.shape) > 0:
        a = (iou_matrix > iou_threshold).astype(np.int32)
        if a.sum(1).max() == 1 and a.sum(0).max() == 1:
            matched_indices = np.stack(np.where(a), axis=1)
        else:
            matched_indices = linear_assignment(-iou_matrix)
    else:
        matched_indices = np.empty(shape=(0, 2))

    unmatched_detections = []
    for d, det in enumerate(detections):
        if d not in matched_indices[:, 0]:
            unmatched_detections.append(d)
    unmatched_trackers = []
    for t, trk in enumerate(trackers):
        if t not in matched_indices[:, 1]:
            unmatched_trackers.append(t)

    # filter out matched with low IOU
    matches = []
    iou_match = []
    for m in matched_indices:
        if iou_matrix[m[0], m[1]] < iou_threshold or (
                np.sum(detections[m[0]]) == 0 and np.sum(trackers[m[1]]) == 0):  # discard match [0 0 0 0] vs [0 0 0 0]
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        else:
            """Add new idea to solve case 1
            track with time_since_update == 1 or 2
            if matched with detection have IoU small is considered again. 
            """
            if time_since_update_track is not None and (time_since_update_track[m[1]] <= 3) and (iou_matrix[m[0], m[1]] < iou_threshold + 0.15):
                unmatched_detections.append(m[0])
                unmatched_trackers.append(m[1])
            else:
                matches.append(m.reshape(1, 2))
                iou_match.append(iou_matrix[m[0], m[1]])
    if len(matches) == 0:
        matches = np.empty((0, 2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)
    return matches, np.array(unmatched_detections), np.array(unmatched_trackers), iou_match
