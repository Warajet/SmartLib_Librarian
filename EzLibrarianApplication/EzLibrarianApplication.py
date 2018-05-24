import sys
import Adapter.TableAdapter as TableAdapter
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SmartLib_LibrarianUI import Ui_MainWindow
from threading import Timer
from DAO import BookDAO, UserDAO
from Book import Book
from User.User import User


# Catch Error and display through MessageBox
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class SmartLibUi(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        '''
        INITIAL UI SETUP
        '''
        # QAction (Menu Bar)
        self.ui.actionMain_Menu.triggered.connect(self.selectTabMainMenu)
        self.ui.actionAdd_Book.triggered.connect(self.dialog_AddBook)
        self.ui.actionExit.triggered.connect(self.exit)

        # pushButton (Main Menu Buttons)
        self.ui.buttonOverview_Books.clicked.connect(self.selectTabBooks)
        self.ui.buttonOverview_Users.clicked.connect(self.selectTabUsers)
        self.ui.buttonOverview_Issue.clicked.connect(self.selectTabIssue)
        self.ui.buttonOverview_4.clicked.connect(self.dialog_AddBook)

        '''
        UI DECORATORs
        '''
        # self.ui.tabWidget.setStyleSheet("QWidget {background-color: yellow }")
        self.ui.buttonOverview_Books.setStyleSheet("background-color:rgb(0,184,237); color:white;")
        self.ui.buttonOverview_Users.setStyleSheet("background-color:rgb(0,156,80); color:white;")
        self.ui.buttonOverview_Issue.setStyleSheet("background-color:rgb(216,65,50); color:white;")

        # Green Button
        self.ui.buttonBooks_Add.setStyleSheet("background-color:green;")
        self.ui.buttonUsers_Add.setStyleSheet("background-color:green;")
        self.ui.buttonCirculation_Add.setStyleSheet("background-color:green;")
        self.ui.buttonIssue_Add.setStyleSheet("background-color:green;")
        '''
        TAB: BOOKS
        '''
        self.ui.tableBooks.verticalHeader().setVisible(False)
        self.ui.tableBooks.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.buttonBooks_Add.clicked.connect(self.dialog_AddBook)
        self.ui.buttonBooks_Edit.clicked.connect(self.dialog_EditBook1)
        # self.ui.buttonBooks_Delete.clicked.connect()
        # self.ui.buttonBooks_Go.clicked.connect()

        '''
        TAB: USERS
        '''
        self.ui.tableUsers.verticalHeader().setVisible(False)
        self.ui.tableUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.buttonUsers_Add.clicked.connect(self.dialog_AddUser)
        self.ui.buttonUsers_Edit.clicked.connect(self.dialog_EditUser1)
        # self.ui.buttonUsers_Delete.clicked.connect()
        # self.ui.buttonUsers_Go.clicked.connect()

        '''
        TAB: CIRCULATION
        '''
        self.ui.tableCirculation.verticalHeader().setVisible(False)
        self.ui.tableCirculation.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # self.ui.buttonCirculation_Add.clicked.connect(self.dialog_AddBook)
        # self.ui.buttonCirculation_Edit.clicked.connect()
        # self.ui.buttonCirculation_Delete.clicked.connect()
        # self.ui.buttonCirculation_Go.clicked.connect()

        '''
        TAB: ISSUE
        '''
        self.ui.tableIssue.verticalHeader().setVisible(False)
        self.ui.tableIssue.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ui.buttonIssue_Add.clicked.connect(self.dialog_AddBook)
        # self.ui.buttonIssue_Edit.clicked.connect()
        # self.ui.buttonIssue_Delete.clicked.connect()
        # self.ui.buttonIssue_Go.clicked.connect()


        '''
        TableAdapter
        '''
        self.bookDAO = BookDAO.BookDAO()
        self.userDAO = UserDAO.UserDAO()
        self.booksTableAdapter = TableAdapter.BookTableAdapter(self.ui.tableBooks)
        self.userTableAdapter = TableAdapter.UserTableAdapter(self.ui.tableUsers)
        self.init_element()

    '''
    FUNCTIONS
    '''

    # App Handler
    def exit(self):
        app.quit()

    # Select Tab Functions
    def selectTabMainMenu(self):
        self.ui.tabWidget.setCurrentIndex(0)

    def selectTabBooks(self):
        self.ui.tabWidget.setCurrentIndex(1)

    def selectTabUsers(self):
        self.ui.tabWidget.setCurrentIndex(2)

    def selectTabIssue(self):
        self.ui.tabWidget.setCurrentIndex(4)

    def init_element(self):
        self.loadAllBooks()
        self.loadAllUsers()

    # Load all books(or update) in database to books table
    def loadAllBooks(self):
        allBooks = self.bookDAO.getAllBooks()
        self.booksTableAdapter.addBooks(allBooks)
        booksCount = len(allBooks)

        # update books quantity on first page button
        self.ui.buttonOverview_Books.setText("   " + str(booksCount) + "  Books")

    # Load all student(or update) in database to student table
    def loadAllUsers(self):
        allUsers = self.userDAO.getAllUsers()
        self.userTableAdapter.addUsers(allUsers)
        usersCount = len(allUsers)

        # update users quantity on first page button
        self.ui.buttonOverview_Users.setText("   " + str(usersCount) + "  Users")

    '''
        Add books
    '''

    def dialog_AddBook(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        dialog.setWindowTitle("Add Book")
        dialog.resize(630, 150)

        label1 = QLabel(self)
        label1.setText("Title: ")
        title_textBox = QLineEdit(self)
        layout.addWidget(label1)
        layout.addWidget(title_textBox)

        label2 = QLabel(self)
        label2.setText("ISBN: ")
        ISBN_textBox = QLineEdit(self)
        layout.addWidget(label2)
        layout.addWidget(ISBN_textBox)

        label3 = QLabel(self)
        label3.setText("Author: ")
        author_textBox = QLineEdit(self)
        layout.addWidget(label3)
        layout.addWidget(author_textBox)

        label4 = QLabel(self)
        label4.setText("Publisher: ")
        publisher_textBox = QLineEdit(self)
        layout.addWidget(label4)
        layout.addWidget(publisher_textBox)

        label5 = QLabel(self)
        label5.setText("RFID: ")
        rfid_textBox = QLineEdit(self)
        layout.addWidget(label5)
        layout.addWidget(rfid_textBox)

        closeButton = QPushButton('OK')

        field = []
        field.append(title_textBox)
        field.append(ISBN_textBox)
        field.append(author_textBox)
        field.append(publisher_textBox)
        field.append(rfid_textBox)
        closeButton.clicked.connect(lambda: self.onDialogAddBookSaved(dialog, field))
        layout.addWidget(closeButton)

        print(dialog.children())
        dialog.setLayout(layout)
        dialog.show()

    def onDialogAddBookSaved(self, dialog, field):
        title = field[0].text()
        ISBN = field[1].text()
        author = field[2].text()
        publisher = field[3].text()
        rfid = field[4].text()

        newBook = Book(None, title, ISBN, None, author, publisher, rfid)
        self.bookDAO.addBook(newBook)
        dialog.close()
        Timer(1, self.loadAllBooks).start()

    '''
        Book Editing

    '''

    def dialog_EditBook1(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        dialog.setWindowTitle("Enter book ID")
        dialog.resize(630, 150)

        label0 = QLabel(self)
        label0.setText("ID: ")
        id_textBox = QLineEdit(self)
        layout.addWidget(label0)
        layout.addWidget(id_textBox)

        okButton = QPushButton('Next')
        okButton.clicked.connect(lambda: self.dialog_EditBook2(dialog, id_textBox))
        layout.addWidget(okButton)

        dialog.setLayout(layout)
        dialog.show()

    def dialog_EditBook2(self, first_dialog, id_textBox):
        book_to_edit = self.bookDAO.getBookFromID(id_textBox.text())
        if (book_to_edit == None):
            errorDialog = QErrorMessage(self)
            errorDialog.showMessage("Error", "Couldn't find book for this ID")
            return

        first_dialog.close()
        dialog = QDialog(self)
        layout = QVBoxLayout()
        label1 = QLabel(self)
        label1.setText("Title: ")
        title_textBox = QLineEdit(self)
        title_textBox.setText(book_to_edit.title)
        layout.addWidget(label1)
        layout.addWidget(title_textBox)

        label2 = QLabel(self)
        label2.setText("ISBN: ")
        ISBN_textBox = QLineEdit(self)
        ISBN_textBox.setText(book_to_edit.isbn)
        layout.addWidget(label2)
        layout.addWidget(ISBN_textBox)

        label3 = QLabel(self)
        label3.setText("Author: ")
        author_textBox = QLineEdit(self)
        author_textBox.setText(book_to_edit.author)
        layout.addWidget(label3)
        layout.addWidget(author_textBox)

        label4 = QLabel(self)
        label4.setText("Publisher: ")
        publisher_textBox = QLineEdit(self)
        publisher_textBox.setText(book_to_edit.publisher)
        layout.addWidget(label4)
        layout.addWidget(publisher_textBox)

        label5 = QLabel(self)
        label5.setText("RFID: ")
        rfid_textBox = QLineEdit(self)
        rfid_textBox.setText(book_to_edit.rfid)
        layout.addWidget(label5)
        layout.addWidget(rfid_textBox)

        closeButton = QPushButton('OK')

        field = []
        field.append(title_textBox)
        field.append(ISBN_textBox)
        field.append(author_textBox)
        field.append(publisher_textBox)
        field.append(rfid_textBox)
        closeButton.clicked.connect(lambda: self.onDialogEditBookSaved(dialog, book_to_edit, field))
        layout.addWidget(closeButton)

        dialog.setLayout(layout)
        dialog.show()

    def onDialogEditBookSaved(self, dialog, oldBook, field):
        title = field[0].text()
        ISBN = field[1].text()
        author = field[2].text()
        publisher = field[3].text()
        rfid = field[4].text()

        updatedBook = Book(oldBook.book_id, title, ISBN, oldBook.added_on, author, publisher, rfid)
        self.bookDAO.updateBook(updatedBook)
        dialog.close()
        self.loadAllBooks()

    '''
     Add user
    '''

    def dialog_AddUser(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        dialog.setWindowTitle("Add User")
        dialog.resize(630, 150)

        label1 = QLabel(self)
        label1.setText("ID: ")
        id_textBox = QLineEdit(self)
        layout.addWidget(label1)
        layout.addWidget(id_textBox)

        label2 = QLabel(self)
        label2.setText("Name: ")
        name_textBox = QLineEdit(self)
        layout.addWidget(label2)
        layout.addWidget(name_textBox)

        label3 = QLabel(self)
        label3.setText("Email: ")
        email_textBox = QLineEdit(self)
        layout.addWidget(label3)
        layout.addWidget(email_textBox)

        label5 = QLabel(self)
        label5.setText("RFID: ")
        rfid_textBox = QLineEdit(self)
        layout.addWidget(label5)
        layout.addWidget(rfid_textBox)

        closeButton = QPushButton('OK')

        field = []
        field.append(id_textBox)
        field.append(name_textBox)
        field.append(email_textBox)
        field.append(rfid_textBox)
        closeButton.clicked.connect(lambda: self.onDialogAddUserSaved(dialog, field))
        layout.addWidget(closeButton)

        dialog.setLayout(layout)
        dialog.show()

    def onDialogAddUserSaved(self, dialog, field):
        id = field[0].text()
        name = field[1].text()
        email = field[2].text()
        rfid = field[3].text()

        newUser = User(id, name, None, email, rfid, None)
        self.userDAO.addUser(newUser)
        dialog.close()
        Timer(1, self.loadAllUsers).start()

    '''
     Edit user
    '''

    def dialog_EditUser1(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        dialog.setWindowTitle("Enter user ID")
        dialog.resize(630, 150)

        label0 = QLabel(self)
        label0.setText("ID: ")
        id_textBox = QLineEdit(self)
        layout.addWidget(label0)
        layout.addWidget(id_textBox)

        okButton = QPushButton('Next')
        okButton.clicked.connect(lambda: self.dialog_EditUser2(dialog, id_textBox))
        layout.addWidget(okButton)

        dialog.setLayout(layout)
        dialog.show()

    def dialog_EditUser2(self, first_dialog, id_textBox):
        user_to_edit = self.userDAO.getUserFromID(id_textBox.text())
        if (user_to_edit == None):
            errorDialog = QErrorMessage(self)
            errorDialog.showMessage("Error", "Couldn't find user for this ID")
            return

        first_dialog.close()
        dialog = QDialog(self)
        layout = QVBoxLayout()
        label1 = QLabel(self)
        label1.setText("Name: ")
        name_textBox = QLineEdit(self)
        name_textBox.setText(user_to_edit.name)
        layout.addWidget(label1)
        layout.addWidget(name_textBox)

        label2 = QLabel(self)
        label2.setText("Email: ")
        email_textBox = QLineEdit(self)
        email_textBox.setText(user_to_edit.email)
        layout.addWidget(label2)
        layout.addWidget(email_textBox)

        label3 = QLabel(self)
        label3.setText("Line token: ")
        lineToken_textBox = QLineEdit(self)
        lineToken_textBox.setText(user_to_edit.lineToken)
        layout.addWidget(label3)
        layout.addWidget(lineToken_textBox)

        label4 = QLabel(self)
        label4.setText("rfid: ")
        rfid_textBox = QLineEdit(self)
        rfid_textBox.setText(user_to_edit.rfid)
        layout.addWidget(label4)
        layout.addWidget(rfid_textBox)

        closeButton = QPushButton('OK')

        field = []
        field.append(name_textBox)
        field.append(email_textBox)
        field.append(lineToken_textBox)
        field.append(rfid_textBox)
        closeButton.clicked.connect(lambda: self.onDialogEditUserSaved(dialog, user_to_edit, field))
        layout.addWidget(closeButton)

        dialog.setLayout(layout)
        dialog.show()

    def onDialogEditUserSaved(self, dialog, oldUser: User, field):
        name = field[0].text()
        email = field[1].text()
        lineToken = field[2].text()
        rfid = field[3].text()

        updatedUser = User(oldUser.user_id, name, oldUser.registered_on, email, rfid, lineToken)
        self.userDAO.updateUser(updatedUser)
        dialog.close()
        self.loadAllUsers()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SmartLibUi()
    w.show()
    sys.exit(app.exec_())
