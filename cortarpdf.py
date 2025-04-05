from PyPDF2 import PdfReader, PdfWriter

def extrair_paginas_pdf(arquivo_entrada, arquivo_saida, pagina_inicial, pagina_final):
    with open(arquivo_entrada, "rb") as pdf_arquivo:
        leitor = PdfReader(pdf_arquivo)
        escritor = PdfWriter()
        
        # Adicionar páginas ao novo PDF
        for num_pagina in range(pagina_inicial - 1, pagina_final):
            escritor.add_page(leitor.pages[num_pagina])
        
        with open(arquivo_saida, "wb") as pdf_saida:
            escritor.write(pdf_saida)
    print(f"PDF gerado: {arquivo_saida}")

# Exemplo de uso
extrair_paginas_pdf("entrada.pdf", "saida.pdf", 501, 504)
