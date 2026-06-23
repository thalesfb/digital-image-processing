import nbformat as nbf
import os
from pathlib import Path

# Certifique-se de que o nbformat está usando a versão 4
nb = nbf.v4.new_notebook()

# Células iniciais
cells = []

# Header
cells.append(nbf.v4.new_markdown_cell("# Aula 6 - Operações de Filtragem\n\nNesta aula, exploraremos métodos no domínio espacial, utilizando convolução e operações pontuais para filtros passa-baixa, passa-alta e ajustes de histograma/brilho."))

# Imports e Setup
code_setup = """import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuração de caminhos
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def show_image(title, img, cmap='gray'):
    plt.figure(figsize=(8, 6))
    if len(img.shape) == 3:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap=cmap)
    plt.title(title)
    plt.axis('off')
    plt.show()"""
cells.append(nbf.v4.new_code_cell(code_setup))

# Experimento 1
cells.append(nbf.v4.new_markdown_cell("### Experimento 1\nCarregue as imagens `mask.jpeg` e `live.jpeg`, calcule a diferença absoluta entre elas. Na imagem resultante aplique equalização de histograma."))
code_exp1 = """# Carregar imagens em tons de cinza
mask_img = cv2.imread(str(INPUT_DIR / "mask.jpeg"), cv2.IMREAD_GRAYSCALE)
live_img = cv2.imread(str(INPUT_DIR / "live.jpeg"), cv2.IMREAD_GRAYSCALE)

# Diferença absoluta
diff_img = cv2.absdiff(mask_img, live_img)

# Equalização de histograma
eq_img = cv2.equalizeHist(diff_img)

# Exibição
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(diff_img, cmap='gray'); axes[0].set_title('Diferença Absoluta'); axes[0].axis('off')
axes[1].imshow(eq_img, cmap='gray'); axes[1].set_title('Equalizado'); axes[1].axis('off')

# Salvar output
cv2.imwrite(str(OUTPUT_DIR / "exp1_diff_eq.jpeg"), eq_img)
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_exp1))

# Experimento 2
cells.append(nbf.v4.new_markdown_cell("### Experimento 2\nCarregue as imagens `mask1.png` e `mask2.png`. Responda: as imagens são iguais? Calcule a diferença entre elas."))
code_exp2 = """mask1 = cv2.imread(str(INPUT_DIR / "mask1.png"))
mask2 = cv2.imread(str(INPUT_DIR / "mask2.png"))

# Verificando se são iguais
sao_iguais = np.array_equal(mask1, mask2)
print("As imagens mask1 e mask2 são iguais?", "Sim" if sao_iguais else "Não")

# Diferença
diff_masks = cv2.absdiff(mask1, mask2)
show_image("Diferença mask1 e mask2", diff_masks)
cv2.imwrite(str(OUTPUT_DIR / "exp2_diff.png"), diff_masks)"""
cells.append(nbf.v4.new_code_cell(code_exp2))
cells.append(nbf.v4.new_markdown_cell("**Respostas:**\n- As imagens são iguais? (Preencha aqui com base na saída do código)"))

# Experimento 3
cells.append(nbf.v4.new_markdown_cell("### Experimento 3\nCarregue as imagens `pcbCropped.png` e `pcbCroppedTranslatedDefected.png`. Elas são iguais? Calcule a diferença entre elas."))
code_exp3 = """pcb1 = cv2.imread(str(INPUT_DIR / "pcbCropped.png"))
pcb2 = cv2.imread(str(INPUT_DIR / "pcbCroppedTranslatedDefected.png"))

sao_iguais_pcb = np.array_equal(pcb1, pcb2)
print("As imagens do PCB são iguais?", "Sim" if sao_iguais_pcb else "Não")

diff_pcb = cv2.absdiff(pcb1, pcb2)
show_image("Diferença PCB", diff_pcb)
cv2.imwrite(str(OUTPUT_DIR / "exp3_diff_pcb.png"), diff_pcb)"""
cells.append(nbf.v4.new_code_cell(code_exp3))
cells.append(nbf.v4.new_markdown_cell("**Respostas:**\n- As imagens são iguais? (Preencha aqui)"))

# Experimento 4
cells.append(nbf.v4.new_markdown_cell("### Experimento 4\nCarregue a imagem `parrot.jpeg`. Aplique um ajuste de brilho (multiplique por um fator de 1.2) e plote as duas imagens."))
code_exp4 = """parrot = cv2.imread(str(INPUT_DIR / "parrot.jpeg"))
parrot_rgb = cv2.cvtColor(parrot, cv2.COLOR_BGR2RGB)

# Multiplicar por 1.2 usando convertScaleAbs para evitar overflow (>255)
parrot_brighter = cv2.convertScaleAbs(parrot_rgb, alpha=1.2, beta=0)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(parrot_rgb); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(parrot_brighter); axes[1].set_title('Brilho x1.2'); axes[1].axis('off')
plt.show()

# Salvar output em BGR
cv2.imwrite(str(OUTPUT_DIR / "exp4_parrot_brighter.jpeg"), cv2.cvtColor(parrot_brighter, cv2.COLOR_RGB2BGR))"""
cells.append(nbf.v4.new_code_cell(code_exp4))

# Experimento 5
cells.append(nbf.v4.new_markdown_cell("### Experimento 5\nAplique ajuste gamma (potência) com um fator 1.5 na imagem `parrot.jpeg`. Plote as duas imagens."))
code_exp5 = """gamma = 1.5
inv_gamma = 1.0 / gamma

# Criação de Look-Up Table (LUT) para otimização
table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
parrot_gamma = cv2.LUT(parrot_rgb, table)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(parrot_rgb); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(parrot_gamma); axes[1].set_title(f'Gamma {gamma}'); axes[1].axis('off')
plt.show()

cv2.imwrite(str(OUTPUT_DIR / "exp5_parrot_gamma.jpeg"), cv2.cvtColor(parrot_gamma, cv2.COLOR_RGB2BGR))"""
cells.append(nbf.v4.new_code_cell(code_exp5))

# Experimento 6
cells.append(nbf.v4.new_markdown_cell("### Experimento 6\nCarregue `bay.jpeg`, `brain.jpeg` e `moon.jpeg`. Execute equalização de histograma global, plote as imagens originais/modificadas e os respectivos histogramas."))
code_exp6 = """imagens = ['bay.jpeg', 'brain.jpeg', 'moon.jpeg']

for img_name in imagens:
    img = cv2.imread(str(INPUT_DIR / img_name), cv2.IMREAD_GRAYSCALE)
    img_eq = cv2.equalizeHist(img)
    
    # Calcular histogramas
    hist_orig = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_eq = cv2.calcHist([img_eq], [0], None, [256], [0, 256])
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Imagem: {img_name}', fontsize=16)
    
    axes[0, 0].imshow(img, cmap='gray'); axes[0, 0].set_title('Original'); axes[0, 0].axis('off')
    axes[0, 1].imshow(img_eq, cmap='gray'); axes[0, 1].set_title('Equalizada'); axes[0, 1].axis('off')
    
    axes[1, 0].plot(hist_orig, color='black'); axes[1, 0].set_title('Histograma Original'); axes[1, 0].set_xlim([0, 256])
    axes[1, 1].plot(hist_eq, color='black'); axes[1, 1].set_title('Histograma Equalizado'); axes[1, 1].set_xlim([0, 256])
    
    plt.tight_layout()
    plt.show()
    
    cv2.imwrite(str(OUTPUT_DIR / f"exp6_eq_{img_name}"), img_eq)"""
cells.append(nbf.v4.new_code_cell(code_exp6))

# Experimento 7
cells.append(nbf.v4.new_markdown_cell("### Experimento 7\nPesquise como utilizar equalização de histograma adaptativa (CLAHE) e aplique em: `dental.jpeg`, `parrot.jpeg` e `skull.jpeg`."))
code_exp7 = """imagens_clahe = ['dental.jpeg', 'parrot.jpeg', 'skull.jpeg']

# Instanciar CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

for img_name in imagens_clahe:
    img = cv2.imread(str(INPUT_DIR / img_name), cv2.IMREAD_GRAYSCALE)
    img_clahe = clahe.apply(img)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(img, cmap='gray'); axes[0].set_title(f'Original: {img_name}'); axes[0].axis('off')
    axes[1].imshow(img_clahe, cmap='gray'); axes[1].set_title('CLAHE'); axes[1].axis('off')
    plt.show()
    
    cv2.imwrite(str(OUTPUT_DIR / f"exp7_clahe_{img_name}"), img_clahe)"""
cells.append(nbf.v4.new_code_cell(code_exp7))

# Experimento 8
cells.append(nbf.v4.new_markdown_cell("### Experimento 8\nUse um filtro passa-baixa e um detector de bordas (Canny) na imagem `croppedBike.png`."))
code_exp8 = """bike = cv2.imread(str(INPUT_DIR / "croppedBike.png"), cv2.IMREAD_GRAYSCALE)

# Sem filtro
edges_raw = cv2.Canny(bike, 100, 200)

# Com filtro Gaussiano passa-baixa (suavização)
bike_blurred = cv2.GaussianBlur(bike, (5, 5), 0)
edges_blurred = cv2.Canny(bike_blurred, 100, 200)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(bike, cmap='gray'); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(edges_raw, cmap='gray'); axes[1].set_title('Canny (Sem Filtro)'); axes[1].axis('off')
axes[2].imshow(edges_blurred, cmap='gray'); axes[2].set_title('Canny (Com Filtro Gaussiano)'); axes[2].axis('off')
plt.show()

cv2.imwrite(str(OUTPUT_DIR / "exp8_bike_edges.png"), edges_blurred)"""
cells.append(nbf.v4.new_code_cell(code_exp8))

# Experimento 9
cells.append(nbf.v4.new_markdown_cell("### Experimento 9\nAplique um filtro para remover o ruído de `noise.png`. Faça o experimento com diferentes tamanhos de kernel (3x3, 5x5)."))
code_exp9 = """noise_img = cv2.imread(str(INPUT_DIR / "noise.png"))
noise_img_rgb = cv2.cvtColor(noise_img, cv2.COLOR_BGR2RGB)

# O ruído Sal e Pimenta é melhor removido pelo filtro Mediano
median_3x3 = cv2.medianBlur(noise_img_rgb, 3)
median_5x5 = cv2.medianBlur(noise_img_rgb, 5)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(noise_img_rgb); axes[0].set_title('Original com Ruído'); axes[0].axis('off')
axes[1].imshow(median_3x3); axes[1].set_title('Filtro Mediano 3x3'); axes[1].axis('off')
axes[2].imshow(median_5x5); axes[2].set_title('Filtro Mediano 5x5'); axes[2].axis('off')
plt.show()

cv2.imwrite(str(OUTPUT_DIR / "exp9_noise_removed.png"), cv2.cvtColor(median_5x5, cv2.COLOR_RGB2BGR))"""
cells.append(nbf.v4.new_code_cell(code_exp9))

# Experimento 10
cells.append(nbf.v4.new_markdown_cell("### Experimento 10\nAplique um filtro para melhorar a nitidez de `blur.webp` (Máscara de Nitidez / Unsharp Masking)."))
code_exp10 = """blur_img = cv2.imread(str(INPUT_DIR / "blur.webp"))
blur_img_rgb = cv2.cvtColor(blur_img, cv2.COLOR_BGR2RGB)

# Unsharp Masking: Imagem Original + (Original - Suavizada) * alpha
gaussian_blur = cv2.GaussianBlur(blur_img_rgb, (9, 9), 10.0)
sharpened = cv2.addWeighted(blur_img_rgb, 1.5, gaussian_blur, -0.5, 0)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(blur_img_rgb); axes[0].set_title('Desfocada (Original)'); axes[0].axis('off')
axes[1].imshow(sharpened); axes[1].set_title('Nitidez (Unsharp Masking)'); axes[1].axis('off')
plt.show()

cv2.imwrite(str(OUTPUT_DIR / "exp10_sharpened.png"), cv2.cvtColor(sharpened, cv2.COLOR_RGB2BGR))"""
cells.append(nbf.v4.new_code_cell(code_exp10))

# Experimento 11
cells.append(nbf.v4.new_markdown_cell("### Experimento 11\nAplique um filtro para extrair as bordas da imagem do exercício anterior (antes e depois da nitidez)."))
code_exp11 = """blur_gray = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
sharpened_gray = cv2.cvtColor(cv2.cvtColor(sharpened, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2GRAY)

edges_before = cv2.Canny(blur_gray, 50, 150)
edges_after = cv2.Canny(sharpened_gray, 50, 150)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(edges_before, cmap='gray'); axes[0].set_title('Bordas ANTES da nitidez'); axes[0].axis('off')
axes[1].imshow(edges_after, cmap='gray'); axes[1].set_title('Bordas DEPOIS da nitidez'); axes[1].axis('off')
plt.show()

cv2.imwrite(str(OUTPUT_DIR / "exp11_edges_after.png"), edges_after)"""
cells.append(nbf.v4.new_code_cell(code_exp11))

nb['cells'] = cells

output_path = Path("experiment/Aula 6/notebook.ipynb")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook gerado em {output_path}")
