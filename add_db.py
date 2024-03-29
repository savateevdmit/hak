import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


def SaveDB(text):
    # print(text)

    # Соединение с базой данных
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    # Добавление записи
    try:
        cursor.execute(f"INSERT INTO test (text) VALUES ('{text}')")
        connection.commit()
        cursor.close()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Запись {text} добавлена")
        msg.setWindowTitle("Уведомление")
        msg.exec_()
    except Exception as e:
        print(f"Unexpected error: {e}")



