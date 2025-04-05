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


image = Image.open('digital.png').convert('L')
img_array = np.array(image)
img_binaria = (img_array > 128).astype(np.uint8)
plt.figure()
plt.imshow(img_binaria, cmap='gray')
plt.title('Imagem original')

b = np.ones((3, 3)).astype('uint8')
# Erosão
img_erodida = erosao(img_binaria, b)
# Abertura
img_op = dilatacao(erosao(img_erodida, b), b)

i=0
img_esq = np.zeros_like(image)
while (i<1):
    img_esq += img_erodida - img_op
    i+=1
    
plt.figure()
plt.imshow(img_op, cmap='gray')
plt.title('Imagem esqueletizada 1x')

# # elementos estruturantes
# b1 = np.zeros((3, 3), dtype='uint8')
# b1[1, 1] = 1
# b1[2, :] = 1
# b1c = np.zeros((3, 3), dtype='uint8')
# b1c[0, :] = 1
# b2 = b1.T
# b2c = b1c.T
# b3 = b1.copy()
# b3[0, :] = 1
# b3[2, :] = 0
# b3c = b1c.copy()
# b3c[0, :] = 0
# b3c[2, :] = 1
# b4 = b3.T
# b4c = b3c.T
# # conjunto de elementos
# b = [[b1, b1c], [b2, b2c], [b3, b3c], [b4, b4c]]

# aplicando hitormiss
esq = img_op.copy()
for i in range(20):
    for ee in b:
        esq = esq ^ hit_or_miss(esq, ee[0], ee[1])
# plt.figure()
# plt.imshow(esq, cmap='gray')
# plt.title('Img após esqueletização')
# Image.fromarray(esq * 255).save('esqueletizacao.png')

# # FUNÇÃO DE PODA (PRUNING) SEM USAR BIBLIOTECAS EXTERNAS
# def prune_skeleton(skel, i):
#     """
#     Realiza a poda (pruning) removendo iterativamente os endpoints de uma imagem esqueletizada.
#     A imagem 'skel' é uma matriz binária (0 e 1).
    
#     Parâmetros:
#       - skel: imagem esqueletizada (numpy array com 0 e 1)
#       - max_iterations: número máximo de iterações
      
#     Retorna:
#       A imagem podada.
#     """
#     # Obtem as dimensões
#     height, width = skel.shape
#     # Cria uma cópia para trabalhar
#     pruned = skel.copy()
    
#     for iteration in range(i):
#         removidos = False
#         # Cria uma cópia que armazenará as alterações desta iteração
#         nova = pruned.copy()
#         for i in range(height):
#             for j in range(width):
#                 # Processa apenas pixels ativos (1)
#                 if pruned[i, j] == 1:
#                     # Conta os vizinhos em 8-direções
#                     vizinhos = 0
#                     for di in [-1, 0, 1]:
#                         for dj in [-1, 0, 1]:
#                             if di == 0 and dj == 0:
#                                 continue
#                             ni = i + di
#                             nj = j + dj
#                             if 0 <= ni < height and 0 <= nj < width:
#                                 if pruned[ni, nj] == 1:
#                                     vizinhos += 1
#                     # Se o pixel tiver exatamente 1 vizinho ativo, é considerado endpoint
#                     if vizinhos == 1:
#                         nova[i, j] = 0
#                         removidos = True
#         pruned = nova
#         if not removidos:
#             break  # Não há mais endpoints para remover
#     return pruned

# # poda na imagem esqueletizada
# pruned = prune_skeleton(esq, 20)
# plt.figure()
# plt.imshow(pruned, cmap='gray')
# plt.title('Imagem Após Poda')
# Image.fromarray(pruned * 255).save('poda.png')
plt.show()