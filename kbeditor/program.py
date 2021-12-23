import sys
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.setFixedSize(800, 800)
    w.setWindowTitle("Simple keyboard editor")
    w.show()
    sys.exit(app.exec_())