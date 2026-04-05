# Practical 8: Contour Detection and Analysis
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 8: Contour Detection & Analysis")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


shapes = np.ones((400, 600, 3), dtype=np.uint8) * 255
cv2.rectangle(shapes, (30,  30),  (160, 130), (0,0,0),   -1)
cv2.circle   (shapes, (280, 80),  65,         (0,0,0),   -1)
cv2.ellipse  (shapes, (450, 80),  (90,50), 0, 0, 360, (0,0,0), -1)
tri = np.array([[60,220],[160,340],[30,340]], np.int32)
cv2.fillPoly (shapes, [tri],                              (0,0,0))
pent= np.array([[310,160],[390,210],[370,310],[250,310],[230,210]], np.int32)
cv2.fillPoly (shapes, [pent],                             (0,0,0))
cv2.rectangle(shapes, (450,180), (570,340), (0,0,0),     -1)
cv2.imwrite('outputs/p8_shapes.png', shapes)


img  = cv2.imread('outputs/base_image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


gray_shapes = cv2.cvtColor(shapes, cv2.COLOR_BGR2GRAY)
_, thresh   = cv2.threshold(gray_shapes, 127, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Total contours found     : {len(contours)}")

drawn_all    = shapes.copy()
drawn_approx = shapes.copy()
drawn_bbox   = shapes.copy()
drawn_info   = shapes.copy()

colors = [(255,0,0),(0,180,0),(0,0,255),(180,100,0),(0,180,180),(160,0,160)]

for i, cnt in enumerate(contours):
    col = colors[i % len(colors)]
    # Draw contour
    cv2.drawContours(drawn_all, [cnt], -1, col, 3)


    x, y, cw, ch = cv2.boundingRect(cnt)
    cv2.rectangle(drawn_bbox, (x,y), (x+cw, y+ch), col, 2)


    eps  = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, eps, True)
    cv2.drawContours(drawn_approx, [approx], -1, col, 3)


    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    M    = cv2.moments(cnt)
    if M['m00']:
        cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    else:
        cx, cy = x, y
    print(f"  Shape {i+1}: vertices={len(approx)}  area={area:.0f}  perimeter={peri:.1f}  centroid=({cx},{cy})")
    cv2.circle(drawn_info, (cx, cy), 5, col, -1)
    cv2.drawContours(drawn_info, [cnt], -1, col, 2)
    cv2.putText(drawn_info, f"S{i+1}", (cx-8, cy-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1)


canny = cv2.Canny(cv2.GaussianBlur(gray,(5,5),0), 50, 150)
contours2, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
hull_img = img.copy()
for cnt in contours2:
    if cv2.contourArea(cnt) > 200:
        hull = cv2.convexHull(cnt)
        cv2.drawContours(hull_img, [hull], -1, (0,255,100), 2)
print(f"\nConvex hulls on scene    : {sum(1 for c in contours2 if cv2.contourArea(c)>200)} shapes")

def lbl(im, txt):
    out = im.copy()
    cv2.rectangle(out, (0, out.shape[0]-26), (out.shape[1], out.shape[0]), (20,20,20), -1)
    cv2.putText(out, txt, (5, out.shape[0]-7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255,255,255), 1, cv2.LINE_AA)
    return out

def rsz(im, h=300):
    r = h / im.shape[0]
    return cv2.resize(im, (int(im.shape[1]*r), h))

gap = 6
gv = np.full((300, gap, 3), 180, np.uint8)

r1 = np.hstack([lbl(rsz(shapes),  "Input Shapes"),  gv,
                lbl(rsz(drawn_all),"All Contours"),  gv,
                lbl(rsz(drawn_approx),"Approx Poly")])
r2 = np.hstack([lbl(rsz(drawn_bbox),"Bounding Rect"),gv,
                lbl(rsz(drawn_info),"Centroids + Labels"),gv,
                lbl(rsz(hull_img),"Convex Hulls (scene)")])
gh = lambda r: np.full((gap, r.shape[1], 3), 180, np.uint8)
grid = np.vstack([r1, gh(r1), r2])
cv2.imwrite('outputs/p8_contours.png', grid)
print("Saved: outputs/p8_contours.png")
print("[OK] Practical 8 Complete")
