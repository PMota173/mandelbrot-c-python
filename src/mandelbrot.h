/**
 * Arquivo: mandelbrot.h
 * Descrição: Interface da biblioteca C para cálculo do Fractal de Mandelbrot.
 *            Define a função que será exportada e chamada pelo Python.
 */

#ifndef MANDELBROT_H
#define MANDELBROT_H

// Diretivas de pré-processador para garantir que a função seja exportada
// corretamente dependendo do sistema operacional (Windows vs Linux/macOS).
#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

/**
 * Função principal de cálculo.
 * Recebe os parâmetros do plano complexo e as dimensões da imagem.
 * O resultado é armazenado diretamente no ponteiro 'resultado', que aponta
 * para uma região de memória previamente alocada pela linguagem chamadora (Python).
 * O uso de ponteiros aqui permite alta eficiência na transferência dos dados.
 */
EXPORT void calcular_mandelbrot(int largura, int altura, int max_iter, double x_min, double x_max, double y_min, double y_max, int *resultado);

#endif // MANDELBROT_H
