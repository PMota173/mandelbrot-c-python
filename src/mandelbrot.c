/**
 * Arquivo: mandelbrot.c
 * Descrição: Implementação do cálculo iterativo do Fractal de Mandelbrot.
 *            Escrito em C para maximizar a performance matemática.
 */

#include "mandelbrot.h"

EXPORT void calcular_mandelbrot(int largura, int altura, int max_iter, double x_min, double x_max, double y_min, double y_max, int *resultado) {
    // Calcula a "distância" entre cada pixel no plano complexo
    double dx = (x_max - x_min) / largura;
    double dy = (y_max - y_min) / altura;

    // Loops aninhados para percorrer cada pixel da imagem gerada.
    // A execução em C compilado garante que essa repetição massiva seja rápida.
    for (int j = 0; j < altura; j++) {
        double c_imag = y_min + j * dy;

        for (int i = 0; i < largura; i++) {
            double c_real = x_min + i * dx;

            double z_real = 0.0;
            double z_imag = 0.0;
            int iter = 0;
            
            // Loop matemático do fractal: z = z^2 + c
            // A tipagem estática do C (double, int) permite otimização na CPU
            // durante essas operações de ponto flutuante.
            while (z_real * z_real + z_imag * z_imag <= 4.0 && iter < max_iter) {
                double temp_real = z_real * z_real - z_imag * z_imag + c_real;
                z_imag = 2.0 * z_real * z_imag + c_imag;
                z_real = temp_real;
                iter++;
            }

            // Armazena o resultado em um array 1D usando aritmética simples,
            // que mapeia a coordenada (i,j) 2D para o índice linear.
            resultado[j * largura + i] = iter;
        }
    }
}
