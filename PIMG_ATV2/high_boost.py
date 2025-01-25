from skimage.transform import rescale
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt

# g(x,y)=A⋅f(x,y)−L(x,y)
# g(x,y): é a imagem filtrada (retornada).
# f(x,y): é a img original.
# L(x,y): suavização\passabaixa
# A: fator de amplificação. A>1 para realçar as bordas
def highboost(image, A, scale):
    img_highboost = image.copy()
    # Reaplica o filtro
    for _ in range(2):
        image_rescaled = rescale(img_highboost, scale, anti_aliasing=True)
        img_suavizada = rescale(image_rescaled, 1/scale, anti_aliasing=True)
        img_highboost = A * img_highboost - img_suavizada

    return img_highboost

# Para as placas 01 e 02, usar scale 1/4, para as outras placas, utilizar escala 1/3
scale = 1/4
image = imread('placa01.png', as_gray=True)
image_rescaled = rescale(image, scale, anti_aliasing=True)
image_restored = rescale(image_rescaled, 1/scale, anti_aliasing=True)
A = [1.5, 2, 3, 4, 5]


_, ax = plt.subplots(1, len(A) + 3, figsize=(20, 5))
ax[0].imshow(image, cmap='gray')
ax[0].set_title("Original")
ax[1].imshow(image_rescaled, cmap='gray')
ax[1].set_title("Reduzida")
ax[2].imshow(image_restored, cmap='gray')
ax[2].set_title("Restaurada")
for i, A in enumerate(A):
    image_highboost = highboost(image_restored, A, scale)
    ax[i + 3].imshow(image_highboost, cmap='gray')
    ax[i + 3].set_title(f"Highboost A={A}")

plt.tight_layout()
plt.show()
