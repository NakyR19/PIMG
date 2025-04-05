import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def erosao(image, elemEstruturante):
    m, n = elemEstruturante.shape
    origin_m, origin_n = m // 2, n // 2
    pad_top = origin_m
    pad_bottom = m - origin_m - 1
    pad_left = origin_n
    pad_right = n - origin_n - 1
    padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant', constant_values=0)
    img_erodida = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            regiao = padded[i:i + m, j:j + n]
            if np.all(regiao[elemEstruturante == 1]):
                img_erodida[i, j] = 1
    return img_erodida

def dilatacao(image, elemEstruturante):
    elemEstLinhas = len(elemEstruturante)
    elemEstColunas = len(elemEstruturante[0]) if elemEstLinhas > 0 else 0
    linhaOrigem = elemEstLinhas // 2
    colunaOrigem = elemEstColunas // 2
    img_rows = len(image)
    img_cols = len(image[0]) if img_rows > 0 else 0
    result = np.zeros_like(image)
    for i in range(img_rows):
        for j in range(img_cols):
            if image[i][j] == 1:
                for di in range(elemEstLinhas):
                    for dj in range(elemEstColunas):
                        if elemEstruturante[di][dj] == 1:
                            ni = i - linhaOrigem + di
                            nj = j - colunaOrigem + dj
                            if 0 <= ni < img_rows and 0 <= nj < img_cols:
                                result[ni][nj] = 1
    return result

def hit_or_miss(a, x, w):
    p1 = erosao(a, x)
    p2 = erosao((1 - a), w)
    return p1 * p2

def skeletonize(binary_image):
    structuring_elements = [
        # Fase 1
        (np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8),
         np.array([[1, 1, 1], [0, 1, 0], [0, 1, 0]], dtype=np.uint8)),
        # Fase 2
        (np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype=np.uint8),
         np.array([[1, 1, 1], [0, 1, 0], [0, 1, 0]], dtype=np.uint8)),
    ]
    
    skeleton = binary_image.copy().astype(np.uint8)
    previous = np.zeros_like(skeleton)
    
    # Iterar até não haver mais mudanças
    iteration = 0
    while not np.array_equal(skeleton, previous) and iteration < 100:
        previous = skeleton.copy()
        
        # Duas fases para o algoritmo
        for phase in range(2):
            for se in structuring_elements:
                hit = hit_or_miss(skeleton, se[0], se[1])
                skeleton = skeleton - hit
                skeleton = np.clip(skeleton, 0, 1)
        
        iteration += 1
    
    return skeleton

# Carregar a imagem
image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)
plt.figure()
plt.imshow(img_binaria, cmap='gray')
plt.title('Imagem Original')

# Abertura
b = np.ones((3, 3)).astype('uint8')
img_op = dilatacao(erosao(img_binaria, b), b)
plt.figure()
plt.imshow(img_op, cmap='gray')
plt.title('Imagem Após Abertura')

# Aplicar esqueletização
skeleton = skeletonize(img_binaria)
plt.figure()
plt.imshow(skeleton, cmap='gray')
plt.title('Imagem Esqueletizada')

# Salvar resultados
Image.fromarray(skeleton * 255).save('skeleton.png')

# Mostrar todas as figuras
plt.show()

print("CHEGOU")
skeleton = skeletonize(img_binaria)
# Salvar resultados
Image.fromarray(skeleton * 255).save('skeleton.png')
print("passou")