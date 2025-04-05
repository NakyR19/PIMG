import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def erosao(image, elemEstruturante):
    m, n = elemEstruturante.shape
    origem_m, origem_n = m // 2, n // 2

    pad_top = origem_m
    pad_bottom = m - origem_m - 1
    pad_left = origem_n
    pad_right = n - origem_n - 1
    padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant', constant_values=0)
    
    img_erodida = np.zeros_like(image)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            regiao = padded[i:i + m, j:j + n]
            if np.all(regiao[elemEstruturante == 1]):
                img_erodida[i, j] = 1
    return img_erodida

def dilatacao(image, elemEstruturante):
    m, n = elemEstruturante.shape
    origem_m, origem_n = m // 2, n // 2
    
    padded = np.pad(image, ((origem_m, origem_m), (origem_n, origem_n)), mode='constant', constant_values=0)
    result = np.zeros_like(image)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 1:
                for di in range(m):
                    for dj in range(n):
                        if elemEstruturante[di, dj] == 1:
                            ni = i - origem_m + di
                            nj = j - origem_n + dj
                            if 0 <= ni < image.shape[0] and 0 <= nj < image.shape[1]:
                                result[ni, nj] = 1
    return result

def abertura(img, B):
    return dilatacao(erosao(img, B), B)

def gerar_kB(B, k):
    kB = B.copy()
    for _ in range(k):
        kB = dilatacao(kB, B)
    return kB

def esqueletizacao(imagem, B):
    esqueleto = np.zeros_like(imagem)
    k = 0
    
    print("Esqueletizando...")
    while True:
        kB = gerar_kB(B, k)
        Ek = erosao(imagem, kB)
        
        if not np.any(Ek):
            break
            
        Ok = abertura(Ek, B)
        Dk = np.logical_and(Ek, np.logical_not(Ok)).astype(np.uint8)
        
        esqueleto = np.logical_or(esqueleto, Dk).astype(np.uint8)
        k += 1
    
    return esqueleto

# Carregar e processar imagem
image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)  # Binarização

B = np.array([[0, 1, 0],
              [1, 1, 1],
              [0, 1, 0]], dtype=np.uint8)

print("entrando")
# Aplicar esqueletização
img_esq = esqueletizacao(img_binaria, B)

print("ola")
# Plotar resultados
plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.imshow(img_binaria, cmap='gray')
plt.title('Imagem Original')

plt.subplot(122)
plt.imshow(img_esq, cmap='gray')
plt.title('Esqueleto')

plt.show()