# Practical 9: Histograms & Histogram Equalization
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 9: Histograms & Equalization")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

img  = cv2.imread('outputs/base_image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


hist_gray = cv2.calcHist([gray], [0], None, [256], [0,256])
print(f"Grayscale histogram: 256 bins, range [0,256]")
print(f"  Peak bin value : {np.argmax(hist_gray)}")
print(f"  Max frequency  : {int(np.max(hist_gray))}")


colors_bgr = ('b','g','r')
hists = {}
for i, c in enumerate(colors_bgr):
    hists[c] = cv2.calcHist([img], [i], None, [256], [0,256])
print(f"BGR histograms computed for each channel")


eq_gray = cv2.equalizeHist(gray)
hist_eq  = cv2.calcHist([eq_gray], [0], None, [256], [0,256])
print(f"Histogram Equalization applied (grayscale)")


clahe      = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
clahe_gray = clahe.apply(gray)
print(f"CLAHE: clipLimit=2.0, tileGridSize=(8,8)")


def draw_hist(hist, color, h=200, w=256, bg=240):
    canvas = np.full((h, w, 3), bg, dtype=np.uint8)
    max_val = np.max(hist)
    for x in range(w):
        bar_h = int((hist[x] / max_val) * (h-4))
        cv2.line(canvas, (x, h-2), (x, h-2-bar_h), color, 1)
    return canvas

hist_canvas_gray = draw_hist(hist_gray, (80,80,80))
hist_canvas_eq   = draw_hist(hist_eq,   (60,120,60))
hist_b = draw_hist(hists['b'], (200, 60,  0))
hist_g = draw_hist(hists['g'], (0,  160,  0))
hist_r = draw_hist(hists['r'], (0,   60,180))


hist_bgr_combined = np.hstack([hist_b, hist_g, hist_r])  # 768 wide

def lbl(im, txt):
    out = im.copy()
    if len(out.shape) == 2:
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.48,(255,255,255),1,cv2.LINE_AA)
    return out

def rsz(im, w, h): return cv2.resize(im,(w,h))

TW, TH = 380, 270
gap = 6
gv = np.full((TH, gap, 3), 180, np.uint8)
gh = lambda r: np.full((gap, r.shape[1], 3), 180, np.uint8)

gray_bgr  = cv2.cvtColor(gray,      cv2.COLOR_GRAY2BGR)
eq_bgr    = cv2.cvtColor(eq_gray,   cv2.COLOR_GRAY2BGR)
clahe_bgr = cv2.cvtColor(clahe_gray,cv2.COLOR_GRAY2BGR)

r1 = np.hstack([lbl(rsz(gray_bgr,TW,TH),   "Grayscale"),  gv,
                lbl(rsz(eq_bgr,TW,TH),     "Equalized"),   gv,
                lbl(rsz(clahe_bgr,TW,TH),  "CLAHE")])
r2 = np.hstack([lbl(rsz(hist_canvas_gray,TW,TH),"Histogram - Gray"),  gv,
                lbl(rsz(hist_canvas_eq,TW,TH),  "Histogram - Equalized"),gv,
                lbl(rsz(hist_bgr_combined,TW,TH),"Histograms B | G | R")])

grid = np.vstack([r1, gh(r1), r2])
cv2.imwrite('outputs/p9_histograms.png', grid)
print(f"\nMean brightness (original) : {np.mean(gray):.1f}")
print(f"Mean brightness (equalized): {np.mean(eq_gray):.1f}")
print(f"Std dev (original)         : {np.std(gray):.1f}")
print(f"Std dev (equalized)        : {np.std(eq_gray):.1f}")
print("\nSaved: outputs/p9_histograms.png")
print("[OK] Practical 9 Complete")
