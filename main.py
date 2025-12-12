from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget,QMessageBox
from core.db_manage import DBManager
from pages.main_page import MainPage
from pages.create_page import CreatePage
from pages.detail_page import DetailPage
from pages.edit_page import EditPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide 게시판")

        self.resize(600, 800)

        self.db = DBManager()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # MainPage
        self.main_page = MainPage(self.db)
        self.main_page.open_create.connect(self.open_create_page)
        self.main_page.open_detail.connect(self.open_detail_page)
        self.main_page.delete_post.connect(self.delete_post_from_main)

        self.stack.addWidget(self.main_page)      
        self.stack.setCurrentWidget(self.main_page)

        # CreatePage
        self.create_page = CreatePage(self.db, self.go_to_main)
        self.stack.addWidget(self.create_page)    

    def open_create_page(self):
        self.create_page.clear_inputs()
        self.stack.addWidget(self.create_page)
        self.stack.setCurrentWidget(self.create_page)

    def go_to_main(self):
        self.main_page.refresh()
        self.stack.setCurrentWidget(self.main_page)

    def open_detail_page(self, post_id):
        self.detail_page = DetailPage(self.db, post_id)
        self.detail_page.edit.connect(self.open_edit_page)
        self.detail_page.back.connect(self.show_main)
        self.detail_page.deleted.connect(self.show_main)

        self.stack.addWidget(self.detail_page)
        self.stack.setCurrentWidget(self.detail_page)

    def show_main(self):
        self.main_page.refresh()
        self.stack.setCurrentWidget(self.main_page)

    def open_edit_page(self, post_id):
        self.edit_page = EditPage(self.db, post_id, self.show_main)
        self.stack.addWidget(self.edit_page)
        self.stack.setCurrentWidget(self.edit_page)
    
    def delete_post_from_main(self, post_id) :
        reply = QMessageBox.question(
            self,
            "경고!",
            "정말 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes :
            self.db.delete_post(post_id)
            QMessageBox.information(self, "삭제됨", "삭제되었습니다.")
            self.main_page.refresh()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
