from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.pushButton1 = QPushButton("Button 1", self.centralwidget)
        self.pushButton2 = QPushButton("Button 2", self.centralwidget)

        lay = QHBoxLayout(self.centralwidget)
        lay.addWidget(self.pushButton1)
        lay.addWidget(self.pushButton2)


stylesheet = """
    MainWindow {
        background-image: url("bells-img.jpg"); 
        background-repeat: no-repeat; 
        background-attachment: fixed;
    }
"""

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     # <---
    window = MainWindow()
    window.resize(640, 640)
    window.show()
    sys.exit(app.exec())