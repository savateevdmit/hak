import sys
import random

import numpy as np
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from PyQt5 import QtCore, QtWidgets

from add_db import SaveDB
from del_db import  DEL_DB

# Это нужно для того, чтобы на экранах с высоким разрешением нормально работало (так написано в учебнике яла)
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# Класс приложения
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.add_graf.clicked.connect(self.graf)
        self.add_error.clicked.connect(self.error)
        self.add_clean.clicked.connect(self.clean)
        self.add_db.clicked.connect(self.add)
        self.del_db.clicked.connect(self.dell)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        # Обратите внимание: имя элемента такое же как в QTDesigner

    def graf(self):
        plot_x = [0, 5, 7, 10, 15, 22, 25, 31, 35, 40]
        plot_y = [6, 9, 3, 15, 5, 13, 7, 11, 9, -5]

        points_x = [5, 24, 6, 1, 33, 39]
        points_y = [2, 7, 21, 8, -3, 1]

        self.MplWidget.canvas.axes.clear()  # очищаем график
        self.MplWidget.canvas.axes.plot(plot_x, plot_y, color='b', marker='o')  # рисуем синий график
        self.MplWidget.canvas.axes.scatter(points_x, points_y, color='r', marker='x')  # рисуем красные точки
        self.MplWidget.canvas.axes.legend(('График', 'Точки'), loc='upper right')  # добавляем легенду
        self.MplWidget.canvas.axes.set_title('Очень красивый график')  # добавляем заголовок
        self.MplWidget.canvas.draw()  # рисуем график

    def clean(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()

    def error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Текст ошибки, также можно сделать уведомление (QMessageBox.Information)")
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def dell(self):
        self.window3 = DEL_DB()
        self.window3.setWindowTitle("Выберите файл из БД")
        self.window3.show()

    def add(self):
        text = self.textEdit.toPlainText()

        if len(text) == 0:  # Проверка на пустую строку
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("В поле с текстом пусто")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            SaveDB(text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.showMaximized()
    sys.exit(app.exec_())
