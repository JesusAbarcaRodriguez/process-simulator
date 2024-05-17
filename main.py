import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from controller.view_controller import MainView
import sys
import os
import resources_rc
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# =======================
# Main
# =======================
app = QApplication(sys.argv)
main = MainView()
main.show()

sys.exit(app.exec_())