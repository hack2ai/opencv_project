# Practical 13: Color-based Segmentation & HSV Masking
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 13: Color-based Segmentation")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

img = cv2.imread('outputs/base_image.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


color_ranges = {
    "Sky (blue)":  ([90,  40,  80], [130, 255, 255]),
    "Grass (green)":([35,  40,  30], [ 85, 255, 200]),
    "Sun (yellow)": ([15,  80, 180], [ 40, 255, 255]),
    "House (slate)":([100, 20,  50], [130,  90, 200]),
    "Roof (dark blue)":([100,30,40],[130,100,160]),
}

masks  = {}
segs   = {}
for name, (lo, hi) in color_ranges.items():
    lower = np.array(lo, dtype=np.uint8)
    upper = np.array(hi, dtype=np.uint8)
    mask  = cv2.inRange(hsv, lower, upper)
    # Morphological clean-up
    k = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    seg  = cv2.bitwise_and(img, img, mask=mask)
    masks[name]  = mask
    segs[name]   = seg
    px_count = np.count_nonzero(mask)
    pct      = px_count / mask.size * 100
    print(f"  {name:<22} pixels={px_count:>7,}  ({pct:5.1f}%)")


combined_mask = np.zeros(img.shape[:2], dtype=np.uint8)
for m in masks.values():
    combined_mask = cv2.bitwise_or(combined_mask, m)
combined_seg  = cv2.bitwise_and(img, img, mask=combined_mask)
print(f"\n  Combined mask coverage: {np.count_nonzero(combined_mask)/combined_mask.size*100:.1f}%")

gc_img    = img.copy()
gc_mask   = np.zeros(img.shape[:2], dtype=np.uint8)
bgd_model = np.zeros((1,65), np.float64)
fgd_model = np.zeros((1,65), np.float64)
rect      = (50, 50, 540, 390)
cv2.grabCut(gc_img, gc_mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
fg_mask  = np.where((gc_mask==2)|(gc_mask==0), 0, 1).astype('uint8')
grabcut_result = img * fg_mask[:,:,np.newaxis]
print("GrabCut foreground extraction completed (5 iterations)")


def lbl(im, txt):
    out = im.copy() if len(im.shape)==3 else cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.44,(255,255,255),1,cv2.LINE_AA)
    return out

TH,TW=190,240; gap=5
def rsz(im): return cv2.resize(im,(TW,TH)) if len(im.shape)==3 else cv2.resize(cv2.cvtColor(im,cv2.COLOR_GRAY2BGR),(TW,TH))
gv=np.full((TH,gap,3),160,np.uint8); gh=lambda r:np.full((gap,r.shape[1],3),160,np.uint8)

seg_list=list(segs.items())
r1=np.hstack([lbl(rsz(img),"Original"),gv,lbl(rsz(seg_list[0][1]),seg_list[0][0]),gv,lbl(rsz(seg_list[1][1]),seg_list[1][0])])
r2=np.hstack([lbl(rsz(seg_list[2][1]),seg_list[2][0]),gv,lbl(rsz(seg_list[3][1]),seg_list[3][0]),gv,lbl(rsz(combined_seg),"All Colors Combined")])
r3=np.hstack([lbl(rsz(masks[seg_list[0][0]]),"Sky Mask"),gv,lbl(rsz(masks[seg_list[1][0]]),"Grass Mask"),gv,lbl(rsz(grabcut_result),"GrabCut Foreground")])
grid=np.vstack([r1,gh(r1),r2,gh(r2),r3])
cv2.imwrite('outputs/p13_segmentation.png', grid)
print("Saved: outputs/p13_segmentation.png")
print("[OK] Practical 13 Complete")
