from PyQt5.QtWidgets import *
from datetime import datetime

class TableAdapter:
    def __init__(self,table):
        self.table = table

    def clearTable(self):
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)

class BookTableAdapter(TableAdapter):
    def __init__(self,table):
        TableAdapter.__init__(self, table)

    def addBooks(self, books):
        self.clearTable()
        row  = 0
        if books is None:
            return
        for book in books:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(book.book_id)))
            self.table.setItem(row, 1, QTableWidgetItem(book.title))
            self.table.setItem(row, 2, QTableWidgetItem(book.author))
            self.table.setItem(row, 3, QTableWidgetItem(book.publisher))
            self.table.setItem(row, 4, QTableWidgetItem(book.isbn))
            self.table.setItem(row, 5, QTableWidgetItem(book.rfid))
            row += 1
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

class UserTableAdapter(TableAdapter):
    def __init__(self, table):
        TableAdapter.__init__(self, table)

    def addUsers(self, users):
        self.clearTable()
        row = 0
        if users is None:
            return
        for user in users:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.name))
            self.table.setItem(row, 2, QTableWidgetItem(user.email))
            self.table.setItem(row, 3, QTableWidgetItem(user.registered_on.strftime('%d/%m/%y %H:%M')))
            self.table.setItem(row, 4, QTableWidgetItem(user.lineToken))
            self.table.setItem(row, 5, QTableWidgetItem(user.rfid))
            row += 1
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

class HistoryTableAdapter(TableAdapter):
    def __init__(self,table):
        TableAdapter.__init__(self,table)

    def addCirculations(self, circulations):
        self.clearTable()
        row = 0
        if circulations is None:
            return
        for circulation in circulations:
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(circulation.borrow_id)))
            self.table.setItem(row, 1, QTableWidgetItem(circulation.book.title))
            self.table.setItem(row, 2, QTableWidgetItem(circulation.user.name))
            self.table.setItem(row, 3, QTableWidgetItem(circulation.borrow_time.strftime('%d/%m/%y %H:%M')))
            self.table.setItem(row, 4, QTableWidgetItem(circulation.due_time.strftime('%d/%m/%y %H:%M')))
            if (circulation.return_time != None):
              self.table.setItem(row, 5, QTableWidgetItem(circulation.return_time.strftime('%d/%m/%y %H:%M')))
            else:
                self.table.setItem(row, 5, QTableWidgetItem("-"))
            row += 1
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)