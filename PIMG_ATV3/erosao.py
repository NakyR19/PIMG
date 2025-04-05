import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def erosao(image, elemEstruturante):
    
    # executando a erosão binária de uma imagem c/ o elemento estruturante
    
    m, n = elemEstruturante.shape
    
    # definindo a origem do elemento estruturante (assumindo como centro)
    origin_m, origin_n = m // 2, n // 2

    # preenchendo as bordas com zero para tratar os limites da imagem
    pad_top = origin_m
    pad_bottom = m - origin_m - 1
    pad_left = origin_n
    pad_right = n - origin_n - 1
    padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant', constant_values=0)
    
    # Cria a imagem de saída com mesmo tamanho da imagem original
    img_erodida = np.zeros_like(image)
    
    # Varre cada pixel da imagem original
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Extrai a região vizinha de tamanho igual ao do elemEstruturante
            regiao = padded[i:i + m, j:j + n]
            # verifica se, para os pixels onde o elemento estruturante é 1,
            # a região também contém 1 em todos esses pontos.
            if np.all(regiao[elemEstruturante == 1]):
                img_erodida[i, j] = 1
    return img_erodida

image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)
        
elemEstruturante = np.array([[1, 1, 1],
                  [1, 1, 1],
                  [1, 1, 1]], dtype=np.uint8)

img_erodida = erosao(img_binaria, elemEstruturante)

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(img_binaria, cmap='gray')
plt.title("Imagem Original")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_erodida, cmap='gray')
plt.title("Imagem Erodida")
plt.axis('off')

plt.tight_layout()
plt.show()
