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

def hit_or_miss(a, x, w):
    p1 = erosao(a, x)
    p2 = erosao((1 - a), w)
    return p1 * p2

def afinamento(img, b):
    aux = img.copy()
    for ee in b:
        aux = aux - hit_or_miss(aux, ee[0], ee[1])
    return aux

image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)
plt.figure()
plt.imshow(img_binaria, cmap='gray')
plt.title('Imagem original')

# Abertura
b = np.ones((3, 3)).astype('uint8')
img_op = dilatacao(erosao(img_binaria, b), b)
plt.figure()
plt.imshow(img_op, cmap='gray')
plt.title('Imagem aberta')

# elementos estruturantes
b1 = np.zeros((3, 3), dtype='uint8')
b1[1, 1] = 1
b1[2, :] = 1
b1c = np.zeros((3, 3), dtype='uint8')
b1c[0, :] = 1
b2 = b1.T
b2c = b1c.T
b3 = b1.copy()
b3[0, :] = 1
b3[2, :] = 0
b3c = b1c.copy()
b3c[0, :] = 0
b3c[2, :] = 1
b4 = b3.T
b4c = b3c.T
b = [[b1, b1c], [b2, b2c], [b3, b3c], [b4, b4c]]

img_afinada = afinamento(img_binaria, b)
plt.figure()
plt.imshow(img_afinada, cmap='gray')
plt.title('Imagem original')


plt.show()



# def esqueletizacao(imagem, B):
#     img_erosao = imagem.copy()
#     esqueleto = np.zeros_like(imagem)
#     for i in range (2):
#         img_erosao = erosao(img_erosao, B)
#         esqueleto = img_erosao - dilatacao(erosao(img_erosao, B), B)
    
#     return esqueleto 