import cv2
import numpy as np
import requests

response = requests.get(
    "https://s3.oryza.vn/crowd-production/1718785129.6680055.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=RET9cq9g8qTNvr3cMW1f%2F20240619%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240619T081849Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=03daec4864d62998780d2fe932b6a166511dc79d746f2458cbbbcc41f69386d2"
)
image_bytes = response.content
image_array = np.frombuffer(image_bytes, np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# show image
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
