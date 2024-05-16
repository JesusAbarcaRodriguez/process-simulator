import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer

class FigureOne(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5),sharey=True, facecolor='white')
        super().__init__(self.fig)

        self.x = np.arange(1, 101)
        self.y_memory = np.zeros_like(self.x)

        self.line, = self.ax.plot(self.x, self.y_memory, color='red')

        self.ax.set_ylim(0, 1024)
        self.ax.set_xlim(0, 150)
        self.ax.set_xticks([])
        self.ax.set_yticks([128, 256, 384, 512, 640, 768, 896, 1024])

        self.memory_text = self.ax.text(0.5, -0.1, '', transform=self.ax.transAxes, ha='center')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_memory)
        self.timer.start(1000)

    def update_memory(self):
        # Generar un nuevo valor de ocupación de memoria (entre 0 y 1024 MB)
        new_memory_value = np.random.randint(0, 1025)

        # Actualizar la lista de datos de ocupación de memoria
        self.y_memory = np.append(self.y_memory[1:], new_memory_value)

        # Actualizar los datos en la gráfica
        self.line.set_ydata(self.y_memory)

        # Actualizar el texto de la memoria
        usage_text = f"{new_memory_value}/1024"
        self.memory_text.set_text(usage_text)

        # Redibujar la gráfica
        self.ax.figure.canvas.draw()
