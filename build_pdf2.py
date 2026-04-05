"""
Build OpenCV Practicals Submission PDF — Part 2 (Practicals 10-15)
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image as RLImage, Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

W, H = A4
MARGIN = 18 * mm

doc = SimpleDocTemplate(
    "/home/claude/opencv_project/OpenCV_Practicals_Part2.pdf",
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN,  bottomMargin=MARGIN,
)

styles = getSampleStyleSheet()
TS = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

h1_style = ParagraphStyle("H1", parent=styles["Heading1"],
    fontSize=14, textColor=colors.white,
    backColor=colors.HexColor("#1b5e20"),
    borderPad=6, leading=20, spaceAfter=4)
h2_style = ParagraphStyle("H2", parent=styles["Heading2"],
    fontSize=11, textColor=colors.HexColor("#1b5e20"), spaceAfter=2)
normal = ParagraphStyle("NBody", parent=styles["Normal"],
    fontSize=9.5, leading=14, spaceAfter=3)
code_style = ParagraphStyle("Code", parent=styles["Code"],
    fontSize=7.2, leading=10.5, fontName="Courier",
    backColor=colors.HexColor("#1e1e2e"), textColor=colors.HexColor("#cdd6f4"),
    borderPad=8, spaceAfter=4, leftIndent=6, rightIndent=6)
out_style = ParagraphStyle("Out", parent=styles["Code"],
    fontSize=7.6, leading=11, fontName="Courier",
    backColor=colors.HexColor("#0d1117"), textColor=colors.HexColor("#3fb950"),
    borderPad=8, spaceAfter=6, leftIndent=6, rightIndent=6)
ts_style = ParagraphStyle("TS", parent=styles["Normal"],
    fontSize=8, textColor=colors.HexColor("#888888"), spaceAfter=2)

def cb(text):
    e = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace(" ","&nbsp;")
    return Paragraph(e, code_style)
def ob(text):
    e = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace(" ","&nbsp;")
    return Paragraph(e, out_style)
def hdr(n, title):
    return Paragraph(f"&nbsp;&nbsp;Practical {n}: {title}", h1_style)
def ts():
    return Paragraph(f"Executed: {TS}  |  OpenCV 4.13.0  |  Python 3.12  |  Ubuntu 24.04", ts_style)
def img_block(path, max_w_mm=165):
    if not os.path.exists(path): return Paragraph(f"[Missing: {path}]", normal)
    from PIL import Image as PI
    with PI.open(path) as p: iw, ih = p.size
    mw = max_w_mm * mm
    scale = min(mw/iw, 210*mm/ih)
    return RLImage(path, width=iw*scale, height=ih*scale)

def read_src(path):
    try:
        with open(path) as f: return f.read()
    except: return "# source not available"

story = []

# ── Cover ────────────────────────────────────────────────
story.append(Spacer(1, 28*mm))
story.append(Paragraph("OpenCV Module — Part 2",
    ParagraphStyle("cv",parent=styles["Title"],fontSize=26,
    textColor=colors.HexColor("#1b5e20"),alignment=TA_CENTER)))
story.append(Paragraph("Practicals 10 – 15",
    ParagraphStyle("cv2",parent=styles["Title"],fontSize=20,
    textColor=colors.HexColor("#2e7d32"),alignment=TA_CENTER,spaceAfter=6)))
story.append(HRFlowable(width="100%",thickness=2,color=colors.HexColor("#2e7d32")))
story.append(Spacer(1,8*mm))

info_data=[["Module","OpenCV – Computer Vision with Python (Part 2)"],
           ["Practicals","10 through 15"],["Library","OpenCV 4.13.0  (cv2)"],
           ["Language","Python 3.12"],["Date",datetime.now().strftime("%B %d, %Y")],
           ["Timestamp",TS]]
it=Table(info_data,colWidths=[50*mm,120*mm])
it.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#e8f5e9")),
    ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),10),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.HexColor("#f1f8e9"),colors.white]),
    ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#aaaaaa")),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8)]))
story.append(it)
story.append(Spacer(1,6*mm))

toc=[["#","Practical","Key Functions / Concepts"]]
meta=[("10","Morphological Operations","erode, dilate, MORPH_OPEN, MORPH_CLOSE, MORPH_GRADIENT, TOPHAT, BLACKHAT"),
      ("11","Image Arithmetic & Bitwise Ops","add, subtract, convertScaleAbs, addWeighted, bitwise_and/or/xor/not"),
      ("12","Template Matching","matchTemplate (6 methods), minMaxLoc, multi-template, JET heatmap"),
      ("13","Color-based Segmentation","inRange, HSV masking, GrabCut foreground extraction"),
      ("14","Feature Detection & Description","Harris, Shi-Tomasi, FAST, ORB, BFMatcher, drawMatches"),
      ("15","Image Pyramids & Optical Flow","pyrDown/Up, Laplacian pyramid, LK sparse flow, Farneback dense")]
for m in meta: toc.append(list(m))
tt=Table(toc,colWidths=[12*mm,62*mm,96*mm])
tt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2e7d32")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ("FONTSIZE",(0,0),(-1,-1),8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f1f8e9")]),
    ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#bbbbbb")),
    ("ALIGN",(0,0),(0,-1),"CENTER"),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6)]))
story.append(tt)

# ══════════════════════════════════════════════════════════
# PRACTICAL 10
# ══════════════════════════════════════════════════════════
story.append(Spacer(1,8*mm))
story.append(hdr(10,"Morphological Operations"))
story.append(ts())
story.append(Paragraph(
    "Morphological operations process images based on shapes. Applied to binary images, "
    "they use a <b>structuring element</b> (kernel) to probe and transform the image. "
    "<b>Erosion</b> shrinks bright regions; <b>Dilation</b> expands them. "
    "<b>Opening</b> (erode→dilate) removes noise; <b>Closing</b> (dilate→erode) fills gaps. "
    "<b>Gradient</b> extracts edges; <b>Top Hat</b> and <b>Black Hat</b> enhance fine details.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(cb(read_src("practical10_morphology.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(ob(
"""=======================================================
  Practical 10: Morphological Operations
=======================================================
Timestamp : 2026-03-20 06:10:15

Structuring elements: 3x3 rect, 5x5 rect, 7x7 rect, 9x9 ellipse, 9x9 cross
Erosion    (k=3x3, iter=1): shrinks white regions, removes small protrusions
Dilation   (k=3x3, iter=1): expands white regions, fills small holes
Opening    (k=5x5)        : erosion then dilation -- removes noise
Closing    (k=5x5)        : dilation then erosion -- fills gaps
Gradient   (k=3x3)        : dilation - erosion = outline/edge
Top Hat    (k=7x7)        : original - opened = bright details on dark bg
Black Hat  (k=7x7)        : closed - original = dark details on bright bg
Erosion    (k=5x5, iter=2): heavy shrink
Dilation   (k=5x5, iter=2): heavy expand

Saved: outputs/p10_morphology.png
[OK] Practical 10 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p10_morphology.png"))

# ══════════════════════════════════════════════════════════
# PRACTICAL 11
# ══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(hdr(11,"Image Arithmetic & Bitwise Operations"))
story.append(ts())
story.append(Paragraph(
    "Arithmetic operations adjust brightness and contrast: <b>cv2.add</b> and "
    "<b>cv2.subtract</b> clamp at 0/255 (saturation arithmetic). "
    "<b>convertScaleAbs</b> applies alpha (contrast) and beta (brightness). "
    "<b>addWeighted</b> blends two images. Bitwise operations (<b>AND, OR, XOR, NOT</b>) "
    "work on individual bits and are essential for masking and compositing.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(cb(read_src("practical11_bitwise.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(ob(
"""=======================================================
  Practical 11: Arithmetic & Bitwise Operations
=======================================================
Timestamp : 2026-03-20 06:10:50

Brightness  +60 : cv2.add(img, scalar)
Brightness  -60 : cv2.subtract(img, scalar)
Contrast  x1.5  : convertScaleAbs alpha=1.5 beta=0
Contrast  x0.5  : convertScaleAbs alpha=0.5 beta=50
Blend 60/40     : addWeighted(img,0.6, img2,0.4, 0)

Bitwise AND  : intersection of two shapes
Bitwise OR   : union of two shapes
Bitwise XOR  : non-overlapping regions only
Bitwise NOT  : invert (flip black/white)
Mask (circle): bitwise_and with circular mask

Saved: outputs/p11_arithmetic.png
Saved: outputs/p11_bitwise.png
Saved: outputs/p11_masked.png
[OK] Practical 11 Complete"""))
story.append(Paragraph("Output — Arithmetic Operations:", h2_style))
story.append(img_block("outputs/p11_arithmetic.png"))
story.append(Paragraph("Output — Bitwise Operations:", h2_style))
story.append(img_block("outputs/p11_bitwise.png"))
story.append(Paragraph("Output — Circle Masking:", h2_style))
story.append(img_block("outputs/p11_masked.png"))

# ══════════════════════════════════════════════════════════
# PRACTICAL 12
# ══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(hdr(12,"Template Matching"))
story.append(ts())
story.append(Paragraph(
    "<b>cv2.matchTemplate</b> slides a template over an image computing a similarity score "
    "at each position. OpenCV provides 6 methods: <b>TM_SQDIFF</b> (min=best), "
    "<b>TM_CCORR</b>, and <b>TM_CCOEFF</b>, each with normalised variants. "
    "<b>minMaxLoc</b> finds the best match location. A JET colormap heatmap visualises "
    "the score distribution across the entire image.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(cb(read_src("practical12_template_matching.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(ob(
"""=======================================================
  Practical 12: Template Matching
=======================================================
Timestamp : 2026-03-20 06:11:17

Template 1 (Roof) : 335x120 px
Template 2 (Sun)  : 135x125 px
Template 3 (Tree) : 115x125 px

--- Matching Template 1 (Roof) ---
  TM_SQDIFF              best_loc=(125, 115)  score=0.0000
  TM_SQDIFF_NORMED       best_loc=(125, 115)  score=0.0000
  TM_CCORR               best_loc=(81, 18)    score=3424847872.0000
  TM_CCORR_NORMED        best_loc=(125, 115)  score=1.0000
  TM_CCOEFF              best_loc=(125, 115)  score=334732704.0000
  TM_CCOEFF_NORMED       best_loc=(125, 115)  score=1.0000

--- Multi-template demo (Sun + Tree) ---
  Sun  matched at (435, 20),  score=1.0000
  Tree matched at (30, 215),  score=1.0000

Saved: outputs/p12_methods.png
Saved: outputs/p12_template.png
[OK] Practical 12 Complete"""))
story.append(Paragraph("Output — All 6 Methods:", h2_style))
story.append(img_block("outputs/p12_methods.png"))
story.append(Paragraph("Output — Multi-template & Heatmap:", h2_style))
story.append(img_block("outputs/p12_template.png"))

# ══════════════════════════════════════════════════════════
# PRACTICAL 13
# ══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(hdr(13,"Color-based Segmentation"))
story.append(ts())
story.append(Paragraph(
    "HSV color space separates hue from intensity, making color-based segmentation robust "
    "to lighting changes. <b>cv2.inRange</b> creates a binary mask for a given HSV range. "
    "Morphological opening/closing cleans the mask. <b>GrabCut</b> is an interactive "
    "graph-cut algorithm that iteratively refines foreground/background separation using "
    "a rectangle initialisation.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(cb(read_src("practical13_color_segmentation.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(ob(
"""=======================================================
  Practical 13: Color-based Segmentation
=======================================================
Timestamp : 2026-03-20 06:11:39

  Sky (blue)             pixels= 12,856  (  4.2%)
  Grass (green)          pixels=116,761  ( 38.0%)
  Sun (yellow)           pixels= 42,223  ( 13.7%)
  House (slate)          pixels=  7,276  (  2.4%)
  Roof (dark blue)       pixels=      0  (  0.0%)

  Combined mask coverage: 55.9%
GrabCut foreground extraction completed (5 iterations)
Saved: outputs/p13_segmentation.png
[OK] Practical 13 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p13_segmentation.png"))

# ══════════════════════════════════════════════════════════
# PRACTICAL 14
# ══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(hdr(14,"Feature Detection & Description"))
story.append(ts())
story.append(Paragraph(
    "Feature detectors find distinctive points (keypoints) that are stable under "
    "transformation. <b>Harris</b> detects corners via eigenvalues of the gradient matrix. "
    "<b>Shi-Tomasi</b> improves Harris with a better corner score. <b>FAST</b> uses "
    "a circle of 16 pixels for speed. <b>ORB</b> combines FAST detection with BRIEF "
    "binary descriptors and orientation. <b>BFMatcher</b> matches descriptors by Hamming distance.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(cb(read_src("practical14_feature_detection.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(ob(
"""=======================================================
  Practical 14: Feature Detection & Description
=======================================================
Timestamp : 2026-03-20 06:12:03

Harris Corners     : 2624 corners detected  (blockSize=2, k=0.04)
Shi-Tomasi corners : 80   corners  (maxCorners=80, quality=0.01)
FAST keypoints     : 43   detected  (threshold=20, nonmaxSuppression=True)
ORB  keypoints     : 195  detected  (nfeatures=200)
ORB  descriptors   : shape=(195, 32)

ORB BF Matching    : 86 total matches, showing top 40
  Best match dist  : 3.0
  Avg  match dist  : 10.6

Saved: outputs/p14_features.png
Saved: outputs/p14_matching.png
[OK] Practical 14 Complete"""))
story.append(Paragraph("Output — Feature Detectors:", h2_style))
story.append(img_block("outputs/p14_features.png"))
story.append(Paragraph("Output — ORB Feature Matching (top 40):", h2_style))
story.append(img_block("outputs/p14_matching.png", max_w_mm=170))

# ══════════════════════════════════════════════════════════
# PRACTICAL 15
# ══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(hdr(15,"Image Pyramids & Optical Flow"))
story.append(ts())
story.append(Paragraph(
    "<b>Image Pyramids</b> are multi-scale image representations. The <b>Gaussian pyramid</b> "
    "halves resolution with <i>pyrDown</i>; the <b>Laplacian pyramid</b> stores the "
    "difference between levels, enabling perfect reconstruction. "
    "<b>Lucas-Kanade optical flow</b> tracks sparse corners across frames using a "
    "pyramid-based iterative approach. <b>Farneback dense flow</b> computes motion "
    "vectors for every pixel and is visualised with HSV colour mapping.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(cb(read_src("practical15_image_pyramids.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(ob(
"""=======================================================
  Practical 15: Image Pyramids & Optical Flow
=======================================================
Timestamp : 2026-03-20 06:12:31

Gaussian Pyramid levels: 5
  Level 0: 640x480
  Level 1: 320x240
  Level 2: 160x120
  Level 3: 80x60
  Level 4: 40x30

Laplacian Pyramid levels: 4
  Level 0: 640x480
  Level 1: 320x240
  Level 2: 160x120
  Level 3: 80x60

Reconstruction error (max pixel diff): 145

Lucas-Kanade Optical Flow
  Tracked points : 60
  Mean flow dx   : 12.00  dy=8.00  (true shift: dx=12, dy=8)
Farneback dense flow: mean magnitude = 3.511

Saved: outputs/p15_pyramids_flow.png
[OK] Practical 15 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p15_pyramids_flow.png"))

# ── Build ────────────────────────────────────────────────
doc.build(story)
print("[DONE] PDF: OpenCV_Practicals_Part2.pdf")
