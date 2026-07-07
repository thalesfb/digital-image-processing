import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
base_dir = Path(r"c:\dev\digital-image-processing")
input_dir = base_dir / "docs" / "avaliacao" / "data" / "input"
output_dir = base_dir / "docs" / "avaliacao" / "data" / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# QUESTÃO 1: RGB, Escala de Cinza e HSL
# -------------------------------------------------------------
print("Processando Questão 1...")
img1_path = input_dir / "parrot.jpeg"
img1_bgr = cv2.imread(str(img1_path))

img1_rgb = cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2RGB)
img1_gray = cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2GRAY)
img1_hsl = cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2HLS)

# Plot side-by-side
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img1_rgb)
axes[0].set_title("RGB (True Color)")
axes[0].axis("off")

axes[1].imshow(img1_gray, cmap="gray")
axes[1].set_title("Escala de Cinza")
axes[1].axis("off")

axes[2].imshow(img1_hsl)
axes[2].set_title("HSL (Visualizado como RGB)")
axes[2].axis("off")

plt.tight_layout()
plt.savefig(output_dir / "q1_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 2: pout.tiff (Melhoria de Contraste)
# -------------------------------------------------------------
print("Processando Questão 2...")
img2_path = input_dir / "pout.tif"
img2 = cv2.imread(str(img2_path), cv2.IMREAD_GRAYSCALE)

# Global Equalization
img2_eq = cv2.equalizeHist(img2)

# CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
img2_clahe = clahe.apply(img2)

# Plot side-by-side with histograms
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Images
axes[0, 0].imshow(img2, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Original (pout.tif)")
axes[0, 0].axis("off")

axes[0, 1].imshow(img2_eq, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title("Equalização Global")
axes[0, 1].axis("off")

axes[0, 2].imshow(img2_clahe, cmap="gray", vmin=0, vmax=255)
axes[0, 2].set_title("CLAHE (Adaptativo)")
axes[0, 2].axis("off")

# Histograms
axes[1, 0].hist(img2.ravel(), bins=256, range=[0, 256], color="black", histtype="step")
axes[1, 0].set_title("Histograma Original")
axes[1, 0].set_xlim([0, 256])

axes[1, 1].hist(img2_eq.ravel(), bins=256, range=[0, 256], color="blue", histtype="step")
axes[1, 1].set_title("Hist. Equalizado Global")
axes[1, 1].set_xlim([0, 256])

axes[1, 2].hist(img2_clahe.ravel(), bins=256, range=[0, 256], color="red", histtype="step")
axes[1, 2].set_title("Hist. CLAHE")
axes[1, 2].set_xlim([0, 256])

plt.tight_layout()
plt.savefig(output_dir / "q2_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 3: ifc_vda.jpeg (Normalização do Histograma)
# -------------------------------------------------------------
print("Processando Questão 3...")
img3_path = input_dir / "ifc_vda.jpeg"
img3 = cv2.imread(str(img3_path), cv2.IMREAD_GRAYSCALE)

# Normalize MinMax
img3_norm = cv2.normalize(img3, None, 0, 255, cv2.NORM_MINMAX)

# Plot side-by-side with histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Images
axes[0, 0].imshow(img3, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Original (ifc_vda.jpeg)")
axes[0, 0].axis("off")

axes[0, 1].imshow(img3_norm, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title("Normalizada (MinMax Stretch)")
axes[0, 1].axis("off")

# Histograms
axes[1, 0].hist(img3.ravel(), bins=256, range=[0, 256], color="black", histtype="step")
axes[1, 0].set_title("Histograma Original")
axes[1, 0].set_xlim([0, 256])

axes[1, 1].hist(img3_norm.ravel(), bins=256, range=[0, 256], color="green", histtype="step")
axes[1, 1].set_title("Histograma Normalizado")
axes[1, 1].set_xlim([0, 256])

plt.tight_layout()
plt.savefig(output_dir / "q3_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 4: Limiarização Linear (Thresholding)
# -------------------------------------------------------------
print("Processando Questão 4...")
# We use moon.jpeg as the grayscale target
img4_path = input_dir / "moon.jpeg"
img4 = cv2.imread(str(img4_path), cv2.IMREAD_GRAYSCALE)

# Fixed thresholding at 100
threshold_value = 100
_, img4_bin = cv2.threshold(img4, threshold_value, 255, cv2.THRESH_BINARY)

# Plot side-by-side with histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Images
axes[0, 0].imshow(img4, cmap="gray", vmin=0, vmax=255)
axes[0, 0].set_title("Original (moon.jpeg)")
axes[0, 0].axis("off")

axes[0, 1].imshow(img4_bin, cmap="gray", vmin=0, vmax=255)
axes[0, 1].set_title(f"Limiarizada (Threshold = {threshold_value})")
axes[0, 1].axis("off")

# Histograms
axes[1, 0].hist(img4.ravel(), bins=256, range=[0, 256], color="black", histtype="step")
axes[1, 0].set_title("Histograma de Entrada")
axes[1, 0].set_xlim([0, 256])

# Binarized image histogram (mostly 0 and 255)
axes[1, 1].hist(img4_bin.ravel(), bins=256, range=[0, 256], color="purple", histtype="step")
axes[1, 1].set_title("Histograma Resultante (Binarizado)")
axes[1, 1].set_xlim([0, 256])

plt.tight_layout()
plt.savefig(output_dir / "q4_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 5: Operação lógica AND
# -------------------------------------------------------------
print("Processando Questão 5...")
img5a_path = input_dir / "ifc_01.png"
img5b_path = input_dir / "ifc_02.png"

img5a = cv2.imread(str(img5a_path), cv2.IMREAD_GRAYSCALE)
img5b = cv2.imread(str(img5b_path), cv2.IMREAD_GRAYSCALE)

# Ensure same dimensions
if img5a.shape != img5b.shape:
    img5b = cv2.resize(img5b, (img5a.shape[1], img5a.shape[0]))

img5_and = cv2.bitwise_and(img5a, img5b)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img5a, cmap="gray")
axes[0].set_title("ifc_01.png")
axes[0].axis("off")

axes[1].imshow(img5b, cmap="gray")
axes[1].set_title("ifc_02.png")
axes[1].axis("off")

axes[2].imshow(img5_and, cmap="gray")
axes[2].set_title("Resultado AND")
axes[2].axis("off")

plt.tight_layout()
plt.savefig(output_dir / "q5_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 6: Comparação mask1.png e mask2.png
# -------------------------------------------------------------
print("Processando Questão 6...")
img6a_path = input_dir / "mask1.png"
img6b_path = input_dir / "mask2.png"

img6a = cv2.imread(str(img6a_path), cv2.IMREAD_GRAYSCALE)
img6b = cv2.imread(str(img6b_path), cv2.IMREAD_GRAYSCALE)

# Are they exactly equal?
are_equal = np.array_equal(img6a, img6b)
print(f"  As imagens mask1.png e mask2.png são idênticas? {are_equal}")

# Calculate absolute difference
img6_diff = cv2.absdiff(img6a, img6b)
diff_pixels = np.sum(img6_diff > 0)
print(f"  Número de pixels diferentes: {diff_pixels}")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img6a, cmap="gray")
axes[0].set_title("mask1.png")
axes[0].axis("off")

axes[1].imshow(img6b, cmap="gray")
axes[1].set_title("mask2.png")
axes[1].axis("off")

# To make the difference highly visible, we can amplify it or show as is
axes[2].imshow(img6_diff, cmap="hot")
axes[2].set_title(f"Diferença Absoluta ({diff_pixels} px dif)")
axes[2].axis("off")

plt.tight_layout()
plt.savefig(output_dir / "q6_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 7: Filtro para eliminar ruído de placa_noisy
# -------------------------------------------------------------
print("Processando Questão 7...")
img7_path = input_dir / "hw3_license_plate_noisy.png"
img7 = cv2.imread(str(img7_path), cv2.IMREAD_GRAYSCALE)

# Apply filters
img7_gaussian = cv2.GaussianBlur(img7, (5, 5), 0)
img7_median = cv2.medianBlur(img7, 5)
img7_bilateral = cv2.bilateralFilter(img7, 9, 75, 75)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].imshow(img7, cmap="gray")
axes[0, 0].set_title("Com Ruído Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(img7_gaussian, cmap="gray")
axes[0, 1].set_title("Filtro Gaussiano (5x5)")
axes[0, 1].axis("off")

axes[1, 0].imshow(img7_median, cmap="gray")
axes[1, 0].set_title("Filtro Mediano (5x5) - RECOMENDADO")
axes[1, 0].axis("off")

axes[1, 1].imshow(img7_bilateral, cmap="gray")
axes[1, 1].set_title("Filtro Bilateral")
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig(output_dir / "q7_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 8: Limpeza de ruído e morfologia em placa.png
# -------------------------------------------------------------
print("Processando Questão 8...")
img8_path = input_dir / "placa.png"
img8_bgr = cv2.imread(str(img8_path))
img8_gray = cv2.cvtColor(img8_bgr, cv2.COLOR_BGR2GRAY)

# b. Suavização Gaussiana
img8_blur = cv2.GaussianBlur(img8_gray, (5, 5), 0)

# c. Binarização Otsu (invertida para que os caracteres fiquem brancos em fundo preto)
_, img8_thresh = cv2.threshold(img8_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# d. Operações morfológicas
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
img8_dil = cv2.dilate(img8_thresh, kernel, iterations=1)
img8_ero = cv2.erode(img8_thresh, kernel, iterations=1)
img8_open = cv2.morphologyEx(img8_thresh, cv2.MORPH_OPEN, kernel)
img8_close = cv2.morphologyEx(img8_thresh, cv2.MORPH_CLOSE, kernel)

# Plot comparison
fig, axes = plt.subplots(3, 2, figsize=(12, 15))
axes[0, 0].imshow(img8_gray, cmap="gray")
axes[0, 0].set_title("Original (Escala de Cinza)")
axes[0, 0].axis("off")

axes[0, 1].imshow(img8_thresh, cmap="gray")
axes[0, 1].set_title("Binarização Otsu Invertida")
axes[0, 1].axis("off")

axes[1, 0].imshow(img8_dil, cmap="gray")
axes[1, 0].set_title("Dilatação (3x3)")
axes[1, 0].axis("off")

axes[1, 1].imshow(img8_ero, cmap="gray")
axes[1, 1].set_title("Erosão (3x3)")
axes[1, 1].axis("off")

axes[2, 0].imshow(img8_open, cmap="gray")
axes[2, 0].set_title("Abertura (Remove ruídos externos)")
axes[2, 0].axis("off")

axes[2, 1].imshow(img8_close, cmap="gray")
axes[2, 1].set_title("Fechamento (Preenche buracos internos)")
axes[2, 1].axis("off")

plt.tight_layout()
plt.savefig(output_dir / "q8_result.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# QUESTÃO 9: Detecção de cones em hw2_cone.jpg
# -------------------------------------------------------------
print("Processando Questão 9...")
img9_path = input_dir / "hw2_cone.jpg"
img9_bgr = cv2.imread(str(img9_path))
img9_rgb = cv2.cvtColor(img9_bgr, cv2.COLOR_BGR2RGB)

# Convert to HLS (HSL equivalent in OpenCV)
img9_hls = cv2.cvtColor(img9_bgr, cv2.COLOR_BGR2HLS)

# Define range for orange color in HLS
lower_orange1 = np.array([3, 40, 100])
upper_orange1 = np.array([18, 220, 255])
# Secondary orange range (for wrapping around 180, if any)
lower_orange2 = np.array([170, 40, 100])
upper_orange2 = np.array([180, 220, 255])

mask1 = cv2.inRange(img9_hls, lower_orange1, upper_orange1)
mask2 = cv2.inRange(img9_hls, lower_orange2, upper_orange2)
orange_mask = mask1 | mask2

# Apply morphological closing and opening to clean mask
kernel_cone = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
orange_mask_clean = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel_cone)
orange_mask_clean = cv2.morphologyEx(orange_mask_clean, cv2.MORPH_OPEN, kernel_cone)

# Find contours
contours, _ = cv2.findContours(orange_mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img9_out = img9_rgb.copy()

cones_detected = 0
for c in contours:
    area = cv2.contourArea(c)
    # Filter by area size to avoid noise
    if 100 < area < 10000:
        x, y, w, h = cv2.boundingRect(c)
        # Check aspect ratio to ensure it fits a cone (normally tall or square-ish, not super flat)
        aspect_ratio = float(w) / h
        # Cones are slender: aspect ratio of width/height <= 0.60, located in the lower road region
        if aspect_ratio <= 0.60 and y > 250:
            cv2.rectangle(img9_out, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cones_detected += 1

print(f"  Detecção de Cones: {cones_detected} cones encontrados.")

fig, axes = plt.subplots(1, 2, figsize=(15, 8))
axes[0].imshow(img9_rgb)
axes[0].set_title("Imagem Original")
axes[0].axis("off")

axes[1].imshow(img9_out)
axes[1].set_title(f"Cones Detectados (Retângulo Verde: {cones_detected})")
axes[1].axis("off")

plt.tight_layout()
plt.savefig(output_dir / "q9_result.png", dpi=150)
plt.close()

print("Processamento concluído com sucesso!")
