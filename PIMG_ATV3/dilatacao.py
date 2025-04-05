import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def dilatacao(image, elemEstruturante):
    """Realiza a dilatação binária de uma imagem por um elemento estruturante"""
    elemEstLinhas = len(elemEstruturante)
    elemEstColunas = len(elemEstruturante[0]) if elemEstLinhas > 0 else 0
    linhaOrigem = elemEstLinhas // 2  # Centro do elemento estruturante
    colunaOrigem = elemEstColunas // 2
    img_rows = len(image)
    img_cols = len(image[0]) if img_rows > 0 else 0
    
    # Cria matriz de resultado preenchida com 0s
    result = [[0 for _ in range(img_cols)] for _ in range(img_rows)]
    
    # Percorre cada pixel da imagem
    for i in range(img_rows):
        for j in range(img_cols):
            # Só processa pixels ativos na imagem original
            if image[i][j] == 1:
                # Aplica o elemento estruturante
                for di in range(elemEstLinhas):
                    for dj in range(elemEstColunas):
                        if elemEstruturante[di][dj] == 1:
                            # Calcula nova posição
                            ni = i - linhaOrigem + di
                            nj = j - colunaOrigem + dj
                            # Verifica limites da imagem
                            if 0 <= ni < img_rows and 0 <= nj < img_cols:
                                result[ni][nj] = 1
    return result


elemEstruturante = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
], dtype=np.uint8)

image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)

img_dilatada = dilatacao(img_binaria, elemEstruturante)

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(img_binaria, cmap='gray')
plt.title("Imagem Original")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_dilatada, cmap='gray')
plt.title("Imagem Dilatada")
plt.axis('off')

plt.tight_layout()
plt.show()
