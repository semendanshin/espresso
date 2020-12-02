import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.comboBox_grade.currentTextChanged.connect(self.load_degree)
        self.comboBox_degree.currentTextChanged.connect(self.load_volume)
        self.comboBox_volume.currentTextChanged.connect(self.load_info)
        self.load_types()

    def load_types(self):
        self.comboBox_grade.addItems([el[0] for el in list(cur.execute(
            """SELECT DISTINCT name from items ORDER BY name"""))])

    def load_degree(self):
        self.comboBox_degree.clear()
        self.comboBox_degree.addItems([el[0].capitalize() for el in list(
            cur.execute("""SELECT degree from degrees JOIN items
                ON degree_id=degrees.id WHERE name=?""", (
                self.comboBox_grade.currentText(), )))])

    def load_volume(self):
        self.comboBox_volume.clear()
        self.comboBox_volume.addItems([str(el[0]) for el in list(cur.execute(
            """SELECT volume from packages JOIN items
                ON items.id=item_id JOIN degrees ON
                degrees.id=degree_id WHERE name=? and
                degree=? ORDER BY volume""", (
                self.comboBox_grade.currentText(),
                self.comboBox_degree.currentText().lower())))])

    def load_info(self):
        try:
            info = list(cur.execute("""SELECT type, price,
                description from packages JOIN degrees
                ON degree_id=degrees.id JOIN types ON type_id=types.id
                JOIN items ON items.id=item_id WHERE
                name=? and volume=?""", (
                self.comboBox_grade.currentText(),
                self.comboBox_volume.currentText())))[0]
        except IndexError:
            self.statusBar.showMessage('Ошибка данных!')
        else:
            self.statusBar.clearMessage()
            self.lineEdit_type.setText(info[0].capitalize())
            self.lineEdit_price.setText(str(info[1]))
            self.plainTextEdit.setPlainText(info[2])


if __name__ == '__main__':
    con = sqlite3.connect('coffee.sqlite')
    cur = con.cursor()
    app = QApplication(sys.argv)
    worker = Main()
    worker.show()
    sys.exit(app.exec())
