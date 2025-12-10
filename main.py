from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from core.db_manage import DBManager
from pages.main_page import MainPage
from pages.create_page import CreatePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide 게시판")

        self.db = DBManager()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # MainPage 생성
        self.main_page = MainPage(self.db)
        self.main_page.open_create.connect(self.open_create_page)
        # (DetailPage는 나중에 연결)
        self.stack.addWidget(self.main_page)

        # CreatePage 생성
        self.create_page = CreatePage(self.db, self.go_to_main)

    def open_create_page(self):
        self.stack.addWidget(self.create_page)
        self.stack.setCurrentWidget(self.create_page)

    def go_to_main(self):
        # 메인으로 돌아오면 목록 새로고침
        self.main_page.refresh()
        self.stack.setCurrentWidget(self.main_page)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
