from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTimer
import sys

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embedded Control Panel")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: #1e272e; color: white;")

        layout = QVBoxLayout()

        self.status_label = QLabel("System Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.status_label)

        start_btn = QPushButton("Start")
        stop_btn = QPushButton("Stop")
        reset_btn = QPushButton("Reset")

        for btn in (start_btn, stop_btn, reset_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            """)
            layout.addWidget(btn)

        start_btn.clicked.connect(self.start_action)
        stop_btn.clicked.connect(self.stop_action)
        reset_btn.clicked.connect(self.reset_action)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.counter = 0

    def start_action(self):
        self.status_label.setText("System Running...")
        self.counter = 0
        self.timer.start(1000)

    def stop_action(self):
        self.status_label.setText("System Stopped.")
        self.timer.stop()

    def reset_action(self):
        self.status_label.setText("System Reset.")
        self.counter = 0
        self.timer.stop()

    def update_status(self):
        self.counter += 1
        self.status_label.setText(f"Running... {self.counter} sec")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = ControlPanel()
    panel.show()
    sys.exit(app.exec_())
