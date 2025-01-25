import fitz  # PyMuPDF
from PIL import Image

def pdf_to_grayscale_images(pdf_path):
    """
    Converte cada página de um PDF em uma imagem em tons de cinza e salva na pasta atual.

    Args:
        pdf_path (str): Caminho para o arquivo PDF.
    """
    try:
        # Abre o PDF
        pdf_document = fitz.open(pdf_path)

        for page_number in range(len(pdf_document)):
            # Obtém a página
            page = pdf_document[page_number]

            # Renderiza a página como uma imagem em RGB
            pix = page.get_pixmap()

            # Converte a imagem para o formato PIL
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Converte para tons de cinza
            gray_image = img.convert('L')

            # Define o caminho para salvar a imagem
            output_file = f'prova.jpeg'

            # Salva a imagem
            gray_image.save(output_file)
            print(f"Página {page_number + 1} salva como {output_file}")

        pdf_document.close()
        print("Conversão concluída!")

    except Exception as e:
        print(f"Erro ao converter PDF: {e}")

# Exemplo de uso
pdf_path = 'prova.pdf'  # Substitua pelo caminho do seu PDF
pdf_to_grayscale_images(pdf_path)
