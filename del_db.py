import sqlite3
import sys

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit, QFileDialog, \
    QMessageBox, QMainWindow, QTableWidget, QDialog, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QTimer, QRect, QCoreApplication, QMetaObject, Qt
from PyQt5.QtGui import QImage, QPainter, QPixmap, QColor
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


class Ui_Form2(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(669, 385)
        self.deleteFilmButton = QPushButton(Form)
        self.deleteFilmButton.setObjectName(u"deleteFilmButton")
        self.deleteFilmButton.setGeometry(QRect(10, 330, 651, 51))
        self.filmsTable = QTableWidget(Form)
        self.filmsTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.filmsTable.setObjectName(u"filmsTable")
        self.filmsTable.setGeometry(QRect(10, 0, 651, 321))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.deleteFilmButton.setText(
            QCoreApplication.translate("Form", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0444\u0430\u0439\u043b",
                                       None))
    # retranslateUi


class DEL_DB(QDialog, Ui_Form2):  # Вот тут основное окно
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.up_f()
        self.deleteFilmButton.clicked.connect(self.df)
        self.dialogs = []
        # self.exitAction.triggered.connect(self.exit)

    def up_f(self):
        try:
            result = []
            connection = sqlite3.connect('test.db')
            cursor = connection.cursor()

            # Function to read all records from the "test" table
            try:
                cursor.execute("SELECT * FROM test")
                res = cursor.fetchall()
            except Exception as e:
                print(f"Error reading records: {e}")

        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Проверьте интернет соединение!")
            msg.setWindowTitle("Ошибка подключения к БД")
            msg.exec_()

        print(res)

        if res:
            for i in res:
                res = list(i)
                result.append(res)
            print(result)

            self.filmsTable.setRowCount(len(result))
            self.filmsTable.setColumnCount(len(result[0]))
            self.filmsTable.setHorizontalHeaderLabels(
                ['Номер', 'Текст'])

            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.filmsTable.setItem(i, j, QTableWidgetItem(str(val)))


    def df(self):
        rows = list(set([i.row() for i in self.filmsTable.selectedItems()]))
        # Вот тут важно, что в переменную ids я записываю нулевой элемент, в данном случае это номер
        ids = [self.filmsTable.item(i, 0).text() for i in rows]
        if not ids:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите что-нибудь!")
            msg.setWindowTitle("Уведомление")
            msg.exec_()
            return

        else:
            print(ids)
            try:
                connection = sqlite3.connect('test.db')
                cursor = connection.cursor()

                try:
                    cursor.execute("DELETE FROM test WHERE number=?", (int(''.join(ids)),))
                    connection.commit()
                    print(f"Record {''.join(ids)} deleted successfully")

                except Exception as e:
                    print(f"Unexpected error: {e}")

                self.up_f()
                self.close()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Файл удалён!")
                msg.setWindowTitle("Уведомление")
                msg.exec_()

            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Проверьте интернет соединение!")
                msg.setWindowTitle("Ошибка подключения к БД")
                msg.exec_()

    def exit(self):
        self.close()


# Если надо будет отладить удаление из бд, расскоментируй эти строки и запускай этот файл
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = DEL_DB()
#     ex.show()
#     sys.exit(app.exec_())
