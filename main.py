from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from core.db_manage import DBManager
from pages.main_page import MainPage
from pages.create_page import CreatePage
from pages.detail_page import DetailPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide 게시판")

        self.db = DBManager()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # MainPage
        self.main_page = MainPage(self.db)
        self.main_page.open_create.connect(self.open_create_page)
        self.main_page.open_detail.connect(self.open_detail_page)

        self.stack.addWidget(self.main_page)      
        self.stack.setCurrentWidget(self.main_page)

        # CreatePage
        self.create_page = CreatePage(self.db, self.go_to_main)
        self.stack.addWidget(self.create_page)    

    def open_create_page(self):
        self.stack.setCurrentWidget(self.create_page)

    def go_to_main(self):
        self.main_page.refresh()
        self.stack.setCurrentWidget(self.main_page)

    def open_detail_page(self, post_id):
        self.detail_page = DetailPage(self.db, post_id)
        self.detail_page.back.connect(self.show_main)
        self.detail_page.deleted.connect(self.show_main)

        self.stack.addWidget(self.detail_page)
        self.stack.setCurrentWidget(self.detail_page)

    def show_main(self):
        self.main_page.refresh()
        self.stack.setCurrentWidget(self.main_page)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
