# Practical 15: Image Pyramids & Optical Flow
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 15: Image Pyramids & Optical Flow")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

img  = cv2.imread('outputs/base_image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


gp = [img]
for _ in range(4):
    gp.append(cv2.pyrDown(gp[-1]))


lp = []
for i in range(len(gp)-1):
    up = cv2.pyrUp(gp[i+1], dstsize=(gp[i].shape[1], gp[i].shape[0]))
    lp.append(cv2.subtract(gp[i], up))

print(f"Gaussian Pyramid levels: {len(gp)}")
for i, level in enumerate(gp):
    print(f"  Level {i}: {level.shape[1]}x{level.shape[0]}")

print(f"\nLaplacian Pyramid levels: {len(lp)}")
for i, level in enumerate(lp):
    print(f"  Level {i}: {level.shape[1]}x{level.shape[0]}")


reconstructed = gp[-1].copy()
for i in range(len(lp)-1, -1, -1):
    up = cv2.pyrUp(reconstructed, dstsize=(lp[i].shape[1], lp[i].shape[0]))
    reconstructed = cv2.add(up, lp[i])

diff = cv2.absdiff(img, reconstructed)
print(f"\nReconstruction error (max pixel diff): {diff.max()}")


frame1 = gray.copy()
M = np.float32([[1, 0, 12], [0, 1, 8]])
frame2 = cv2.warpAffine(frame1, M, (frame1.shape[1], frame1.shape[0]))


corners = cv2.goodFeaturesToTrack(frame1, maxCorners=60, qualityLevel=0.01, minDistance=12)
p0 = corners.astype(np.float32)

lk_params = dict(winSize=(21,21), maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,30,0.01))
p1, st, err = cv2.calcOpticalFlowPyrLK(frame1, frame2, p0, None, **lk_params)

good_new = p1[st==1]
good_old = p0[st==1]

flow_vis = cv2.cvtColor(frame1, cv2.COLOR_GRAY2BGR)
for new, old in zip(good_new, good_old):
    a, b = new.ravel().astype(int)
    c, d = old.ravel().astype(int)
    cv2.arrowedLine(flow_vis, (c,d), (a,b), (0,255,0), 2, tipLength=0.3)
    cv2.circle(flow_vis, (c,d), 4, (255,100,0), -1)

tracked_pts = int(st.sum())
dx = float(np.mean(good_new[:,0] - good_old[:,0]))
dy = float(np.mean(good_new[:,1] - good_old[:,1]))
print(f"\nLucas-Kanade Optical Flow")
print(f"  Tracked points : {tracked_pts}")
print(f"  Mean flow dx   : {dx:.2f}  dy={dy:.2f}  (true shift: dx=12, dy=8)")


flow_dense = cv2.calcOpticalFlowFarneback(frame1, frame2, None,
    pyr_scale=0.5, levels=3, winsize=15, iterations=3,
    poly_n=5, poly_sigma=1.2, flags=0)
mag, ang = cv2.cartToPolar(flow_dense[...,0], flow_dense[...,1])
hsv_flow = np.zeros((frame1.shape[0], frame1.shape[1], 3), dtype=np.uint8)
hsv_flow[...,1] = 255
hsv_flow[...,0] = ang * 180 / np.pi / 2
hsv_flow[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
dense_vis = cv2.cvtColor(hsv_flow, cv2.COLOR_HSV2BGR)
print(f"Farneback dense flow: mean magnitude = {mag.mean():.3f}")


def lbl(im, txt):
    out = im.copy() if len(im.shape)==3 else cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.44,(255,255,255),1,cv2.LINE_AA)
    return out

TH,TW=190,240; gap=5
def rsz(im,tw=TW,th=TH):
    s=im if len(im.shape)==3 else cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
    return cv2.resize(s,(tw,th))
gv=np.full((TH,gap,3),160,np.uint8); gh=lambda r:np.full((gap,r.shape[1],3),160,np.uint8)


def lp_disp(im):
    n=cv2.normalize(cv2.convertScaleAbs(im),None,0,255,cv2.NORM_MINMAX)
    return n

r1=np.hstack([lbl(rsz(gp[0]),"Gaussian L0 640x480"),gv,
              lbl(rsz(gp[1]),"Gaussian L1 320x240"),gv,
              lbl(rsz(gp[2]),"Gaussian L2 160x120")])
r2=np.hstack([lbl(rsz(gp[3]),"Gaussian L3 80x60"),gv,
              lbl(rsz(lp_disp(lp[0])),"Laplacian L0"),gv,
              lbl(rsz(lp_disp(lp[1])),"Laplacian L1")])
r3=np.hstack([lbl(rsz(reconstructed),"Reconstructed"),gv,
              lbl(rsz(flow_vis),"LK Sparse Flow"),gv,
              lbl(rsz(dense_vis),"Farneback Dense Flow")])
grid=np.vstack([r1,gh(r1),r2,gh(r2),r3])
cv2.imwrite('outputs/p15_pyramids_flow.png', grid)
print("Saved: outputs/p15_pyramids_flow.png")
print("[OK] Practical 15 Complete")
