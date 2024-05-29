# Docs 
+ https://docs.ultralytics.com/
# Train
## Concept 
+ **box_loss**:
  + Loss liên quan đến : dự đoán vị trí và kích thước của các hộp giới hạn (bounding boxes) xung quanh các đối tượng
  + Tính bằng cách so sánh sự khác biệt giữa các tọa độ dự đoán của các hộp giới hạn và các tọa độ thật của các hộp giới hạn trong dữ liệu huấn luyện
  + Thuật toán tính loss: GIoU (Generalized Intersection over Union), DIoU (Distance Intersection over Union), hoặc CIoU (Complete Intersection over Union) 
+ **cls_loss**:
  + classification loss 
  + Loss này thường được tính bằng cách sử dụng các phương pháp như Cross-Entropy Loss hoặc Focal Loss, nhằm so sánh sự khác biệt giữa các nhãn lớp dự đoán và các nhãn lớp thật
+ **dfl_loss**:
  + (Distribution Focal Loss) đại diện cho tổn thất liên quan đến việc dự đoán các tọa độ của các hộp giới hạn theo phân phối xác suất
  +  Đây là một dạng đặc biệt của loss được sử dụng trong các mô hình tiên tiến như YOLOv8, nơi mà các tọa độ hộp giới hạn không chỉ được dự đoán trực tiếp mà còn được biểu diễn dưới dạng phân phối xác suất
+ **Instances**: 
  + thể hiện số lượng các đối tượng (instances) được phát hiện hoặc xử lý trong quá trình huấn luyện.
  + thông tin về số lượng các đối tượng có mặt trong các batch của dữ liệu huấn luyện tại mỗi bước (iteration).

## Thông số đánh giá
+ **True Positives (TP)**: 
  + True Positives là số lượng dự đoán đúng của mô hình khi mô hình dự đoán một đối tượng là thuộc về một lớp cụ thể và đối tượng đó thực sự thuộc về lớp đó
  + nếu mô hình dự đoán đúng rằng có một chiếc xe hơi trong ảnh và thực sự có một chiếc xe hơi ở vị trí đó, thì đó là một True Positive.
+ **False Positives (FP)**:
  + False Positives là số lượng dự đoán sai của mô hình khi mô hình dự đoán một đối tượng thuộc về một lớp cụ thể nhưng đối tượng đó không thuộc về lớp đó
  + nếu mô hình dự đoán rằng có một chiếc xe hơi trong ảnh nhưng thực tế không có chiếc xe hơi nào ở vị trí đó, thì đó là một False Positive.
+ **False Negatives (FN)**:
  + False Negatives là số lượng dự đoán sai của mô hình khi mô hình không phát hiện ra một đối tượng thuộc về một lớp cụ thể mặc dù đối tượng đó thực sự thuộc về lớp đó.
  + nếu có một chiếc xe hơi trong ảnh nhưng mô hình không phát hiện ra nó, thì đó là một False Negative.
+ **True Negatives (TN)**:
  + True Negatives là số lượng dự đoán đúng của mô hình khi mô hình dự đoán một đối tượng không thuộc về một lớp cụ thể và đối tượng đó thực sự không thuộc về lớp đó.
  + nếu mô hình dự đoán đúng rằng không có chiếc xe hơi nào trong một phần của ảnh và thực tế không có chiếc xe hơi nào ở phần đó, thì đó là một True Negative.

+ Những khái niệm này rất quan trọng để tính toán các chỉ số đánh giá hiệu suất của mô hình như Precision, Recall, F1-Score

+ **P (Precision)**: 
  + đo lường tỷ lệ các dự đoán đúng (true positives) trong số các dự đoán của mô hình.
  + P = TP / (TP + FP): số dự đoán đúng trên tổng số dự đoán (đúng + sai)
  + `Trong số các đối tượng mà mô hình dự đoán là đúng, bao nhiêu phần trăm thực sự đúng`
+ **R (Recall)**:
  +  đo lường tỷ lệ các đối tượng đúng được mô hình phát hiện so với tổng số các đối tượng thực sự có trong hình ảnh.
  + R = TP/(TP + FN)
  + `Trong số các đối tượng thực sự có trong hình ảnh, bao nhiêu phần trăm được mô hình phát hiện`
+ **F1 Score**
  + F1-score là một thước đo quan trọng trong lĩnh vực học máy, đặc biệt hữu ích khi làm việc với dữ liệu mất cân bằng (imbalanced data)
  + Nó là trung bình điều hòa của Precision và Recall
  + F1 = 2 x (PxR/P+R)
  + Khi nào sử dụng F1-score?
    + Dữ liệu mất cân bằng
    + Tầm quan trọng của cả Precision và Recall: Khi không thể đánh đổi giữa Precision và Recall, ví dụ như trong phát hiện bệnh, nơi cả hai loại lỗi đều quan trọng.
+ **mAP50 (Mean Average Precision at IoU=0.50)**:
  + 
# Example:
```
Model summary (fused): 168 layers, 3006038 parameters, 0 gradients, 8.1 GFLOPs
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100%|██████████| 27/27 [00:02<00:00,  9.40it/s]
                   all        833       5658      0.805      0.667      0.741      0.449
                person        833       2782      0.752      0.681       0.75      0.444
                  head        833       2876      0.858      0.653      0.732      0.454
Speed: 0.1ms preprocess, 1.3ms inference, 0.0ms loss, 0.9ms postprocess per image
Results saved to runs/detect/train
```
+ R thấp: số lượng nhận diện kém so với thực tế.
+ P trung bình : các box nhận diện được có độ chính xác chấp nhận được.

# Infer
+ Disable logging info: result = model(image_infer, verbose=False)

## inference-arguments
+ https://docs.ultralytics.com/modes/predict/#inference-arguments
+ 