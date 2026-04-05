# Practical 11: Image Arithmetic & Bitwise Operations
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 11: Arithmetic & Bitwise Operations")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

img = cv2.imread('outputs/base_image.png')
h, w = img.shape[:2]


brighter = cv2.add(img, np.full_like(img, 60))
darker   = cv2.subtract(img, np.full_like(img, 60))
higher_c = cv2.convertScaleAbs(img, alpha=1.5, beta=0)   # contrast x1.5
lower_c  = cv2.convertScaleAbs(img, alpha=0.5, beta=50)  # contrast x0.5

print("Brightness  +60 : cv2.add(img, scalar)")
print("Brightness  -60 : cv2.subtract(img, scalar)")
print("Contrast  x1.5  : convertScaleAbs alpha=1.5 beta=0")
print("Contrast  x0.5  : convertScaleAbs alpha=0.5 beta=50")


img2 = np.zeros_like(img)
cv2.rectangle(img2, (0,0), (w,h), (30,30,30), -1)
for i in range(5):
    cv2.circle(img2, (80+i*110, h//2), 80, (
        int(40+i*40), int(200-i*30), int(80+i*35)), -1)
blended = cv2.addWeighted(img, 0.6, img2, 0.4, 0)
print("Blend 60/40     : addWeighted(img,0.6, img2,0.4, 0)")


shape1 = np.zeros((300,300), dtype=np.uint8)
shape2 = np.zeros((300,300), dtype=np.uint8)
cv2.rectangle(shape1, (30,80),  (200,220), 255, -1)
cv2.circle   (shape2, (180,150), 100,      255, -1)

bit_and  = cv2.bitwise_and(shape1, shape2)
bit_or   = cv2.bitwise_or (shape1, shape2)
bit_xor  = cv2.bitwise_xor(shape1, shape2)
bit_not1 = cv2.bitwise_not(shape1)
bit_not2 = cv2.bitwise_not(shape2)

print("\nBitwise AND  : intersection of two shapes")
print("Bitwise OR   : union of two shapes")
print("Bitwise XOR  : non-overlapping regions only")
print("Bitwise NOT  : invert (flip black/white)")


mask = np.zeros((h,w), dtype=np.uint8)
cv2.circle(mask, (w//2, h//2), min(h,w)//3, 255, -1)
masked_img = cv2.bitwise_and(img, img, mask=mask)
print("Mask (circle): bitwise_and with circular mask")


def lbl(im, txt):
    out = im.copy() if len(im.shape)==3 else cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.46,(255,255,255),1,cv2.LINE_AA)
    return out

def rsz(im,tw,th):
    src = im if len(im.shape)==3 else cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
    return cv2.resize(src,(tw,th))

gap=5; gv3=lambda h: np.full((h,gap,3),160,np.uint8); gh3=lambda r:np.full((gap,r.shape[1],3),160,np.uint8)
TH,TW=200,250
p=[lbl(rsz(x,TW,TH),t) for x,t in [(img,"Original"),(brighter,"Brighter +60"),
    (darker,"Darker -60"),(higher_c,"Contrast x1.5"),(lower_c,"Contrast x0.5"),(blended,"Blend 60/40")]]
r1=np.hstack([p[0],gv3(TH),p[1],gv3(TH),p[2]])
r2=np.hstack([p[3],gv3(TH),p[4],gv3(TH),p[5]])
arith=np.vstack([r1,gh3(r1),r2])
cv2.imwrite('outputs/p11_arithmetic.png', arith)

TH2,TW2=200,200
q=[lbl(rsz(x,TW2,TH2),t) for x,t in [(shape1,"Shape 1 (rect)"),(shape2,"Shape 2 (circle)"),
    (bit_and,"AND"),(bit_or,"OR"),(bit_xor,"XOR"),(bit_not1,"NOT shape1")]]
r3=np.hstack([q[0],gv3(TH2),q[1],gv3(TH2),q[2]])
r4=np.hstack([q[3],gv3(TH2),q[4],gv3(TH2),q[5]])
bitw=np.vstack([r3,gh3(r3),r4])
cv2.imwrite('outputs/p11_bitwise.png', bitw)
cv2.imwrite('outputs/p11_masked.png', lbl(masked_img,"Circle Mask Applied"))

print("\nSaved: outputs/p11_arithmetic.png")
print("Saved: outputs/p11_bitwise.png")
print("Saved: outputs/p11_masked.png")
print("[OK] Practical 11 Complete")
