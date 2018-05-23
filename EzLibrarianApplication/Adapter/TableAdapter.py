from PyQt5.QtWidgets import *
from datetime import datetime


class TableAdapter:
    def __init__(self,table):
        self.table = table

    def addRow(self,object):
        pass

    def clearTable(self):
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)

class BookTableAdapter(TableAdapter):
    def __init__(self,table):
        TableAdapter.__init__(self, table)

    def addBooks(self, books):
        self.clearTable()

        row  = 0
        for book in books:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(book.book_id)))
            self.table.setItem(row, 1, QTableWidgetItem(book.title))
            self.table.setItem(row, 2, QTableWidgetItem(book.author))
            self.table.setItem(row, 3, QTableWidgetItem(book.publisher))
            self.table.setItem(row, 4, QTableWidgetItem(book.isbn))
            self.table.setItem(row, 5, QTableWidgetItem(book.rfid))
            row +=1
        header = self.table.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QHeaderView.Stretch)


class UserTableAdapter(TableAdapter):
    def __init__(self, table):
        TableAdapter.__init__(self, table)

    def addUsers(self, users):
        self.clearTable()

        row = 0
        for user in users:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.name))
            self.table.setItem(row, 2, QTableWidgetItem(user.email))
            self.table.setItem(row, 3, QTableWidgetItem(user.registered_on.strftime('%d/%m/%y')))
            self.table.setItem(row, 4, QTableWidgetItem(user.lineToken))
            self.table.setItem(row, 5, QTableWidgetItem(user.rfid))
            row += 1
        header = self.table.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QHeaderView.Stretch)
