from PIL import Image

def cortar_e_centralizar(imagem_path, tamanho_bloco, novo_tamanho):
    # Carregar a imagem original
    imagem = Image.open(imagem_path)
    largura, altura = imagem.size

    # Lista para armazenar os blocos 48x48 com imagem centralizada
    blocos_centralizados = []

    # Iterar sobre a imagem para cortar em blocos de tamanho especificado
    for y in range(0, altura, tamanho_bloco):
        for x in range(0, largura, tamanho_bloco):
            # Cortar o bloco 32x32
            box = (x, y, x + tamanho_bloco, y + tamanho_bloco)
            bloco = imagem.crop(box)

            # Criar nova imagem 48x48 com fundo transparente
            novo_bloco = Image.new("RGBA", (novo_tamanho, novo_tamanho), (0, 0, 0, 0))

            # Calcular a posição para centralizar o bloco 32x32 dentro do 48x48
            pos_x = (novo_tamanho - tamanho_bloco) // 2
            pos_y = (novo_tamanho - tamanho_bloco) // 2

            # Colar o bloco 32x32 no centro do 48x48
            novo_bloco.paste(bloco, (pos_x, pos_y))
            blocos_centralizados.append(novo_bloco)

    return blocos_centralizados

# Exemplo de uso
imagem_path = "ow1.png"  # Caminho da imagem enviada
tamanho_bloco = 32
novo_tamanho = 48

# Chamar a função e gerar os blocos centralizados
blocos = cortar_e_centralizar(imagem_path, tamanho_bloco, novo_tamanho)

# Salvar cada bloco centralizado como uma nova imagem
for i, bloco in enumerate(blocos):
    bloco.save(f"ash{i}.png")
