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

        self.doubleSpinBox_latitude.valueChanged.connect(self.get_image)
        self.doubleSpinBox_longitude.valueChanged.connect(self.get_image)
        self.doubleSpinBox_scale.valueChanged.connect(self.get_image)

    def get_image(self):
        # self.doubleSpinBox_scale.setFocus()

        # single step to latitude anв longitude
        self.doubleSpinBox_latitude.setSingleStep(self.doubleSpinBox_scale.value() / 10)
        self.doubleSpinBox_longitude.setSingleStep(self.doubleSpinBox_scale.value() / 10)

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.doubleSpinBox_longitude.value()}," \
                      f"{self.doubleSpinBox_latitude.value()}&spn={self.doubleSpinBox_scale.value()},{0.0001}&l=map&size=650,450"
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
    def keyPressEvent(self, event):
        # zoom in
        if event.key() in [QtCore.Qt.Key_PageUp, QtCore.Qt.Key]:
            self.doubleSpinBox_scale.setValue(self.doubleSpinBox_scale.value() / 2)

        # zoom out
        elif event.key() in [QtCore.Qt.Key_PageDown]:
            self.doubleSpinBox_scale.setValue(self.doubleSpinBox_scale.value() * 2)

        # move center up
        elif event.key() in [QtCore.Qt.Key_W]:
            self.doubleSpinBox_latitude.setValue(
                self.doubleSpinBox_latitude.value() + self.doubleSpinBox_scale.value() / 10)

        # move center down
        elif event.key() in [QtCore.Qt.Key_S]:
            self.doubleSpinBox_latitude.setValue(
                self.doubleSpinBox_latitude.value() - self.doubleSpinBox_scale.value() / 10)

        # move center right
        elif event.key() in [QtCore.Qt.Key_D]:
            self.doubleSpinBox_longitude.setValue(
                self.doubleSpinBox_longitude.value() + self.doubleSpinBox_scale.value() / 10)

        # move center left
        elif event.key() in [QtCore.Qt.Key_A]:
            self.doubleSpinBox_longitude.setValue(
                self.doubleSpinBox_longitude.value() - self.doubleSpinBox_scale.value() / 10)

        else:
            super(QMainWindow, self).keyPressEvent(event)

        self.get_image()

    # mouse wheel( up or down)
    def wheelEvent(self, event):
        # zoom in
        if event.angleDelta().y() == 120:
            self.doubleSpinBox_scale.setValue(self.doubleSpinBox_scale.value() / 2)
            self.get_image()
        # zoom out
        else:
            self.doubleSpinBox_scale.setValue(self.doubleSpinBox_scale.value() * 2)
            self.get_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
