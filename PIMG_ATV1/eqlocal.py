import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from PIL import Image
import ocrmypdf
import subprocess
import time
import os
import difflib

# lê a imagem
img = imread('prova.jpeg')

# realiza a equalização local
def local_equalization(img, k):
    # add padding na img
    padded_img = np.pad(img, k // 2, mode='edge') 
    # inicializa a img de saída
    output = np.zeros_like(img)
    print("ok1")
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # extrai a janela local
            local_window = padded_img[i:i+k, j:j+k]
            
            # calcula o histograma local
            h, _ = np.histogram(local_window, bins=400, range=(0, 400))
            h = h.astype('float') / (k * k)  # normalizando o histograma
            
             # aplica o limite de clipagem
            h = np.clip(h, 0, 0.001)
            h = h / np.sum(h)  # renormaliza o histograma
            
            # calcula a função de transformação cumulativa
            T = (np.cumsum(h) * 255).astype('uint8')
            
            # aplica a transformação (ao pixel central da janela)
            output[i, j] = T[img[i, j]]
    return output
        
tam_jan1 = 200
tam_jan2 = 400        
print("ok2")
output1 = local_equalization(img, tam_jan1) # equalização local com janela 200x200
output2 = local_equalization(img, tam_jan2) # equalização local com janela 400x400

# Função para calcular a precisão do OCR 
def calculate_accuracy(extracted_text, reference_text):
    return difflib.SequenceMatcher(None, extracted_text, reference_text).ratio() * 100

# Função para realizar OCR e medir desempenho
def perform_ocr(image_path, ocr_output_path, text_output_path, reference_text):
    start_time = time.time()
    ocrmypdf.ocr(image_path, ocr_output_path)
    end_time = time.time()
    processing_time = end_time - start_time

    subprocess.run(["pdftotext", ocr_output_path, text_output_path])
    with open(text_output_path, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    accuracy = calculate_accuracy(extracted_text, reference_text)
    file_size = os.path.getsize(ocr_output_path) / 1024  # Tamanho em KB

    return processing_time, accuracy, file_size

# Exibindo as imgs
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
ax[0].imshow(img, cmap='gray')
ax[0].set_title('Img Original')
ax[1].imshow(output1, cmap='gray')
ax[1].set_title('Img Eq Local 200x200')
ax[2].imshow(output2, cmap='gray')
ax[2].set_title('IMG Eq Local 400x400')
plt.show(block=False)
print("ok3")

# Salvando as imagens como PDF
img_pil = Image.fromarray(img)
output1_pil = Image.fromarray(output1)
output2_pil = Image.fromarray(output2)

img_pil.save("img_original.pdf")
output1_pil.save("img_eq_local_200x200.pdf")
output2_pil.save("img_eq_local_400x400.pdf")

# Texto de referência para calcular a precisão do OCR
reference_text = """Questão 2 (4 pontos)
Escreva uma função para decidir se num tabuleiro de jogo da velha há um vencedor e, caso exista,
qual é o símbolo associado a ele.

Sua função deve verificar as seguintes situações anômalas:

1. Ocorrência de mais de um vencedor
2. Ocorrência de mais de dois tipos de símbolos associados aos jogadores"""

# Aplicar OCR nas imagens PDF e medir desempenho
results = []
results.append(perform_ocr("img_original.pdf", "img_original_ocr.pdf", "img_original.txt", reference_text))
results.append(perform_ocr("img_eq_local_200x200.pdf", "img_eq_local_200x200_ocr.pdf", "img_eq_local_200x200.txt", reference_text))
results.append(perform_ocr("img_eq_local_400x400.pdf", "img_eq_local_400x400_ocr.pdf", "img_eq_local_400x400.txt", reference_text))

# exibir os resultados
for i, (processing_time, accuracy, file_size) in enumerate(results):
    print(f"Imagem {i+1}:")
    print(f"Tempo de Processamento: {processing_time:.2f} s")
    print(f"Precisão OCR: {accuracy:.2f} %")
    print(f"Tamanho do Arquivo: {file_size:.2f} KB")
    print()
    
# extraindo o texto do ocr
subprocess.run(["pdftotext", "img_original_ocr.pdf", "img_original.txt"])
subprocess.run(["pdftotext", "img_eq_local_200x200_ocr.pdf", "img_eq_local_200x200.txt"])
subprocess.run(["pdftotext", "img_eq_local_400x400_ocr.pdf", "img_eq_local_400x400.txt"])

# Exibe os histogramas das imagens original e transformadas
fig, ax = plt.subplots(1, 3, figsize=(18, 4))
ax[0].hist(img.ravel(), bins=400, range=(0, 400), color='black', alpha=0.7)
ax[0].set_title('Histograma Original')
ax[1].hist(output1.ravel(), bins=400, range=(0, 400), color='black', alpha=0.7)
ax[1].set_title('Histograma 200x200')
ax[2].hist(output2.ravel(), bins=400, range=(0, 400), color='black', alpha=0.7)
ax[2].set_title('Histograma 400x400')
plt.show()

