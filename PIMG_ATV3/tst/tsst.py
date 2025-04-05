import numpy as np
import cv2

# Exemplo: matriz representando uma imagem em escala de cinza
imagem = np.array([
    [0, 0, 0],
    [255, 255, 0],
    [0, 0, 0],
], dtype=np.uint8)

# Cria o kernel 3x3 (todos os elementos iguais a 1)
kernel = np.array([
    [0, 255, 0],
    [0, 255, 0],
    [0, 0, 0],
], dtype=np.uint8)


# Realiza a dilatação seguida da erosão (fechamento morfológico)
dilatada = cv2.dilate(imagem, kernel, iterations=1)
print("Dilatada:")
print(dilatada)
fechamento = cv2.erode(dilatada, kernel, iterations=1)
# Ou, de forma direta, usando morphologyEx:
# fechamento = cv2.morphologyEx(imagem, cv2.MORPH_CLOSE, kernel)

# Exibe as matrizes no console
print("Imagem Original:")
print(imagem)
print("\nImagem com Fechamento:")
print(fechamento)
