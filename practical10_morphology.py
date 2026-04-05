# Practical 10: Morphological Operations
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 10: Morphological Operations")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


binary = np.zeros((300, 500), dtype=np.uint8)
cv2.rectangle(binary, (30,  30),  (150, 130), 255, -1)
cv2.circle   (binary, (260, 80),  60, 255, -1)
cv2.rectangle(binary, (340, 30),  (470, 130), 255, -1)
cv2.ellipse  (binary, (120,220),  (80,45), 0, 0, 360, 255, -1)
cv2.rectangle(binary, (260,180),  (460,270), 255, -1)


noise_px = np.random.randint(0, binary.shape[0]*binary.shape[1], 1200)
for px in noise_px:
    r, c = divmod(int(px), binary.shape[1])
    if r < binary.shape[0] and c < binary.shape[1]:
        binary[r, c] = 255 if binary[r, c] == 0 else 0


k3  = np.ones((3,3), np.uint8)
k5  = np.ones((5,5), np.uint8)
k7  = np.ones((7,7), np.uint8)
k_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
k_cross   = cv2.getStructuringElement(cv2.MORPH_CROSS,   (9,9))


eroded    = cv2.erode  (binary, k3, iterations=1)
dilated   = cv2.dilate (binary, k3, iterations=1)
opened    = cv2.morphologyEx(binary, cv2.MORPH_OPEN,    k5)
closed    = cv2.morphologyEx(binary, cv2.MORPH_CLOSE,   k5)
gradient  = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT,k3)
tophat    = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT,  k7)
blackhat  = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT,k7)
erode2    = cv2.erode  (binary, k5, iterations=2)
dilate2   = cv2.dilate (binary, k5, iterations=2)

print(f"Structuring elements: 3x3 rect, 5x5 rect, 7x7 rect, 9x9 ellipse, 9x9 cross")
print(f"Erosion    (k=3x3, iter=1): shrinks white regions, removes small protrusions")
print(f"Dilation   (k=3x3, iter=1): expands white regions, fills small holes")
print(f"Opening    (k=5x5)        : erosion then dilation — removes noise")
print(f"Closing    (k=5x5)        : dilation then erosion — fills gaps")
print(f"Gradient   (k=3x3)        : dilation - erosion = outline/edge")
print(f"Top Hat    (k=7x7)        : original - opened = bright details on dark bg")
print(f"Black Hat  (k=7x7)        : closed - original = dark details on bright bg")
print(f"Erosion    (k=5x5, iter=2): heavy shrink")
print(f"Dilation   (k=5x5, iter=2): heavy expand")

def to3(im): return cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
def lbl(im, txt):
    out = to3(im).copy()
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.46,(255,255,255),1,cv2.LINE_AA)
    return out

gap=5; TH,TW=200,240
def rsz(im): return cv2.resize(to3(im),(TW,TH))
gv=np.full((TH,gap,3),160,np.uint8); gh=lambda r:np.full((gap,r.shape[1],3),160,np.uint8)

cells=[binary,eroded,dilated,opened,closed,gradient,tophat,blackhat,erode2]
labs=["Input (noisy)","Erosion k=3","Dilation k=3","Opening k=5","Closing k=5",
      "Gradient k=3","Top Hat k=7","Black Hat k=7","Erosion k=5 x2"]
padded=[lbl(rsz(c),labs[i]) for i,c in enumerate(cells)]

r1=np.hstack([padded[0],gv,padded[1],gv,padded[2]])
r2=np.hstack([padded[3],gv,padded[4],gv,padded[5]])
r3=np.hstack([padded[6],gv,padded[7],gv,padded[8]])
grid=np.vstack([r1,gh(r1),r2,gh(r2),r3])
cv2.imwrite('outputs/p10_morphology.png', grid)
print("\nSaved: outputs/p10_morphology.png")
print("[OK] Practical 10 Complete")
