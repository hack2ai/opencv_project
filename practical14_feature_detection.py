# Practical 14: Feature Detection & Description
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 14: Feature Detection & Description")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

img  = cv2.imread('outputs/base_image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_f = np.float32(gray)


harris = cv2.cornerHarris(gray_f, blockSize=2, ksize=3, k=0.04)
harris_dilated = cv2.dilate(harris, None)
harris_vis = img.copy()
harris_vis[harris_dilated > 0.01 * harris_dilated.max()] = [0, 0, 255]
corners_count = np.sum(harris_dilated > 0.01 * harris_dilated.max())
print(f"Harris Corners     : {corners_count} corners detected  (blockSize=2, k=0.04)")


shi_corners = cv2.goodFeaturesToTrack(gray, maxCorners=80, qualityLevel=0.01,
                                       minDistance=10)
shi_vis = img.copy()
if shi_corners is not None:
    shi_corners = np.int32(shi_corners)
    for c in shi_corners:
        x, y = c.ravel()
        cv2.circle(shi_vis, (x, y), 5, (0, 255, 0), -1)
        cv2.circle(shi_vis, (x, y), 5, (0,150, 0),   1)
print(f"Shi-Tomasi corners : {len(shi_corners) if shi_corners is not None else 0} corners  (maxCorners=80, quality=0.01)")


fast = cv2.FastFeatureDetector_create(threshold=20, nonmaxSuppression=True)
kp_fast = fast.detect(gray, None)
fast_vis = cv2.drawKeypoints(img, kp_fast, None, color=(255,180,0),
                              flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
print(f"FAST keypoints     : {len(kp_fast)} detected  (threshold=20, nonmaxSuppression=True)")


orb  = cv2.ORB_create(nfeatures=200)
kp_orb, des_orb = orb.detectAndCompute(gray, None)
orb_vis = cv2.drawKeypoints(img, kp_orb, None, color=(0,200,255),
                             flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
print(f"ORB keypoints      : {len(kp_orb)} detected  (nfeatures=200)")
print(f"ORB descriptors    : shape={des_orb.shape if des_orb is not None else 'None'}")


M = cv2.getRotationMatrix2D((img.shape[1]//2, img.shape[0]//2), 15, 0.9)
img2 = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
kp2, des2 = orb.detectAndCompute(gray2, None)

if des_orb is not None and des2 is not None:
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(bf.match(des_orb, des2), key=lambda x: x.distance)
    top_matches = matches[:40]
    match_vis = cv2.drawMatches(img, kp_orb, img2, kp2, top_matches, None,
                                 flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    print(f"\nORB BF Matching    : {len(matches)} total matches, showing top 40")
    print(f"  Best match dist  : {top_matches[0].distance:.1f}")
    print(f"  Avg  match dist  : {sum(m.distance for m in top_matches)/len(top_matches):.1f}")
else:
    match_vis = img.copy()


def lbl(im, txt):
    out = im.copy()
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.44,(255,255,255),1,cv2.LINE_AA)
    return out

TH,TW=220,310; gap=5
def rsz(im): return cv2.resize(im,(TW,TH))
gv=np.full((TH,gap,3),160,np.uint8); gh=lambda r:np.full((gap,r.shape[1],3),160,np.uint8)

r1=np.hstack([lbl(rsz(harris_vis),"Harris Corners"),gv,lbl(rsz(shi_vis),"Shi-Tomasi"),gv,lbl(rsz(fast_vis),"FAST")])
r2=np.hstack([lbl(rsz(orb_vis),"ORB Keypoints"),gv,lbl(rsz(img2),"Rotated Copy"),gv,lbl(rsz(img),"Original")])
grid1=np.vstack([r1,gh(r1),r2])
cv2.imwrite('outputs/p14_features.png', grid1)

MH,MW=300,900
match_out=cv2.resize(match_vis,(MW,MH))
cv2.rectangle(match_out,(0,MH-28),(MW,MH),(20,20,20),-1)
cv2.putText(match_out,"ORB BF Matching — top 40 correspondences",(5,MH-8),
            cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,255),1,cv2.LINE_AA)
cv2.imwrite('outputs/p14_matching.png', match_out)

print("\nSaved: outputs/p14_features.png")
print("Saved: outputs/p14_matching.png")
print("[OK] Practical 14 Complete")
