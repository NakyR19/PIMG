# Comparação de Desempenho da Digitalização

A tabela abaixo compara o desempenho da digitalização utilizando OCR nas três diferentes imagens: a imagem original, a imagem com equalização local 128X128 e a imagem com equalização local 256x256.

| Imagem                    | Tempo de Processamento (s)  | Precisão OCR (%)     | Tamanho do Arquivo (KB)   |
|---------------------------|-----------------------------|----------------------|---------------------------|
| Imagem Original           | 1.52                        | 21.60                | 20.46                     |
| Equalização Local 128X128 | 1.45                        | 45.06                | 25.27                     |
| Equalização Local 256x256 | 1.46                        | 20.34                | 24.99                     |

## Observações

- **Tempo de Processamento:** Tempo necessário para realizar o OCR na imagem.
- **Precisão OCR:** Percentual de precisão do texto extraído em relação ao texto original.
- **Tamanho do Arquivo:** Tamanho do arquivo PDF gerado após a aplicação do OCR.

### Conclusão

A imagem com equalização local 128X128 apresentou a maior precisão no OCR, e teve um tempo de processamento ligeiramente menor, contudo houve um aumento no tamanho do arquivo. Logo, pode ser considerada a melhor dentre as testadas.