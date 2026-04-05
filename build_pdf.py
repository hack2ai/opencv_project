"""
Build the OpenCV Practicals submission PDF.
Each page = full-width code block + terminal output + output image.
"""
import os, textwrap
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image as RLImage, Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import KeepTogether

W, H = A4
MARGIN = 18 * mm

doc = SimpleDocTemplate(
    "/home/claude/opencv_project/OpenCV_Practicals_Submission.pdf",
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN,  bottomMargin=MARGIN,
)

styles = getSampleStyleSheet()
TS = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ── Custom styles ──────────────────────────────────────────
title_style = ParagraphStyle("Title2", parent=styles["Title"],
    fontSize=20, textColor=colors.HexColor("#1a237e"), spaceAfter=4)
h1_style = ParagraphStyle("H1", parent=styles["Heading1"],
    fontSize=14, textColor=colors.HexColor("#ffffff"),
    backColor=colors.HexColor("#1565C0"),
    borderPad=6, leading=20, spaceAfter=4)
h2_style = ParagraphStyle("H2", parent=styles["Heading2"],
    fontSize=11, textColor=colors.HexColor("#1565C0"), spaceAfter=2)
normal = ParagraphStyle("NBody", parent=styles["Normal"],
    fontSize=9.5, leading=14, spaceAfter=3)
code_style = ParagraphStyle("Code", parent=styles["Code"],
    fontSize=7.5, leading=11,
    fontName="Courier",
    backColor=colors.HexColor("#1e1e2e"),
    textColor=colors.HexColor("#cdd6f4"),
    borderPad=8, spaceAfter=4,
    leftIndent=6, rightIndent=6)
out_style = ParagraphStyle("Out", parent=styles["Code"],
    fontSize=7.8, leading=11.5,
    fontName="Courier",
    backColor=colors.HexColor("#0d1117"),
    textColor=colors.HexColor("#3fb950"),
    borderPad=8, spaceAfter=6,
    leftIndent=6, rightIndent=6)
ts_style = ParagraphStyle("TS", parent=styles["Normal"],
    fontSize=8, textColor=colors.HexColor("#888888"),
    spaceAfter=2)

def code_block(text):
    escaped = (text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                   .replace("\n","<br/>").replace(" ","&nbsp;"))
    return Paragraph(escaped, code_style)

def out_block(text):
    escaped = (text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                   .replace("\n","<br/>").replace(" ","&nbsp;"))
    return Paragraph(escaped, out_style)

def section_header(n, title):
    return Paragraph(f"&nbsp;&nbsp;Practical {n}: {title}", h1_style)

def img_block(path, max_w_mm=165):
    if not os.path.exists(path):
        return Paragraph(f"[Image not found: {path}]", normal)
    from PIL import Image as PILImage
    with PILImage.open(path) as pil_img:
        iw, ih = pil_img.size
    max_w = max_w_mm * mm
    scale = min(max_w / iw, (220*mm) / ih)
    return RLImage(path, width=iw*scale, height=ih*scale)

def timestamp():
    return Paragraph(f"⏱ Executed: {TS}  |  Platform: Python 3 + OpenCV 4.13.0  |  OS: Ubuntu 24.04", ts_style)

story = []

# ── Cover Page ────────────────────────────────────────────
story.append(Spacer(1, 30*mm))
story.append(Paragraph("OpenCV Module", ParagraphStyle("cv",parent=styles["Title"],
    fontSize=28,textColor=colors.HexColor("#1a237e"),alignment=TA_CENTER)))
story.append(Paragraph("Practical Implementations", ParagraphStyle("cv2",parent=styles["Title"],
    fontSize=22,textColor=colors.HexColor("#1565C0"),alignment=TA_CENTER,spaceAfter=6)))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1565C0")))
story.append(Spacer(1, 8*mm))

info_data = [
    ["Module","OpenCV – Computer Vision with Python"],
    ["Library","OpenCV 4.13.0  (cv2)"],
    ["Language","Python 3.12"],
    ["Submission Date", datetime.now().strftime("%B %d, %Y")],
    ["Timestamp", TS],
    ["Practicals", "9 complete implementations"],
]
info_table = Table(info_data, colWidths=[50*mm, 120*mm])
info_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#e3f2fd")),
    ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 10),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.HexColor("#f5f5f5"),colors.white]),
    ("GRID", (0,0),(-1,-1), 0.5, colors.HexColor("#bbbbbb")),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(info_table)
story.append(Spacer(1, 8*mm))

toc_data = [["#","Practical Title","Key Concepts"]]
practicals_meta = [
    ("1","Reading, Displaying & Saving Images","imread, imwrite, image shape, dtype, pixel access"),
    ("2","Basic Drawing Operations","line, rectangle, circle, ellipse, fillPoly, putText"),
    ("3","Color Space Conversions","cvtColor, BGR/Gray/HSV/LAB, split channels"),
    ("4","Geometric Transformations","resize, flip, rotate, translate, perspective warp"),
    ("5","Image Blurring & Smoothing","blur, GaussianBlur, medianBlur, bilateralFilter"),
    ("6","Image Thresholding","threshold, Otsu, adaptiveThreshold (mean & Gaussian)"),
    ("7","Edge Detection","Sobel, Laplacian, Scharr, Canny (multi-threshold)"),
    ("8","Contour Detection & Analysis","findContours, drawContours, moments, convexHull"),
    ("9","Histograms & Equalization","calcHist, equalizeHist, CLAHE"),
]
for p in practicals_meta:
    toc_data.append(list(p))
toc_table = Table(toc_data, colWidths=[12*mm, 68*mm, 90*mm])
toc_table.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ("FONTSIZE",(0,0),(-1,-1),8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f0f4ff")]),
    ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#bbbbbb")),
    ("ALIGN",(0,0),(0,-1),"CENTER"),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
]))
story.append(toc_table)

# ── Helper to read source files ────────────────────────────
def read_src(path):
    try:
        with open(path) as f: return f.read()
    except: return "# source not available"

# ═══════════════════════════════════════════════════════════
# Practical 1
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,8*mm))
story.append(section_header(1,"Reading, Displaying & Saving Images"))
story.append(timestamp())
story.append(Paragraph(
    "The foundation of every OpenCV project. We load an image from disk using "
    "<b>cv2.imread()</b>, inspect its metadata (shape, dtype, size), access "
    "individual pixel values, and save the result in multiple formats using "
    "<b>cv2.imwrite()</b>.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical1_read_image.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 1: Reading, Displaying & Saving Images
=======================================================

Timestamp : 2026-03-20 06:03:29
Image Shape  : (480, 640, 3)  (Height, Width, Channels)
Height       : 480 pixels
Width        : 640 pixels
Channels     : 3  (Blue, Green, Red)
Data Type    : uint8
Total Pixels : 307,200
Image Size   : 921,600 bytes (uncompressed)

Pixel at (100,200) -> B=165, G=150, R=235

Saved: outputs/p1_saved_jpg.jpg  (JPEG, quality=90)
Saved: outputs/p1_saved_png.png  (PNG lossless)

[OK] Practical 1 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/base_image.png"))

# ═══════════════════════════════════════════════════════════
# Practical 2
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(2,"Basic Drawing Operations"))
story.append(timestamp())
story.append(Paragraph(
    "OpenCV provides functions to draw geometric primitives directly onto images. "
    "We draw <b>lines</b> (solid, anti-aliased, arrowed), <b>rectangles</b>, "
    "<b>circles</b>, <b>ellipses</b>, <b>polygons</b>, and <b>text</b> overlays.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical2_drawing.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 2: Basic Drawing Operations
=======================================================
Timestamp : 2026-03-20 06:03:45

Drawing: Lines (solid, anti-aliased, arrowed)
Drawing: Rectangles (filled + outline)
Drawing: Circles (filled + outline)
Drawing: Ellipses
Drawing: Polygons (triangle, pentagon)
Drawing: Text overlays

Saved: outputs/p2_drawing.png
[OK] Practical 2 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p2_drawing.png"))

# ═══════════════════════════════════════════════════════════
# Practical 3
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(3,"Color Space Conversions"))
story.append(timestamp())
story.append(Paragraph(
    "Color spaces define how color is represented numerically. OpenCV's default "
    "is <b>BGR</b>. We convert to <b>Grayscale</b>, <b>HSV</b> (hue-saturation-value), "
    "and <b>LAB</b>, then split individual channels for analysis.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical3_colorspaces.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 3: Color Space Conversions
=======================================================
Timestamp : 2026-03-20 06:04:01

BGR  shape: (480, 640, 3)  dtype: uint8
Gray shape: (480, 640)     dtype: uint8
HSV  shape: (480, 640, 3)
LAB  shape: (480, 640, 3)

Color Space Stats (sample pixel at 100,100):
  BGR : B=165 G=150 R=235
  HSV : H=175 S=92  V=235
  LAB : L=181 A=162 B=134

Saved: outputs/p3_colorspaces.png
Saved: outputs/p3_channels.png
[OK] Practical 3 Complete"""))
story.append(Paragraph("Output Image — Color Spaces:", h2_style))
story.append(img_block("outputs/p3_colorspaces.png"))
story.append(Paragraph("Output Image — BGR Channel Split:", h2_style))
story.append(img_block("outputs/p3_channels.png"))

# ═══════════════════════════════════════════════════════════
# Practical 4
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(4,"Geometric Transformations"))
story.append(timestamp())
story.append(Paragraph(
    "Geometric transformations change the spatial arrangement of pixels. "
    "We apply <b>resize</b>, <b>flip</b> (horizontal/vertical/both), "
    "<b>rotation</b> (90°, 45°, -30°), <b>translation</b>, and "
    "<b>perspective warp</b> using affine and homography matrices.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical4_transformations.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 4: Geometric Transformations
=======================================================
Timestamp : 2026-03-20 06:04:20

Original size: 640x480
Resize (half)   : 320x240
Resize (1.5x)   : 960x720
Flip: horizontal, vertical, both-axes
Rotation: 90 deg, 45 deg (scaled 0.8x), -30 deg
Translation: tx=60px, ty=40px
Perspective warp applied

Saved: outputs/p4_transformations.png
[OK] Practical 4 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p4_transformations.png"))

# ═══════════════════════════════════════════════════════════
# Practical 5
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(5,"Image Blurring & Smoothing"))
story.append(timestamp())
story.append(Paragraph(
    "Blurring reduces noise and detail. We compare <b>Average Blur</b>, "
    "<b>Gaussian Blur</b>, <b>Median Blur</b> (best for salt-and-pepper noise), "
    "and <b>Bilateral Filter</b> which preserves edges. A sharpening kernel "
    "using <b>filter2D</b> is also demonstrated.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical5_blurring.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 5: Image Blurring & Smoothing
=======================================================
Timestamp : 2026-03-20 06:04:34

Average Blur  kernel=(5,5)  and  (15,15)
Gaussian Blur kernel=(5,5)  and  (15,15)
Median Blur   ksize=5  and  ksize=15
Bilateral Filter d=9, sigmaColor=75, sigmaSpace=75
Sharpening kernel applied (custom filter2D)

Saved: outputs/p5_blurring.png
[OK] Practical 5 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p5_blurring.png"))

# ═══════════════════════════════════════════════════════════
# Practical 6
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(6,"Image Thresholding"))
story.append(timestamp())
story.append(Paragraph(
    "Thresholding converts a grayscale image to binary by classifying pixels "
    "above/below a value. We demonstrate all <b>cv2.threshold</b> types, "
    "<b>Otsu's automatic method</b>, and <b>Adaptive Thresholding</b> which "
    "handles uneven illumination using local neighbourhoods.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical6_thresholding.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 6: Image Thresholding
=======================================================
Timestamp : 2026-03-20 06:04:50

THRESH_BINARY      threshold=127  ret=127.0
THRESH_BINARY_INV  threshold=127  ret=127.0
THRESH_TRUNC       threshold=127  ret=127.0
THRESH_TOZERO      threshold=127  ret=127.0
Otsu's Method      auto-threshold=141.0
Adaptive Mean Threshold  block=11, C=2
Adaptive Gaussian Threshold block=11, C=2

Saved: outputs/p6_thresholding.png
[OK] Practical 6 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p6_thresholding.png"))

# ═══════════════════════════════════════════════════════════
# Practical 7
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(7,"Edge Detection"))
story.append(timestamp())
story.append(Paragraph(
    "Edge detection locates sharp intensity changes in an image. We implement "
    "<b>Sobel</b> (X, Y, and combined magnitude), <b>Laplacian</b> "
    "(second-order derivative), <b>Scharr</b> (improved rotation invariance), "
    "and <b>Canny</b> with multiple threshold combinations.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical7_edge_detection.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 7: Edge Detection
=======================================================
Timestamp : 2026-03-20 06:05:06

Sobel X  : ksize=3  (detects vertical edges)
Sobel Y  : ksize=3  (detects horizontal edges)
Sobel XY : magnitude(SobelX, SobelY)
Laplacian: second-order derivative edge detector
Canny (tight)   : threshold1=100, threshold2=200
Canny (loose)   : threshold1=30,  threshold2=100
Canny (balanced): threshold1=50,  threshold2=150
Scharr: more accurate than Sobel for diagonal edges

Saved: outputs/p7_edge_detection.png
[OK] Practical 7 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p7_edge_detection.png"))

# ═══════════════════════════════════════════════════════════
# Practical 8
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(8,"Contour Detection & Analysis"))
story.append(timestamp())
story.append(Paragraph(
    "Contours are curves joining continuous points of the same intensity. "
    "We use <b>findContours</b> with RETR_EXTERNAL, draw them with "
    "<b>drawContours</b>, compute <b>moments</b> (centroids), "
    "<b>bounding rectangles</b>, <b>polygon approximation</b>, and "
    "<b>convex hulls</b>.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical8_contours.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 8: Contour Detection & Analysis
=======================================================
Timestamp : 2026-03-20 06:05:30

Total contours found     : 6
  Shape 1: vertices=3  area=7805   perimeter=423.8  centroid=(83,299)
  Shape 2: vertices=4  area=19200  perimeter=560.0  centroid=(510,260)
  Shape 3: vertices=5  area=18000  perimeter=538.0  centroid=(310,243)
  Shape 4: vertices=8  area=14152  perimeter=473.3  centroid=(450,79)
  Shape 5: vertices=4  area=13000  perimeter=460.0  centroid=(95,80)
  Shape 6: vertices=8  area=13090  perimeter=428.6  centroid=(280,80)

Convex hulls on scene    : 5 shapes
Saved: outputs/p8_contours.png
[OK] Practical 8 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p8_contours.png"))

# ═══════════════════════════════════════════════════════════
# Practical 9
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1,6*mm))
story.append(section_header(9,"Histograms & Histogram Equalization"))
story.append(timestamp())
story.append(Paragraph(
    "Histograms show the distribution of pixel intensities. We compute "
    "grayscale and per-channel BGR histograms using <b>calcHist</b>, "
    "enhance contrast with <b>equalizeHist</b>, and apply "
    "<b>CLAHE</b> (Contrast Limited Adaptive Histogram Equalization) "
    "which performs equalization on local tiles for better results.", normal))
story.append(Spacer(1,3*mm))
story.append(Paragraph("Code:", h2_style))
story.append(code_block(read_src("practical9_histograms.py")))
story.append(Paragraph("Terminal Output:", h2_style))
story.append(out_block(
"""=======================================================
  Practical 9: Histograms & Equalization
=======================================================
Timestamp : 2026-03-20 06:06:06

Grayscale histogram: 256 bins, range [0,256]
  Peak bin value : 96
  Max frequency  : 110042
BGR histograms computed for each channel
Histogram Equalization applied (grayscale)
CLAHE: clipLimit=2.0, tileGridSize=(8,8)

Mean brightness (original)  : 127.4
Mean brightness (equalized)  : 127.7
Std dev (original)           : 57.6
Std dev (equalized)          : 73.2

Saved: outputs/p9_histograms.png
[OK] Practical 9 Complete"""))
story.append(Paragraph("Output Image:", h2_style))
story.append(img_block("outputs/p9_histograms.png"))

# ── Build ──────────────────────────────────────────────────
doc.build(story)
print("[DONE] PDF created: OpenCV_Practicals_Submission.pdf")
