import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from EZLib_LibrarianUI import Ui_MainWindow

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
        self.ui.pushButton_4.clicked.connect(self.dialog_AddBook)

        '''
        TAB: BOOKS
        '''
        self.ui.buttonBooks_Add.clicked.connect(self.dialog_AddBook)
        #self.ui.buttonBooks_Edit.clicked.connect()
        #self.ui.buttonBooks_Delete.clicked.connect()
        #self.ui.buttonBooks_Go.clicked.connect()

        '''
        TAB: USERS
        '''
        #self.ui.buttonUsers_Add.clicked.connect(self.dialog_AddBook)
        #self.ui.buttonUsers_Edit.clicked.connect()
        #self.ui.buttonUsers_Delete.clicked.connect()
        #self.ui.buttonUsers_Go.clicked.connect()

        '''
        TAB: ISSUE
        '''
        #self.ui.buttonBooks_Add.clicked.connect(self.dialog_AddBook)
        #self.ui.buttonBooks_Edit.clicked.connect()
        #self.ui.buttonBooks_Delete.clicked.connect()
        #self.ui.buttonBooks_Go.clicked.connect()

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
        self.ui.tabWidget.setCurrentIndex(3)

    # Add/Edit/Delete Dialog
    def dialog_AddBook(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        dialog.setWindowTitle("Add Book")
        dialog.resize(630, 150)
        
        label1 = QLabel(self)
        label1.setText("Title: ")
        textBox1 = QLineEdit(self)
        layout.addWidget(label1)
        layout.addWidget(textBox1)

        label2 = QLabel(self)
        label2.setText("ISBN: ")
        textBox2 = QLineEdit(self)
        layout.addWidget(label2)
        layout.addWidget(textBox2)

        label3 = QLabel(self)
        label3.setText("Author: ")
        textBox3 = QLineEdit(self)
        layout.addWidget(label3)
        layout.addWidget(textBox3)

        label4 = QLabel(self)
        label4.setText("Publisher: ")
        textBox4 = QLineEdit(self)
        layout.addWidget(label4)
        layout.addWidget(textBox4)

        closeButton = QPushButton('OK')
        closeButton.clicked.connect(dialog.close)
        layout.addWidget(closeButton)
        
        dialog.setLayout(layout)
        dialog.show()

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SmartLibUi()
    w.show()
    sys.exit(app.exec_())
