import os
import sys

import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from design.main import *

SCREEN_SIZE = [800, 450]


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_image)

    def get_image(self):

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.doubleSpinBox_longitude.value()}," \
                      f"{self.doubleSpinBox_latitude.value()}&spn={self.doubleSpinBox_scale.value()},{self.doubleSpinBox_scale.value()}&l=map"

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
        self.pixmap = QPixmap(self.map_file)
        print(self.pixmap)
        self.image.setPixmap(self.pixmap)


    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
