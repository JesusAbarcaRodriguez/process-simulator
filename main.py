import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from controller.view_controller import MainView
# =======================
# Main
# =======================
app = QApplication(sys.argv)
main = MainView()
main.show()
sys.exit(app.exec_())