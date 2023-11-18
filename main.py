import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class AddFilmWidget(QMainWindow):
    def __init__(self, parent=None, res=[]):
        super().__init__(parent)
        uic.loadUi('addEditCoffeForm.ui', self)

        if res:
            self.res = res[0]
            self.NameText.setText(str(res[0][1]))
            self.StepenText.setText(str(res[0][2]))
            self.MolotText.setText(str(res[0][3]))
            self.VkysText.setText(str(res[0][4]))
            self.SumText.setText(str(res[0][5]))
            self.ObemText.setText(str(res[0][6]))
            self.pushButton.clicked.connect(self.r)

    def r(self):
        if self.res[0] == 0:
            self.con = sqlite3.connect('films_db.sqlite')
            cur = self.con.cursor()
            res = cur.execute(f'''SELECT id FROM films''').fetchall()
            res = max([i[0] for i in res])
            cur.execute(f'''INSERT INTO films(Name, Stepen, Molot, Vkys, Sum, Obem) 
            VALUES({res + 1}, "{self.NameText.text()}", {self.StepenText.text()}, {self.MolotText.text()},
            {self.VkysText.text()}, {self.SumText.text()}, {self.ObemText.text()})''')
            self.con.commit()
            self.parent().updatetab()
            self.close()
        else:
            self.statusbar.showMessage('Неверно заполнена форма')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.NewButton.clicked.connect(self.add)
        self.EditButton.clicked.connect(self.edit)
        self.updatetab()

    def updatetab(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Coffi").fetchall()
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        for row, items in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col, item in enumerate(items):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))

    def edit(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 1:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            res = cur.execute(
                f'''SELECT Id, Name, Stepen, Molot, Vkys, Sum, Obem FROM Coffi WHERE id = {ids[0]}''').fetchall()
            self.add_film_widget = AddFilmWidget(self, res)
            self.add_film_widget.show()

    def add(self):
        self.add_film_widget = AddFilmWidget(self)
        self.add_film_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
