# Keni algoritam za detekciju ivica

## Ideja

Želimo da implementiramo OpenCV implementaciju:

```
edges = cv2.Canny(blurred, 100, 200)
```

TODO objašnjenje, kroz ove izvore što sam video

Za double threshold:
After application of non-maximum suppression, the remaining edge pixels provide a more accurate representation of real edges in an image. However, some edge pixels remain that are caused by noise and color variation. To account for these spurious responses, it is essential to filter out edge pixels with a weak gradient value and preserve edge pixels with a high gradient value

## Izvori

- Edge Detection Using Gradients | Edge Detection, First Principles of Computer Vision YouTube snimak: https://www.youtube.com/watch?v=lOEBsQodtEQ
- Sobel operator, Wikipedia članak: https://en.wikipedia.org/wiki/Sobel_operator
- Canny Edge Detector | Edge Detection, First Principles of Computer Vision YouTube snimak: https://www.youtube.com/watch?v=hUC1uoigH6s
- Canny Edge Detector, Wikipedia članak: https://en.wikipedia.org/wiki/Canny_edge_detector
  - Dobar izvor za korake koje treba sprovesti
- RO-1.0X104: Non-Maximal Suppression in Canny Edge Detection Algorithm, Deep Eigen, YouTube snimak: https://www.youtube.com/watch?v=9cpTmJCsI0M