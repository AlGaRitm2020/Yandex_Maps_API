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
        # import design
        self.setupUi(self)

        # create static map button
        self.pushButton.clicked.connect(self.get_image)

    def get_image(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.doubleSpinBox_longitude.value()}," \
                      f"{self.doubleSpinBox_latitude.value()}&spn={self.doubleSpinBox_scale.value()},{0.0001}&l=map"
        # get response
        response = requests.get(map_request)

        if not response:
            print("Request execution error: ")
            print(map_request)
            print("Http status:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # write img to file
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        # set pixmap to label
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    # delete temp file map.png
    def closeEvent(self, event):
        os.remove(self.map_file)

    # key pressed (PgUP and PgDown)
    def keyPressEvent(self, e):
        # zoom in
        if e.key() in [QtCore.Qt.Key_PageUp]:
            self.doubleSpinBox_scale.setValue(self.doubleSpinBox_scale.value() / 2)
            self.get_image()

        # zoom out
        elif e.key() in [QtCore.Qt.Key_PageDown]:
            self.doubleSpinBox_scale.setValue(self.doubleSpinBox_scale.value() * 2)
            self.get_image()
        else:
            super(QMainWindow, self).keyPressEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
