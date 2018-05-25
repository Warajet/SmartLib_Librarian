import json

from Book import Book
from datetime import datetime
from DAO.AbstractDAO import AbstractDAO
from constant import rfc_822_format
import requests
import random


class BookDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def getBookFromID(self, id):
        try:
            path = '/book/' + str(id)
            response = requests.get(self.server_ip + path, timeout = self.timeout, headers=self.get_authentication_header(path))
            book = None
            if response.status_code == 200:
                book = self.constructBook(response.json())
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            book = Book(random.randint(100,1000),"Offline book", "-",datetime.now(),True,"Offline guy",
                        "Offline press .ltd")
            print("Waring! use offline data for debugging only")
        if self.parent is not None:
            self.parent.addBook(book)

        return book

    def getBookFromRFID_ID(self, rfid):
        try:
            path = '/book/rfid/' + str(rfid)
            response = requests.get(self.server_ip + path, timeout = self.timeout, headers=self.get_authentication_header(path))
            book = None
            if response.status_code == 200:
                book = self.constructBook(response.json())
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            book = Book(random.randint(100, 1000), "Offline book", "-", datetime.now(), True, "Offline guy",
                        "Offline press .ltd")
            print("Waring! use offline data for debugging only")


        if self.parent is not None:
            self.parent.addBook(book)

        return book

    @staticmethod
    def constructBook(arguments):
        time_arg = "added_on"

        arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        return Book(**arguments)

    def getAllBooks(self):
        try:
            path = '/book'
            response = requests.get(self.server_ip + path, timeout = self.timeout, headers=self.get_authentication_header(path))
            book = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.constructBook(raw_data ))

                return to_return
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")

    def addBook(self, book:Book):
        path = '/book'

        dict_to_add = book.__dict__
        del dict_to_add['book_id']
        del dict_to_add['added_on']

        print(dict_to_add)

        response = requests.post(self.server_ip + path, json=dict_to_add, timeout=self.timeout, headers=self.get_authentication_header(path))
        if response.status_code == 201:  # Success
            print(response.json())
            pass

    def updateBook(self, book:Book):
        path = '/book/' + str(book.book_id)

        dict_to_add = book.__dict__
        del dict_to_add['added_on']

        print(dict_to_add)

        response = requests.put(self.server_ip + path, json=dict_to_add, timeout=self.timeout, headers=self.get_authentication_header(path))
        if response.status_code == 200:  # Success
            print(response.json())
            pass
        else:
            print("Failed")

    def deleteBook(self,book:Book):
        path = '/book/' + str(book.book_id)

        response = requests.delete(self.server_ip + path, timeout=self.timeout, headers=self.get_authentication_header(path))
        if response.status_code == 200:  # Success
            print(response.json())
            pass
        else:
            print("Failed")

    def searchBook(self,keyword:str):
        if keyword == "" or keyword.startswith(' '):
            return self.getAllBooks()

        try:
            path = '/book/search/' + str(keyword)
            response = requests.get(self.server_ip + path, timeout=self.timeout, headers=self.get_authentication_header(path))
            book = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.constructBook(raw_data))

                return to_return
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")




if __name__ == "__main__":
    bookDAO = BookDAO()
    for book in bookDAO.searchBook("asp"):
        print(book.__dict__)




