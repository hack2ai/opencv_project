# Practical 12: Template Matching
import cv2
import numpy as np
from datetime import datetime

print("=" * 55)
print("  Practical 12: Template Matching")
print("=" * 55)
print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

img = cv2.imread('outputs/base_image.png')
h, w = img.shape[:2]



tmpl_roof = img[115:235, 125:460].copy()

tmpl_sun  = img[20:145,  435:570].copy()

tmpl_tree = img[215:340,  30:145].copy()

print(f"Template 1 (Roof) : {tmpl_roof.shape[1]}x{tmpl_roof.shape[0]} px")
print(f"Template 2 (Sun)  : {tmpl_sun.shape[1]}x{tmpl_sun.shape[0]}  px")
print(f"Template 3 (Tree) : {tmpl_tree.shape[1]}x{tmpl_tree.shape[0]} px")


METHODS = {
    "TM_SQDIFF"        : cv2.TM_SQDIFF,
    "TM_SQDIFF_NORMED" : cv2.TM_SQDIFF_NORMED,
    "TM_CCORR"         : cv2.TM_CCORR,
    "TM_CCORR_NORMED"  : cv2.TM_CCORR_NORMED,
    "TM_CCOEFF"        : cv2.TM_CCOEFF,
    "TM_CCOEFF_NORMED" : cv2.TM_CCOEFF_NORMED,
}

def match_and_draw(scene, tmpl, method_id, method_name):
    result  = cv2.matchTemplate(scene, tmpl, method_id)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # For SQDIFF methods, minimum is the best match
    top_left = min_loc if method_id in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED) else max_loc
    th, tw    = tmpl.shape[:2]
    bottom_right = (top_left[0]+tw, top_left[1]+th)
    vis = scene.copy()
    cv2.rectangle(vis, top_left, bottom_right, (0, 255, 0), 3)
    cv2.putText(vis, method_name, (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(vis, method_name, (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (0,80,200), 1, cv2.LINE_AA)
    score = min_val if method_id in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED) else max_val
    return vis, top_left, score, result

print("\n--- Matching Template 1 (Roof) ---")
method_results = []
for name, mid in METHODS.items():
    vis, loc, score, hmap = match_and_draw(img, tmpl_roof, mid, name)
    method_results.append((vis, hmap, name, loc, score))
    print(f"  {name:<22} best_loc={loc}  score={score:.4f}")


print("\n--- Multi-template demo (Sun + Tree) ---")
vis_sun,  loc_sun,  sc_sun,  _ = match_and_draw(img, tmpl_sun,  cv2.TM_CCOEFF_NORMED, "Sun")
vis_tree, loc_tree, sc_tree, _ = match_and_draw(img, tmpl_tree, cv2.TM_CCOEFF_NORMED, "Tree")
print(f"  Sun  matched at {loc_sun},  score={sc_sun:.4f}")
print(f"  Tree matched at {loc_tree}, score={sc_tree:.4f}")


_, _, _, hmap_best = match_and_draw(img, tmpl_roof, cv2.TM_CCOEFF_NORMED, "")
hmap_norm = cv2.normalize(hmap_best, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
hmap_color = cv2.applyColorMap(hmap_norm, cv2.COLORMAP_JET)
hmap_resized = cv2.resize(hmap_color, (w, h))


def lbl(im, txt):
    out = im.copy()
    cv2.rectangle(out,(0,out.shape[0]-26),(out.shape[1],out.shape[0]),(20,20,20),-1)
    cv2.putText(out,txt,(5,out.shape[0]-7),cv2.FONT_HERSHEY_SIMPLEX,0.44,(255,255,255),1,cv2.LINE_AA)
    return out

TH,TW=200,260; gap=5
def rsz(im): return cv2.resize(im,(TW,TH))
gv=np.full((TH,gap,3),160,np.uint8); gh=lambda r:np.full((gap,r.shape[1],3),160,np.uint8)

method_imgs = [lbl(rsz(r[0]), r[2]) for r in method_results]
r1=np.hstack([method_imgs[0],gv,method_imgs[1],gv,method_imgs[2]])
r2=np.hstack([method_imgs[3],gv,method_imgs[4],gv,method_imgs[5]])
grid_methods=np.vstack([r1,gh(r1),r2])
cv2.imwrite('outputs/p12_methods.png', grid_methods)

r3=np.hstack([lbl(rsz(img),"Scene"),gv,
              lbl(rsz(vis_sun),"Sun Matched"),gv,
              lbl(rsz(vis_tree),"Tree Matched")])
r4=np.hstack([lbl(rsz(hmap_resized),"Match Heatmap (JET)"),gv,
              lbl(cv2.resize(tmpl_roof,(TW,TH)),"Template: Roof"),gv,
              lbl(cv2.resize(tmpl_sun, (TW,TH)),"Template: Sun")])
grid2=np.vstack([r3,gh(r3),r4])
cv2.imwrite('outputs/p12_template.png', grid2)

print("\nSaved: outputs/p12_methods.png")
print("Saved: outputs/p12_template.png")
print("[OK] Practical 12 Complete")
