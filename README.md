# OpenCV Module — Practical Implementations

---

## Project Structure

```
opencv_project/
│
├── practical1_read_image.py        ← Practical 1 : Reading, Displaying & Saving Images
├── practical2_drawing.py           ← Practical 2 : Basic Drawing Operations
├── practical3_colorspaces.py       ← Practical 3 : Color Space Conversions
├── practical4_transformations.py   ← Practical 4 : Geometric Transformations
├── practical5_blurring.py          ← Practical 5 : Image Blurring & Smoothing
├── practical6_thresholding.py      ← Practical 6 : Image Thresholding
├── practical7_edge_detection.py    ← Practical 7 : Edge Detection
├── practical8_contours.py          ← Practical 8 : Contour Detection & Analysis
├── practical9_histograms.py        ← Practical 9 : Histograms & Equalization
├── practical10_morphology.py       ← Practical 10: Morphological Operations
├── practical11_bitwise.py          ← Practical 11: Arithmetic & Bitwise Operations
├── practical12_template_matching.py← Practical 12: Template Matching
├── practical13_color_segmentation.py← Practical 13: Color-based Segmentation
├── practical14_feature_detection.py← Practical 14: Feature Detection & Description
├── practical15_image_pyramids.py   ← Practical 15: Image Pyramids & Optical Flow
│
├── build_pdf.py                    ← Builds submission PDF Part 1 (Practicals 1–9)
├── build_pdf2.py                   ← Builds submission PDF Part 2 (Practicals 10–15)
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
│
└── outputs/                        ← All generated images (created on first run)
    ├── base_image.png
    ├── p1_saved_jpg.jpg
    ├── p1_saved_png.png
    ├── p2_drawing.png
    ├── p3_colorspaces.png
    ├── p3_channels.png
    ├── p4_transformations.png
    ├── p5_blurring.png
    ├── p6_thresholding.png
    ├── p7_edge_detection.png
    ├── p8_contours.png
    ├── p9_histograms.png
    ├── p10_morphology.png
    ├── p11_arithmetic.png
    ├── p11_bitwise.png
    ├── p11_masked.png
    ├── p12_methods.png
    ├── p12_template.png
    ├── p13_segmentation.png
    ├── p14_features.png
    ├── p14_matching.png
    └── p15_pyramids_flow.png
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## How to Run

Run each practical individually:
```bash
python practical1_read_image.py
python practical2_drawing.py
python practical3_colorspaces.py
# ... and so on up to practical15
```

Or run all at once:
```bash
for i in $(seq 1 15); do python practical${i}_*.py; done
```

Generate the submission PDFs:
```bash
python build_pdf.py    # Part 1 — Practicals 1–9
python build_pdf2.py   # Part 2 — Practicals 10–15
```

---

## Practicals Summary

| # | Topic | Key cv2 Functions |
|---|---|---|
| 1 | Reading, Displaying & Saving | imread, imwrite, shape, dtype |
| 2 | Basic Drawing | line, rectangle, circle, ellipse, fillPoly, putText |
| 3 | Color Spaces | cvtColor, split, BGR/Gray/HSV/LAB |
| 4 | Geometric Transformations | resize, flip, warpAffine, warpPerspective |
| 5 | Blurring & Smoothing | blur, GaussianBlur, medianBlur, bilateralFilter |
| 6 | Thresholding | threshold, THRESH_OTSU, adaptiveThreshold |
| 7 | Edge Detection | Sobel, Laplacian, Scharr, Canny |
| 8 | Contours | findContours, drawContours, moments, convexHull |
| 9 | Histograms | calcHist, equalizeHist, CLAHE |
| 10 | Morphology | erode, dilate, morphologyEx |
| 11 | Arithmetic & Bitwise | add, subtract, addWeighted, bitwise_and/or/xor/not |
| 12 | Template Matching | matchTemplate (6 methods), minMaxLoc |
| 13 | Color Segmentation | inRange, HSV masking, GrabCut |
| 14 | Feature Detection | Harris, Shi-Tomasi, FAST, ORB, BFMatcher |
| 15 | Pyramids & Optical Flow | pyrDown/Up, calcOpticalFlowPyrLK, Farneback |

---

## Requirements

- Python 3.10+
- opencv-python-headless >= 4.0
- numpy >= 1.21
- Pillow >= 9.0
- reportlab >= 3.6 (for PDF generation only)
