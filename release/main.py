import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from UI.mainWin import Ui_Form
from UI.addEditCoffeForm import Ui_Form2


class AddFilmWidget(QMainWindow, Ui_Form2):
    def __init__(self, parent=None, res=[]):
        super().__init__(parent)
        self.setupUi(self)

        if res:
            self.res = res[0]
            self.NameText.setText(str(res[0][1]))
            self.StepenText.setText(str(res[0][2]))
            self.MolotText.setText(str(res[0][3]))
            self.VkysText.setText(str(res[0][4]))
            self.SumText.setText(str(res[0][5]))
            self.ObemText.setText(str(res[0][6]))
            self.pushButton.clicked.connect(self.r2)
        else:
            self.pushButton.clicked.connect(self.r)

    def r2(self):
        try:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            cur.execute(f'''UPDATE coffi
             SET Name = "{self.NameText.text()}", 
             Stepen = {self.StepenText.text()}, 
             Molot = "{self.MolotText.text()}", 
             Vkys = "{self.VkysText.text()}", 
             Sum = {self.SumText.text()}, 
             Obem = {self.ObemText.text()}
             WHERE id = {self.res[0]}''')
            con.commit()
            self.parent().updatetab()
            self.close()
        except:
            error = QMessageBox()
            error.setText("Неверно заполнена форма")
            error.setWindowTitle("Error")
            error.exec_()

    def r(self):
        try:
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            cur.execute(f'''INSERT INTO coffi(Name, Stepen, Molot, Vkys, Sum, Obem) 
            VALUES("{self.NameText.text()}", {self.StepenText.text()}, "{self.MolotText.text()}",
            "{self.VkysText.text()}", {self.SumText.text()}, {self.ObemText.text()})''')
            con.commit()
            self.parent().updatetab()
            self.close()
        except:
            error = QMessageBox()
            error.setText("Неверно заполнена форма")
            error.setWindowTitle("Error")
            error.exec_()


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.NewButton.clicked.connect(self.add)
        self.EditButton.clicked.connect(self.edit)
        self.updatetab()

    def updatetab(self):
        con = sqlite3.connect("data/coffee.sqlite")
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
            con = sqlite3.connect("data/coffee.sqlite")
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
