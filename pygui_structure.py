from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

def on_click():
    print("Button was clicked!")


app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

button = QPushButton("Click Me",)
button.clicked.connect(on_click)
button.setStyleSheet("""
    QPushButton {
        background-color: #2c3e50;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #1974cf;
    }""")

layout.addWidget(button)
window.setLayout(layout)
window.show()

app.exec_()


