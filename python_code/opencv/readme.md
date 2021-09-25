# Some opencv function often using.

+ Ref [Motion_Detection](https://github.com/Vuong02011996/Motion_Detection)
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
