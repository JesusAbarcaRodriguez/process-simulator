import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from controller.menu_controller import MenuApp
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# =======================
# Main
# =======================
app = QApplication(sys.argv)
main = MenuApp()
main.show()

sys.exit(app.exec_())