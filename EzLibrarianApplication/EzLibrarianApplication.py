import sys
import cv2
import Adapter.TableAdapter as TableAdapter
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from SmartLib_LibrarianUI import Ui_MainWindow
from Scanner.CameraScanner import CameraScanner
from CameraViewerWidget import CameraViewerWidget
from DAO import BookDAO, UserDAO, BookCirculationDAO, NotificationDAO
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Book import Book
from User.User import User
from threading import Timer, Thread

class SmartLibUi(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        '''
        UI SIGNALS & SLOTS
        '''
        # Menu Bar (QAction)
        self.ui.actionMain_Menu.triggered.connect(lambda: self.ui.tabWidget.setCurrentIndex(0))
        self.ui.actionAdd_Book.triggered.connect(self.dialog_AddBook)
        self.ui.actionAdd_User.triggered.connect(self.dialog_AddUser)
        self.ui.actionReturnBook.triggered.connect(self.dialog_ReturnBook)
        self.ui.actionRefresh.triggered.connect(self.init_element)
        self.ui.actionReport.triggered.connect(self.quickReportDetails)
        self.ui.actionExit.triggered.connect(lambda: app.quit())
        # Main Menu Buttons (pushButton)
        self.ui.buttonOverview_Books.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))
        self.ui.buttonOverview_Users.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))
        self.ui.buttonOverview_Issue.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(4))
        self.ui.buttonOverview_AddBook.clicked.connect(self.dialog_AddBook)
        self.ui.buttonOverview_AddUser.clicked.connect(self.dialog_AddUser)
        self.ui.buttonOverview_ReturnBook.clicked.connect(self.dialog_ReturnBook)

        '''
        UI DECORATORS
        '''
        # [Overview] Button Colors
        self.ui.buttonOverview_Books.setStyleSheet("background-color:rgb(135, 206, 250);")
        self.ui.buttonOverview_Users.setStyleSheet("background-color:rgb(128, 255, 212);")
        self.ui.buttonOverview_Issue.setStyleSheet("background-color:rgb(241, 128, 128);")
        # [Tab] Text Font & Colors
        self.ui.tabWidget.setStyleSheet('QTabBar { font-size: 12pt; }')
        self.ui.tabWidget.tabBar().setTabTextColor(1, QColor(0, 184, 237))
        self.ui.tabWidget.tabBar().setTabTextColor(2, QColor(0, 156, 80))
        self.ui.tabWidget.tabBar().setTabTextColor(3, QColor(255, 157, 0))
        self.ui.tabWidget.tabBar().setTabTextColor(4, QColor(216, 65, 50))

        '''
        UI TABS
        '''
        # Tab[0] All Books
        self.ui.buttonBooks_Add.clicked.connect(self.dialog_AddBook)
        self.ui.buttonBooks_Edit.clicked.connect(self.dialog_EditBook)
        self.ui.buttonBooks_Delete.clicked.connect(self.dialog_deleteBook)
        self.ui.buttonBooks_Go.clicked.connect(self.searchBooks)
        self.ui.buttonBooks_Refresh.clicked.connect(self.init_element)
        self.ui.tableBooks.doubleClicked.connect(self.dialog_EditBook)
        # Tab[1] All Users
        self.ui.buttonUsers_Add.clicked.connect(self.dialog_AddUser)
        self.ui.buttonUsers_Edit.clicked.connect(self.dialog_EditUser)
        self.ui.buttonUsers_Delete.clicked.connect(self.dialog_DeleteUser)
        self.ui.buttonUsers_Go.clicked.connect(self.searchUser)
        self.ui.buttonUsers_Refresh.clicked.connect(self.init_element)
        self.ui.tableUsers.doubleClicked.connect(self.dialog_EditUser)
        # Tab[2] History
        self.ui.buttonHistory_Filter.setEnabled(False)
        self.ui.buttonHistory_Go.clicked.connect(self.searchHistory)
        self.ui.buttonHistory_Refresh.clicked.connect(self.init_element)
        # Tab[3] Issue Books
        self.ui.buttonIssue_ReturnBook.clicked.connect(self.dialog_ReturnBook)
        self.ui.buttonIssue_Remind.clicked.connect(self.sendNotificationToAllOnBorrow)
        self.ui.buttonIssue_Go.clicked.connect(self.searchOnBorrow)
        self.ui.buttonIssue_Refresh.clicked.connect(self.init_element)
        self.camUpdatetimer = None
        self.camIDscan = None
        self.returnDialog = None

        '''
        TableAdapter & DAO
        '''
        self.bookDAO = BookDAO.BookDAO()
        self.userDAO = UserDAO.UserDAO()
        self.notificationDAO = NotificationDAO.NotificationDAO()
        self.bookCirculationDAO = BookCirculationDAO.BookCirculationDAO()
        self.booksTableAdapter = TableAdapter.BookTableAdapter(self.ui.tableBooks)
        self.userTableAdapter = TableAdapter.UserTableAdapter(self.ui.tableUsers)
        self.historyTableAdapter = TableAdapter.HistoryTableAdapter(self.ui.tableHistory)
        self.onBorrowTableAdapter = TableAdapter.HistoryTableAdapter(self.ui.tableIssue)
        self.init_element()
        # Real-time search when typing
        self.ui.lineEditBooks_SearchBox.textChanged.connect(self.searchBooks)
        self.ui.lineEditUsers_SearchBox.textChanged.connect(self.searchUser)
        self.ui.lineEditHistory_SearchBox.textChanged.connect(self.searchHistory)
        self.ui.lineEditIssue_SearchBox.textChanged.connect(self.searchOnBorrow)

    '''
    ALL FUNCTIONS
    '''
    def init_element(self):
        self.loadAllBooks()
        self.loadAllUsers()
        self.loadAllHistory()
        self.loadAllOnBorrowBooks()

    # Load data and display + getter function
    def loadAllBooks(self):
        self.booksTableAdapter.addBooks(self.bookDAO.getAllBooks())
        self.ui.buttonOverview_Books.setText("   " + str(self.getNumAllBooks()) + "  Books")
    def loadAllUsers(self):
        self.userTableAdapter.addUsers(self.userDAO.getAllUsers())
        self.ui.buttonOverview_Users.setText("   " + str(self.getNumAllUsers()) + "  Users")
    def loadAllHistory(self):
        allHistory = self.bookCirculationDAO.getAllCirculations()
        self.historyTableAdapter.addCirculations(allHistory)
    def loadAllOnBorrowBooks(self):
        self.onBorrowTableAdapter.addCirculations(self.bookCirculationDAO.getAllOnBorrowCirculation())
        self.ui.buttonOverview_Issue.setText(" " + str(self.getNumBorrowBooks()) + " Issue Books")
    def getNumAllBooks(self):
        return len(self.bookDAO.getAllBooks())
    def getNumAllUsers(self):
        return len(self.userDAO.getAllUsers())
    def getNumIssueBooks(self):
        return len(self.bookCirculationDAO.getAllOnBorrowCirculation())
    def getNumBorrowBooks(self):
        return len(self.bookCirculationDAO.getAllOnBorrowCirculation())

    # Data visualization (pie chart)
    def quickReportDetails(self):
        plt.figure(num='Quick Report', figsize=(5, 6), dpi=200)
        reportGrid = GridSpec(2, 1)

        # Book Status
        book_status = [self.getNumAllBooks(), self.getNumIssueBooks()]
        labels1 = 'On Shelves' , 'Issue Books'
        plt.subplot(reportGrid[0, 0], aspect=1)
        plt.title('Book Status')
        plt.pie(book_status, explode=(0, 0.2), labels=labels1, colors=['lightskyblue', 'lightcoral'], autopct='%1.1f%%')
        
        # Books Issued till Date
        book_issued_till_date = [len(self.bookCirculationDAO.getAllOnBorrowCirculation()) - len(self.bookCirculationDAO.getOverdueCirculation()), len(self.bookCirculationDAO.getOverdueCirculation())]
        labels2 = 'In-period', 'Overdue Books'
        plt.subplot(reportGrid[1, 0], aspect=1)
        plt.title('Books Issued till Date')
        plt.pie(book_issued_till_date, explode=(0, 0.2), labels=labels2, colors=['aquamarine', 'khaki'], autopct='%1.1f%%')

        plt.tight_layout()
        plt.show()

    '''
    POP-UP DIALOGS
    '''
    def dialog_AddBook(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Book")
        dialog.resize(630, 150)
        layout = QVBoxLayout()

        label1 = QLabel(self)
        label1.setText("Title: ")
        lineEdit_Title = QLineEdit(self)
        layout.addWidget(label1)
        layout.addWidget(lineEdit_Title)

        label2 = QLabel(self)
        label2.setText("ISBN: ")
        lineEdit_ISBN = QLineEdit(self)
        layout.addWidget(label2)
        layout.addWidget(lineEdit_ISBN)

        label3 = QLabel(self)
        label3.setText("Author: ")
        lineEdit_Author = QLineEdit(self)
        layout.addWidget(label3)
        layout.addWidget(lineEdit_Author)

        label4 = QLabel(self)
        label4.setText("Publisher: ")
        lineEdit_Publisher = QLineEdit(self)
        layout.addWidget(label4)
        layout.addWidget(lineEdit_Publisher)

        label5 = QLabel(self)
        label5.setText("RFID: ")
        lineEdit_RFID = QLineEdit(self)
        layout.addWidget(label5)
        layout.addWidget(lineEdit_RFID)

        okButton = QPushButton('OK')
        layout.addWidget(okButton)

        field = []
        field.append(lineEdit_Title)
        field.append(lineEdit_ISBN)
        field.append(lineEdit_Author)
        field.append(lineEdit_Publisher)
        field.append(lineEdit_RFID)
        okButton.clicked.connect(lambda: self.onDialogAddBookSaved(dialog, field))

        dialog.setLayout(layout)
        dialog.show()

    def onDialogAddBookSaved(self, dialog, field):
        title = field[0].text()
        isbn = field[1].text()
        author = field[2].text()
        publisher = field[3].text()
        rfid = field[4].text()

        newBook = Book(None, title, isbn, None, author, publisher, rfid)
        self.bookDAO.addBook(newBook)
        dialog.close()
        Timer(1, self.loadAllBooks).start()

    def dialog_EditBook(self):
        try:
            book_id = self.ui.tableBooks.item(self.ui.tableBooks.currentRow(), 0).text()
        except AttributeError:
            self.displayErrorNoSpecificRow()
            return
        book_to_edit = self.bookDAO.getBookFromID(book_id)
        if (book_to_edit == None):
            self.displayErrorNoID()
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Book ID<" + str(book_to_edit.book_id) + ">")
        dialog.resize(630, 600)
        layout = QVBoxLayout()

        label1 = QLabel(self)
        label1.setText("Title: ")
        lineEdit_Title = QLineEdit(self)
        lineEdit_Title.setText(book_to_edit.title)
        layout.addWidget(label1)
        layout.addWidget(lineEdit_Title)

        label2 = QLabel(self)
        label2.setText("ISBN: ")
        lineEdit_ISBN = QLineEdit(self)
        lineEdit_ISBN.setText(book_to_edit.isbn)
        layout.addWidget(label2)
        layout.addWidget(lineEdit_ISBN)

        label3 = QLabel(self)
        label3.setText("Author: ")
        lineEdit_Author = QLineEdit(self)
        lineEdit_Author.setText(book_to_edit.author)
        layout.addWidget(label3)
        layout.addWidget(lineEdit_Author)

        label4 = QLabel(self)
        label4.setText("Publisher: ")
        lineEdit_Publisher = QLineEdit(self)
        lineEdit_Publisher.setText(book_to_edit.publisher)
        layout.addWidget(label4)
        layout.addWidget(lineEdit_Publisher)

        label5 = QLabel(self)
        label5.setText("RFID: ")
        lineEdit_RFID = QLineEdit(self)
        lineEdit_RFID.setText(book_to_edit.rfid)
        layout.addWidget(label5)
        layout.addWidget(lineEdit_RFID)

        okButton = QPushButton('OK')
        layout.addWidget(okButton)

        field = []
        field.append(lineEdit_Title)
        field.append(lineEdit_ISBN)
        field.append(lineEdit_Author)
        field.append(lineEdit_Publisher)
        field.append(lineEdit_RFID)
        okButton.clicked.connect(lambda: self.onDialogEditBookSaved(dialog, book_to_edit, field))

        dialog.setLayout(layout)
        dialog.show()

    def onDialogEditBookSaved(self, dialog, oldBook, field):
        title = field[0].text()
        isbn = field[1].text()
        author = field[2].text()
        publisher = field[3].text()
        rfid = field[4].text()

        updatedBook = Book(oldBook.book_id, title, isbn, oldBook.added_on, author, publisher, rfid)
        self.bookDAO.updateBook(updatedBook)
        dialog.close()
        self.loadAllBooks()

    def dialog_deleteBook(self):
        try:
            book_id = self.ui.tableBooks.item(self.ui.tableBooks.currentRow(), 0).text()
            book_title = self.ui.tableBooks.item(self.ui.tableBooks.currentRow(), 1).text()
        except AttributeError:
            self.displayErrorNoSpecificRow()
            return
        book_to_delete = self.bookDAO.getBookFromID(book_id)
        if (book_to_delete == None):
            self.displayErrorNoID()
            return

        warningText = "Do you want to delete the selected book?" + "\n\nID: " + str(book_id) + "\nTitle: " + str(book_title)
        buttonReply = QMessageBox.question(self, "Warning", warningText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.bookDAO.deleteBook(book_to_delete)
            self.loadAllBooks()

    def dialog_AddUser(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add User")
        dialog.resize(630, 150)
        layout = QVBoxLayout()

        label1 = QLabel(self)
        label1.setText("Name: ")
        lineEdit_Name = QLineEdit(self)
        layout.addWidget(label1)
        layout.addWidget(lineEdit_Name)

        label2 = QLabel(self)
        label2.setText("Email: ")
        lineEdit_Email = QLineEdit(self)
        layout.addWidget(label2)
        layout.addWidget(lineEdit_Email)

        label3 = QLabel(self)
        label3.setText("RFID: ")
        lineEdit_RFID = QLineEdit(self)
        layout.addWidget(label3)
        layout.addWidget(lineEdit_RFID)

        okButton = QPushButton('OK')
        layout.addWidget(okButton)

        field = []
        field.append(lineEdit_Name)
        field.append(lineEdit_Email)
        field.append(lineEdit_RFID)
        okButton.clicked.connect(lambda: self.onDialogAddUserSaved(dialog, field))

        dialog.setLayout(layout)
        dialog.show()

    def onDialogAddUserSaved(self, dialog, field):
        name = field[0].text()
        email = field[1].text()
        rfid = field[2].text()

        newUser = User(None, name, None, email, rfid, None)
        self.userDAO.addUser(newUser)
        dialog.close()
        Timer(1, self.loadAllUsers).start()

    def dialog_EditUser(self):
        try:
            user_id = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 0).text()
        except AttributeError:
            self.displayErrorNoSpecificRow()
            return
        user_to_edit = self.userDAO.getUserFromID(user_id)
        if (user_to_edit == None):
            self.displayErrorNoID()
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User ID<" + str(user_to_edit.user_id) + ">")
        dialog.resize(630, 600)
        layout = QVBoxLayout()

        label1 = QLabel(self)
        label1.setText("Name: ")
        lineEdit_Name = QLineEdit(self)
        lineEdit_Name.setText(user_to_edit.name)
        layout.addWidget(label1)
        layout.addWidget(lineEdit_Name)

        label2 = QLabel(self)
        label2.setText("Email: ")
        lineEdit_Email = QLineEdit(self)
        lineEdit_Email.setText(user_to_edit.email)
        layout.addWidget(label2)
        layout.addWidget(lineEdit_Email)

        label3 = QLabel(self)
        label3.setText("RFID: ")
        lineEdit_RFID = QLineEdit(self)
        lineEdit_RFID.setText(user_to_edit.rfid)
        layout.addWidget(label3)
        layout.addWidget(lineEdit_RFID)

        okButton = QPushButton('OK')
        layout.addWidget(okButton)

        field = []
        field.append(lineEdit_Name)
        field.append(lineEdit_Email)
        field.append(lineEdit_RFID)
        okButton.clicked.connect(lambda: self.onDialogEditUserSaved(dialog, user_to_edit, field))

        dialog.setLayout(layout)
        dialog.show()

    def onDialogEditUserSaved(self, dialog, oldUser: User, field):
        name = field[0].text()
        email = field[1].text()
        rfid = field[2].text()

        updatedUser = User(oldUser.user_id, name, oldUser.registered_on, email, rfid)
        self.userDAO.updateUser(updatedUser)
        dialog.close()
        self.loadAllUsers()

    def dialog_DeleteUser(self):
        try:
            user_id = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 0).text()
            user_name = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 1).text()
        except AttributeError:
            self.displayErrorNoSpecificRow()
            return
        user_to_delete = self.userDAO.getUserFromID(user_id)
        if (user_to_delete == None):
            self.displayErrorNoID()
            return

        warningText = "Do you want to delete the selected user?" + "\n\nID: " + str(user_id) + "\nName: " + str(user_name)
        buttonReply = QMessageBox.question(self, "Warning", warningText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.userDAO.deleteUser(user_to_delete)
            self.loadAllUsers()
    
    # Error Dialogs
    def displayErrorNoSpecificRow(self):
        errorDialog = QErrorMessage(self)
        errorDialog.showMessage("Please select specific row first")
    def displayErrorNoID(self):
        errorDialog = QErrorMessage(self)
        errorDialog.showMessage("Could not find item for this ID")

    '''
    RETURN BOOK FUNCTIONS
    '''
    def dialog_ReturnBook(self):
        self.returnDialog = QDialog(self)
        self.returnDialog.setWindowTitle("Scan or Enter Book ID")
        self.returnDialog.resize(630, 150)
        layout = QVBoxLayout()

        label1 = QLabel(self)
        label1.setText("Book ID: ")
        id_textBox = QLineEdit(self)
        layout.addWidget(label1)
        layout.addWidget(id_textBox)

        # Camera scanner
        self.camIDscan = CameraScanner(self, 1280, 720, 10, 0)
        camViewWidget = CameraViewerWidget(self)
        layout.addWidget(camViewWidget)
        self.camUpdatetimer = QtCore.QTimer(self)
        self.camUpdatetimer.timeout.connect(lambda: self.updateCamImage(camViewWidget,self.camIDscan))
        self.camUpdatetimer.start(1)
        self.camIDscan.setDaemon(True)
        self.camIDscan.start()

        okButton = QPushButton('Next')
        layout.addWidget(okButton)
        okButton.clicked.connect(lambda: self.returnBook(id_textBox))

        self.returnDialog.setLayout(layout)
        self.returnDialog.show()

    def returnBook(self, id_textBox=None,id=None):
        self.camUpdatetimer.stop()
        self.camIDscan.pause()

        if id_textBox is None:  # Input via camera
            print("return id " + str(id))
            borrowID_to_return = self.bookCirculationDAO.getBorrowIDFromBookID(id)
        else:   # Manual textbox input
            borrowID_to_return = self.bookCirculationDAO.getBorrowIDFromBookID(id_textBox.text())

        if (borrowID_to_return == None):
            self.displayErrorNoID()
            print("Return failed : ID not found in Borrow Circulation")
        else:
            self.bookCirculationDAO.returnBook(borrowID_to_return)
        self.returnDialog.close()
        Thread(target=self.init_element).run()

    def updateCamImage(self,camViewWidget,camIDScan):
        self.window_width_idScan = 630
        self.window_height_idScan = 600
        if not camIDScan.getImageQueue().empty():
            frame = camIDScan.getImageQueue().get()
            img = frame["img"]
            try:
                img_height, img_width, img_colors = img.shape
            except AttributeError:
                return
            scale_w = float(self.window_width_idScan) / float(img_width)
            scale_h = float(self.window_height_idScan) / float(img_height)
            scale = min([scale_w, scale_h])
            if scale == 0:
                scale = 1
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QImage(img.data, width, height, bpl, QImage.Format_RGB888).mirrored(True, False)
            camViewWidget.setImage(image)

    def sendNotificationToAllOnBorrow(self):
        warningText = "Do you want to notify user?"
        buttonReply = QMessageBox.question(self, "Information", warningText, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            Thread(target=self.notificationDAO.notifyAllOnBorrow).start()

    '''
    SEARCH FUNCTION 
    '''
    def searchUser(self):
        keyword = self.ui.lineEditUsers_SearchBox.text()
        self.userTableAdapter.addUsers(self.userDAO.searchUser(keyword))
    def searchBooks(self):
        keyword = self.ui.lineEditBooks_SearchBox.text()
        Thread(target=self.booksTableAdapter.addBooks,args=[self.bookDAO.searchBook(keyword)]).run()
    def searchHistory(self):
        keyword = self.ui.lineEditHistory_SearchBox.text()
        self.historyTableAdapter.addCirculations(self.bookCirculationDAO.searchHistory(keyword))
    def searchOnBorrow(self):
        keyword = self.ui.lineEditIssue_SearchBox.text()
        self.onBorrowTableAdapter.addCirculations(self.bookCirculationDAO.searchOnBorrow(keyword))

# Catch Error and display through MessageBox
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)
old_hook = sys.excepthook
sys.excepthook = catch_exceptions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SmartLibUi()
    w.show()
    sys.exit(app.exec_())