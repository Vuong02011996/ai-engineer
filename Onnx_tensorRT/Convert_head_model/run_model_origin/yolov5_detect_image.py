import sys
import torch
import numpy as np
from Onnx_tensorRT.Convert_head_model.run_model_origin.models.experimental import attempt_load
from Onnx_tensorRT.Convert_head_model.run_model_origin.utils.general import check_img_size, non_max_suppression, scale_coords
from Onnx_tensorRT.Convert_head_model.run_model_origin.utils.datasets import letterbox
import cv2
from glob import glob


class Y5Detect:
    def __init__(self, weights):
        """
        :param weights: 'yolov5s.pt'
        """
        self.weights = weights
        self.model_image_size = 640
        self.conf_threshold = 0.3
        self.iou_threshold = 0.45
        self.model, self.device = self.load_model(use_cuda=True)
        # self.model, self.device = self.load_model(use_cuda=False)

        stride = int(self.model.stride.max())  # model stride
        self.image_size = check_img_size(self.model_image_size, s=stride)
        self.class_names = self.model.module.names if hasattr(self.model, 'module') else self.model.names

    def load_model(self, use_cuda=False):
        if use_cuda is None:
            use_cuda = torch.cuda.is_available()
        device = torch.device('cuda:0' if use_cuda else 'cpu')

        model = attempt_load(self.weights, map_location=device)
        return model, device

    def preprocess_image(self, image_rgb):
        # Padded resize
        img = letterbox(image_rgb.copy(), new_shape=self.image_size)[0]

        # Convert
        img = img.transpose(2, 0, 1)  # to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        return img

    def predict(self, image_rgb, label_select=list, show=False):
        image_rgb_shape = image_rgb.shape
        img = self.preprocess_image(image_rgb)
        pred = self.model(img)[0]
        # Apply NMS
        pred = non_max_suppression(pred,
                                   self.conf_threshold,
                                   self.iou_threshold,)
        bboxes = []
        labels = []
        scores = []
        for i, det in enumerate(pred):  # detections per image
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image_rgb_shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    with torch.no_grad():
                        x1 = xyxy[0].cpu().data.numpy()
                        y1 = xyxy[1].cpu().data.numpy()
                        x2 = xyxy[2].cpu().data.numpy()
                        y2 = xyxy[3].cpu().data.numpy()
                        #                        print('[INFO] bbox: ', x1, y1, x2, y2)
                        # bboxes.append(list(map(int, [x1, y1, x2, y2])))
                        label = self.class_names[int(cls)]
                        # #                        print('[INFO] label: ', label)
                        # labels.append(label)
                        # score = conf.cpu().data.numpy()
                        # #                        print('[INFO] score: ', score)
                        # scores.append(float(score))

                        if label in label_select:
                            bboxes.append(list(map(int, [x1, y1, x2, y2])))
                            labels.append(label)
                            score = conf.cpu().data.numpy()
                            scores.append(float(score))
                            # preds.append(np.array([int(x1), int(y1), int(x2), int(y2), float(score), int(cls)]))
        if show:
            if bboxes is not None:
                image_show = draw_boxes(image_bgr, bboxes, scores=scores, labels=labels, class_names=self.class_names)
                cv2.namedWindow('detections', cv2.WINDOW_NORMAL)
                cv2.imshow('detections', image_show)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        return bboxes, labels, scores

    def predict_sort(self, image_rgb, label_select=list):
        image_rgb_shape = image_rgb.shape
        img = self.preprocess_image(image_rgb)
        pred = self.model(img)[0]
        # Apply NMS
        pred = non_max_suppression(pred,
                                   self.conf_threshold,
                                   self.iou_threshold,)
        bboxes = []
        labels = []
        scores = []
        preds = []
        for i, det in enumerate(pred):  # detections per image
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image_rgb_shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    with torch.no_grad():
                        x1 = xyxy[0].cpu().data.numpy()
                        y1 = xyxy[1].cpu().data.numpy()
                        x2 = xyxy[2].cpu().data.numpy()
                        y2 = xyxy[3].cpu().data.numpy()
                        label = self.class_names[int(cls)]
                        if label in label_select:
                            bboxes.append(list(map(int, [x1, y1, x2, y2])))
                            labels.append(label)
                            score = conf.cpu().data.numpy()
                            scores.append(float(score))
                            preds.append(np.array([int(x1), int(y1), int(x2), int(y2), float(score), int(cls)]))

        return bboxes, labels, scores, np.array(preds)


def draw_boxes(image, boxes, scores=None, labels=None, class_names=None, line_thickness=2, font_scale=1.0,
               font_thickness=2):
    num_classes = len(class_names)
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
            color = (45, 255, 255)
            label = '-'.join([class_name, score])

            ret, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, line_thickness)
            cv2.rectangle(image, (xmin, ymax - ret[1] - baseline), (xmin + ret[0], ymax), color, -1)
            cv2.putText(image, label, (xmin, ymax - baseline), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0),
                        font_thickness)
    else:
        color = (0, 255, 0)
        for b in boxes:
            xmin, ymin, xmax, ymax = list(map(int, b))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 1)
    return image


if __name__ == '__main__':
    y5_model = Y5Detect(weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt")

    img_path = "/home/oryza/Pictures/image_test/"

    list_image_test = glob(img_path + "*.*")
    for image_test in list_image_test:
        image_bgr = cv2.imread(image_test)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        y5_model.predict(image_rgb, label_select=["head"], show=True)