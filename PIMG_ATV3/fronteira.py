import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def erosao(image, elemEstruturante):
    # executando a erosão binária de uma imagem c/ o elemento estruturante
    m, n = elemEstruturante.shape
    
    # definindo a origem do elemento estruturante (assumindo como centro)
    origem_m, origem_n = m // 2, n // 2

    # preenchendo as bordas com zero para tratar os limites da imagem
    pad_top = origem_m
    pad_bottom = m - origem_m - 1
    pad_left = origem_n
    pad_right = n - origem_n - 1
    padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant', constant_values=0)
    
    img_erodida = np.zeros_like(image)
    
    # varrendo cada pixel da imagem original
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # extraindo a região vizinha de tamanho igual ao do elemEstruturante
            regiao = padded[i:i + m, j:j + n]
            # verifica se, para os pixels onde o elemento estruturante é 1,
            # a região também contém 1 em todos esses pontos.
            if np.all(regiao[elemEstruturante == 1]):
                img_erodida[i, j] = 1
    return img_erodida

def dilatacao(image, elemEstruturante):
    elemEstLinhas = len(elemEstruturante)
    elemEstColunas = len(elemEstruturante[0]) if elemEstLinhas > 0 else 0
    linhaOrigem = elemEstLinhas // 2  # definindo centro do elem Estruturante
    colunaOrigem = elemEstColunas // 2
    img_linhas = len(image)
    img_colunas = len(image[0]) if img_linhas > 0 else 0
    
    # cria umsss matriz preenchida com 0s
    result = np.zeros_like(image)
    
    # percorrendo a img
    for i in range(img_linhas):
        for j in range(img_colunas):
            # Só processa pixels ativos na img original
            if image[i][j] == 1:
                # aplicando o elemest
                for di in range(elemEstLinhas):
                    for dj in range(elemEstColunas):
                        if elemEstruturante[di][dj] == 1:
                            ni = i - linhaOrigem + di
                            nj = j - colunaOrigem + dj
                            # limite da img
                            if 0 <= ni < img_linhas and 0 <= nj < img_colunas:
                                result[ni][nj] = 1
    return result

b = np.ones((3, 3)).astype('uint8')
elemEstruturanteA = np.array([[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]], dtype=np.uint8)

def fronteira(img, b):
    img_fronteira = img.copy()
    img_fronteira = img - erosao(img, b)
    return img_fronteira
    
    

image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)

img_aberta = dilatacao(erosao(img_binaria, elemEstruturanteA), elemEstruturanteA)
img_fechada = erosao(dilatacao(img_aberta, elemEstruturanteA), elemEstruturanteA)
img_fronteira = fronteira(img_fechada, elemEstruturanteA)
plt.figure()
plt.imshow(img_fronteira, cmap='gray')
plt.title('Imagem fronteira')
plt.show()