# Arquivo: main.py
# Descrição: Aplicação gráfica em Python. Atua como "linguagem de cola", 
#            gerenciando a interface com o usuário e orquestrando as 
#            chamadas para a biblioteca de cálculo em C.

import tkinter as tk
import ctypes
import os
import sys
import argparse

# --- Integração Python -> C (FFI) ---
# Identifica o sistema operacional para carregar o arquivo binário correto.
if sys.platform.startswith('win'):
    LIB_NAME = "mandelbrot.dll"
elif sys.platform.startswith('darwin'):
    LIB_NAME = "libmandelbrot.dylib"
else:
    LIB_NAME = "libmandelbrot.so"

try:
    # ctypes é a biblioteca padrão do Python para interagir com bibliotecas C.
    # Ela carrega a biblioteca compilada na memória do processo Python.
    lib_path = os.path.join(os.path.dirname(__file__), "..", LIB_NAME)
    if not os.path.exists(lib_path):
        lib_path = os.path.join(os.path.dirname(__file__), LIB_NAME)

    mandel_lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"Erro ao carregar a biblioteca '{LIB_NAME}'. Você compilou o código C? Erro: {e}")
    sys.exit(1)

# Precisamos definir explicitamente a "assinatura" da função C.
# Como o Python tem tipagem dinâmica, o ctypes precisa saber quais tipos C 
# correspondentes (int, double, ponteiros) enviar para evitar falhas de memória.
mandel_lib.calcular_mandelbrot.argtypes = [
    ctypes.c_int,               # largura
    ctypes.c_int,               # altura
    ctypes.c_int,               # max_iter
    ctypes.c_double,            # x_min
    ctypes.c_double,            # x_max
    ctypes.c_double,            # y_min
    ctypes.c_double,            # y_max
    ctypes.POINTER(ctypes.c_int) # resultado (ponteiro para o array em C)
]
mandel_lib.calcular_mandelbrot.restype = None


class MandelbrotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal de Mandelbrot (C + Python)")

        # Configurações iniciais de visualização
        self.width = 600
        self.height = 400
        self.max_iter = 100
        self.x_min = -2.5
        self.x_max = 1.0
        self.y_min = -1.0
        self.y_max = 1.0

        self.create_widgets()
        self.draw_fractal()

    def create_widgets(self):
        # Criação da interface gráfica aproveitando a facilidade do Tkinter
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Label(control_frame, text="Largura:").grid(row=0, column=0)
        self.entry_width = tk.Entry(control_frame, width=5)
        self.entry_width.insert(0, str(self.width))
        self.entry_width.grid(row=0, column=1)

        tk.Label(control_frame, text="Altura:").grid(row=0, column=2)
        self.entry_height = tk.Entry(control_frame, width=5)
        self.entry_height.insert(0, str(self.height))
        self.entry_height.grid(row=0, column=3)

        tk.Label(control_frame, text="Iterações Max:").grid(row=0, column=4)
        self.entry_iter = tk.Entry(control_frame, width=5)
        self.entry_iter.insert(0, str(self.max_iter))
        self.entry_iter.grid(row=0, column=5)

        tk.Button(control_frame, text="Gerar", command=self.update_params_and_draw).grid(row=0, column=6, padx=10)
        tk.Button(control_frame, text="Reset", command=self.reset_params).grid(row=0, column=7)

        self.status_label = tk.Label(self.root, text="Clique com botão esquerdo para zoom in, direito para zoom out.", fg="gray")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.zoom_in)
        self.canvas.bind("<Button-2>", self.zoom_out)
        self.canvas.bind("<Button-3>", self.zoom_out)

    def reset_params(self):
        self.x_min = -2.5
        self.x_max = 1.0
        self.y_min = -1.0
        self.y_max = 1.0
        self.update_params_and_draw()

    def update_params_and_draw(self):
        try:
            self.width = int(self.entry_width.get())
            self.height = int(self.entry_height.get())
            self.max_iter = int(self.entry_iter.get())
            self.canvas.config(width=self.width, height=self.height)
            self.draw_fractal()
        except ValueError:
            self.status_label.config(text="Erro: Valores inválidos nos campos!")

    def zoom_in(self, event):
        self.apply_zoom(event.x, event.y, zoom_factor=0.5)

    def zoom_out(self, event):
        self.apply_zoom(event.x, event.y, zoom_factor=2.0)

    def apply_zoom(self, mouse_x, mouse_y, zoom_factor):
        click_real = self.x_min + (mouse_x / self.width) * (self.x_max - self.x_min)
        click_imag = self.y_min + (mouse_y / self.height) * (self.y_max - self.y_min)

        radius_x = ((self.x_max - self.x_min) / 2) * zoom_factor
        radius_y = ((self.y_max - self.y_min) / 2) * zoom_factor

        self.x_min = click_real - radius_x
        self.x_max = click_real + radius_x
        self.y_min = click_imag - radius_y
        self.y_max = click_imag + radius_y

        self.draw_fractal()

    def iter_to_color(self, iters, max_iter):
        if iters == max_iter:
            return "#000000"
        intensity = int((iters / max_iter) * 255)
        return f"#{0:02x}{intensity:02x}{255:02x}"

    def draw_fractal(self):
        self.status_label.config(text="Calculando em C...")
        self.root.update()

        # O Python aloca o bloco de memória que o C vai preencher.
        # Isso é mais eficiente do que o C alocar e devolver a propriedade pro Python.
        ResultArrayType = ctypes.c_int * (self.width * self.height)
        resultado_c = ResultArrayType()

        # Chama a função C passando as configurações e o ponteiro de memória
        mandel_lib.calcular_mandelbrot(
            self.width, self.height, self.max_iter,
            self.x_min, self.x_max, self.y_min, self.y_max,
            resultado_c
        )

        self.status_label.config(text="Renderizando interface...")
        self.root.update()

        self.img = tk.PhotoImage(width=self.width, height=self.height)

        # Transforma o array linear que veio do C em pixels para a imagem
        pixels = []
        for j in range(self.height):
            row = []
            for i in range(self.width):
                iters = resultado_c[j * self.width + i]
                color = self.iter_to_color(iters, self.max_iter)
                row.append(color)
            pixels.append("{" + " ".join(row) + "}")

        self.img.put(" ".join(pixels))

        self.canvas.delete("all")
        self.canvas.create_image((0, 0), image=self.img, state="normal", anchor="nw")

        self.status_label.config(text=f"Pronto! | x=[{self.x_min:.2f}, {self.x_max:.2f}] y=[{self.y_min:.2f}, {self.y_max:.2f}]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mandelbrot Fractal Viewer")
    parser.add_argument("--demo", action="store_true", help="Executar com parâmetros de demonstração")
    args = parser.parse_args()

    root = tk.Tk()
    app = MandelbrotApp(root)

    if args.demo:
        app.entry_width.delete(0, tk.END); app.entry_width.insert(0, "800")
        app.entry_height.delete(0, tk.END); app.entry_height.insert(0, "600")
        app.entry_iter.delete(0, tk.END); app.entry_iter.insert(0, "200")
        app.x_min = -0.74877
        app.x_max = -0.74872
        app.y_min = 0.06505
        app.y_max = 0.06510
        app.update_params_and_draw()

    root.mainloop()