from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        # Create a button
        self.button = QPushButton("Open New Window")
        self.button.clicked.connect(self.open_new_window)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        # Set up central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()


class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Window")
        self.setGeometry(150, 150, 300, 200)

        # Add a label to the new window
        label = QLabel("This is the new window!", self)
        label.move(50, 80)


if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    app.exec()