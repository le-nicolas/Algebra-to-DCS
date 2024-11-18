from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QSlider, QPushButton, QWidget
)
from PyQt5.QtCore import QTimer, Qt
import sys
import random

class DCSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Distributed Control System - Monitoring Dashboard")
        self.setGeometry(100, 100, 800, 600)
        
        # Main container
        self.container = QWidget()
        self.layout = QVBoxLayout()

        # Tank status display
        self.tank_displays = []
        for i in range(4):  # 4 tanks for simplicity
            label = QLabel(f"Tank-{i+1}: Level = 50")
            label.setStyleSheet("font-size: 16px;")
            self.layout.addWidget(label)
            self.tank_displays.append((i, label))
        
        # Threshold sliders and disturbance buttons
        self.threshold_sliders = []
        for i in range(4):
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(20)
            slider.setMaximum(80)
            slider.setValue(50)
            slider.valueChanged.connect(self.update_threshold)
            self.layout.addWidget(slider)
            self.threshold_sliders.append(slider)

            button = QPushButton(f"Simulate Disturbance - Tank-{i+1}")
            button.clicked.connect(lambda checked, tank=i: self.simulate_disturbance(tank))
            self.layout.addWidget(button)
        
        # Start monitoring
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        # Simulated data update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tanks)
        self.timer.start(2000)  # Update every 2 seconds

    def update_tanks(self):
        for i, label in self.tank_displays:
            new_level = random.randint(10, 90)
            label.setText(f"Tank-{i+1}: Level = {new_level}")
            if new_level < self.threshold_sliders[i].value() - 10 or new_level > self.threshold_sliders[i].value() + 10:
                label.setStyleSheet("color: red; font-size: 16px;")
            else:
                label.setStyleSheet("color: black; font-size: 16px;")

    def update_threshold(self):
        sender = self.sender()
        index = self.threshold_sliders.index(sender)
        print(f"Threshold for Tank-{index+1} updated to {sender.value()}")

    def simulate_disturbance(self, tank):
        disturbance = random.randint(-20, 20)
        print(f"Disturbance for Tank-{tank+1}: {disturbance}")
        label = self.tank_displays[tank][1]
        current_level = int(label.text().split("=")[-1])
        new_level = max(0, min(100, current_level + disturbance))
        label.setText(f"Tank-{tank+1}: Level = {new_level}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DCSApp()
    window.show()
    sys.exit(app.exec_())
