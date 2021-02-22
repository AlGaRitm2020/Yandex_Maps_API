import os
import sys

import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

SCREEN_SIZE = [800, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.spinBox_latitude.value()}," \
                      f"{self.spinBox_latitude.value()}&spn={self.spinBox_scale.value()},{self.spinBox_scale.value()}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        # Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 50)
        self.image.resize(750, 450)
        self.image.setPixmap(self.pixmap)
        self.image.show()


    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        # self.pixmap = QPixmap(self.map_file)
        # self.image = QLabel(self)
        # self.image.move(0, 0)
        # self.image.resize(600, 450)
        # self.image.setPixmap(self.pixmap)

        # label "Enter the coordinates"
        self.label_coords = QLabel("Enter the coordinates", self)
        self.label_coords.resize(100, 20)
        self.label_coords.move(0, 0)

        # label "Enter the scale"
        self.label_coords = QLabel("Enter the scale", self)
        self.label_coords.resize(100, 20)
        self.label_coords.move(0, 30)

        # spinBox for latitude coord
        self.spinBox_latitude = QDoubleSpinBox(self)
        self.spinBox_latitude.resize(100, 20)
        self.spinBox_latitude.move(200, 0)

        # spinBox for longitude coord
        self.spinBox_longitude = QDoubleSpinBox(self)
        self.spinBox_longitude.resize(100, 20)
        self.spinBox_longitude.move(310, 0)

        # spinBox for scale
        self.spinBox_scale = QDoubleSpinBox(self)
        self.spinBox_scale.resize(100, 20)
        self.spinBox_scale.move(200, 30)

        # pushbutton
        self.pushbutton = QPushButton("Draw", self)
        self.pushbutton.move(420, 0)
        self.pushbutton.resize(100, 50)
        self.pushbutton.clicked.connect(self.getImage)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
