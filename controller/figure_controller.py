import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer
from util.global_state import GlobalState 
class FigureOne(FigureCanvas):
    def __init__(self, is_pri_mem):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5),sharey=True, facecolor='white')
        super().__init__(self.fig)
        self.global_state = GlobalState()
        self.fig.subplots_adjust(left=0.07, right=0.99, top=0.9, bottom=0.1)
        self.is_pri_mem = is_pri_mem
        self.x = np.arange(1, 101)
        self.y_memory = np.zeros_like(self.x)

        self.line, = self.ax.plot(self.x, self.y_memory, color='red')
        self.ax.set_ylim(0, 1024)
        self.ax.set_xlim(0, 150)
        self.ax.set_xticks([])
        if self.is_pri_mem:
            self.ax.set_yticks(range(0, self.global_state.block_prim_memory_size, 512))
        else:
            self.ax.set_yticks(range(0, self.global_state.block_sec_memory_size, self.global_state.block_sec_memory_size//6))
    

        self.memory_text = self.ax.text(0.5, -0.1, '', transform=self.ax.transAxes, ha='center')
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_memory)
        self.timer.start(1000)

    def update_memory(self):
        if self.is_pri_mem:
            # Actualizar la lista de datos de ocupación de memoria
            self.y_memory = np.append(self.y_memory[1:], self.global_state.pri_memory_used)
            # Actualizar el texto de la memoria
            usage_text = f"{self.global_state.pri_memory_used}/{self.global_state.block_prim_memory_size}"
        else:
            # Actualizar la lista de datos de ocupación de memoria
            self.y_memory = np.append(self.y_memory[1:], self.global_state.sec_memory_used)
            # Actualizar el texto de la memoria
            usage_text = f"{self.global_state.sec_memory_used}/{self.global_state.block_sec_memory_size}"
        self.memory_text.set_text(usage_text)
        # Actualizar los datos en la gráfica
        self.line.set_ydata(self.y_memory)

        # Redibujar la gráfica
        self.ax.figure.canvas.draw()
