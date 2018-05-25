import json
from datetime import datetime, timedelta

import requests

from BookCirculation import BookCirculation
from DAO.AbstractDAO import AbstractDAO
from DAO.BookDAO import BookDAO
from DAO.UserDAO import UserDAO
from constant import *


class BookCirculationDAO(AbstractDAO):
    def __init__(self, parent = None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def borrow(self, user, books):
        borrow_list = []
        for book in books:
            borrow_list.append({"user": {"user_id": user.user_id}, "book": {"book_id": book.book_id}})

        # try:
        path = '/borrow'
        response = requests.post(self.server_ip + path, json=borrow_list, timeout = self.timeout, headers=self.get_authentication_header(path))
        if response.status_code == 200:   #Success
            book_circulations = []
            for raw_book_circulation in response.json():
                book_circulations.append(self.construct_book_ciruclation(raw_book_circulation))

            if self.parent is not None:
                due_time = book_circulations[0].due_time
                print(str(due_time))
                self.parent.borrowBookCallback(due_time)

        # except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
        #     self.parent.borrowBookCallback(datetime.now() + timedelta(days=7))
        #     print("Borrow failed")


        # return book_circulations

    def getAllCirculations(self):
        try:
            path = '/history'
            response = requests.get(self.server_ip + path , timeout = self.timeout, headers=self.get_authentication_header(path))
            circulations = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.construct_book_circulation(raw_data ))
                return to_return
            else:
                print("Request failed")
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")

        return None

    def getAllOnBorrowCirculation(self):
        try:
            path = '/borrow'
            response = requests.get(self.server_ip + path , timeout = self.timeout, headers=self.get_authentication_header(path))
            circulations = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.construct_book_circulation(raw_data ))
                return to_return
            else:
                print("Request failed")
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")


    @staticmethod
    def construct_book_circulation(arguments):
        time_args = ["borrow_time", "due_time", "return_time"]

        for time_arg in time_args:
            if time_arg in arguments.keys() and arguments[time_arg] is not None:
                arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        arguments["book"] = BookDAO.constructBook(arguments["book"])
        arguments["user"] = UserDAO.constructUser(arguments["user"])

        return BookCirculation(**arguments)

    def getBorrowIDFromBookID(self,bookID):
        for circulation in self.getAllOnBorrowCirculation():
            # print("cir id" + + str(circulation.book.book_id )+ "  " + str(bookID))
            if(str(circulation.book.book_id) == str(bookID)):
                return circulation.borrow_id

        return None

    def returnBook(self,borrowID):
        path = '/return/' + str(borrowID)
        response = requests.delete(self.server_ip + path, timeout=self.timeout, headers=self.get_authentication_header(path))
        if response.status_code == 200:  # Success
            print(response.text)
            pass
        else:
            print("Failed")

    def searchHistory(self, keyword):
        if keyword == "" or keyword.startswith(' '):
            return self.getAllCirculations()

        try:
            path = '/history/search/' + keyword
            response = requests.get(self.server_ip + path, timeout = self.timeout, headers=self.get_authentication_header(path))
            circulations = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.construct_book_circulation(raw_data ))
                return to_return
            else:
                print("Request failed")
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")

        return None

    def searchOnBorrow(self, keyword):
        if keyword == "" or keyword.startswith(' '):
            return self.getAllCirculations()

        try:
            path = '/borrow/search/' + keyword
            response = requests.get(self.server_ip + path , timeout = self.timeout, headers=self.get_authentication_header(path))
            circulations = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.construct_book_circulation(raw_data ))
                return to_return
            else:
                print("Request failed")
        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")

        return None





if __name__ == "__main__":
    bookCirculationDAO = BookCirculationDAO()
    for circulation in bookCirculationDAO.getAllCirculations():
        print(str(circulation))
