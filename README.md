# Mandelbrot Fractal (C + Python)

## Descrição
Este projeto é uma demonstração de integração entre as linguagens de programação C e Python para a disciplina de Conceitos de Linguagens de Programação.
O objetivo é utilizar a linguagem C para o processamento computacional intensivo (desempenho) através do cálculo do fractal de Mandelbrot e utilizar Python para gerenciar a interface gráfica (`tkinter`). A integração ocorre através do mecanismo FFI (Foreign Function Interface) fornecido pela biblioteca nativa `ctypes`.

## Estrutura do Repositório
- `src/mandelbrot.c`: Lógica principal de cálculo das iterações matemáticas em C.
- `src/mandelbrot.h`: Arquivo de cabeçalho e documentação das assinaturas exportadas do C.
- `src/main.py`: Aplicação Python encarregada de interagir com o usuário, passar parâmetros para a biblioteca C usando ponteiros alocados e renderizar o resultado matemático.
- `docs/documentacao.md`: Documentação técnica completa detalhando os motivos de uso das linguagens e como funciona o ctypes.
- `Makefile`: Script facilitador para construir (build) e executar a aplicação.

## Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas e configuradas no seu `PATH`:
- **gcc**: Compilador C (para gerar a biblioteca dinâmica `.so`, `.dll` ou `.dylib`).
- **python3** (ou `python` no Windows): Interpretador Python (versão 3+).
- **tkinter**: Biblioteca gráfica padrão do Python.
- **ctypes**: Biblioteca nativa que intermedeia o C e o Python. (Já vem inclusa na instalação do Python).

## Instruções de Compilação
Para compilar a biblioteca compartilhada do C, entre na pasta principal `mandelbrot` e execute:
```bash
make
```
*(No Windows/MinGW, será gerado `mandelbrot.dll`, no Linux `libmandelbrot.so` e no macOS `libmandelbrot.dylib`)*.

## Instruções de Execução
Para executar a aplicação e abrir a interface gráfica padrão:
```bash
make run
```

## Exemplo de Uso (Demonstração)
Se desejar executar a aplicação diretamente apontando para uma área exótica de "zoom" (demostração do poder de cálculo) pré-configurada, execute:
```bash
make demo
```

**Controles Básicos na Interface:**
- **Botão Esquerdo do Mouse**: Clicar em qualquer ponto do fractal fará a câmera aplicar "Zoom In" (aproximar).
- **Botão Direito do Mouse**: Clicar na imagem fará a câmera aplicar "Zoom Out" (afastar).
- **Painel Superior**: Permite alterar o tamanho da janela (`Largura`/`Altura`) e aumentar a profundidade do cálculo (`Iterações Max`). Ao editar os valores, clique em **Gerar**.