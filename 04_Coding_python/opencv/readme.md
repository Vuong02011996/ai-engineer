# Some opencv function often using.

+ Ref [Motion_Detection](https://github.com/Vuong02011996/Motion_Detection)

## Change illumination image by change gama
+ Ref [change-image-illumination](https://stackoverflow.com/questions/33322488/how-to-change-image-illumination-in-opencv-python)
```python
def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)
```

## Accumulating the weighted average an image

```python
cv2.accumulateWeighted(image, self.bg, self.accumWeight)
```
## Find contours
```python
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
```
## Compute the absolute difference between two image
```python
delta = cv2.absdiff(self.bg.astype("uint8"), image)
```

## Perform a series of erosions and dilations
+ Remove noise(small blobs)
```python
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
```
