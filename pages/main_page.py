from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class MainPage(QWidget):
    # 상세 페이지로 이동할때 씀! post_id를 보낸다!
    open_detail = Signal(int)

    # 작성 페이지로 이동하는 url(?)
    open_create = Signal()
    # 삭제버튼
    delete_post = Signal(int)

    def __init__(self, db):
        super().__init__()
        self.db = db

        layout = QVBoxLayout()

        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "제목", "작성자", "삭제"])
        
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 80)
        self.table.resizeRowsToContents()

        self.table.cellDoubleClicked.connect(self.handle_row_double_click)
        layout.addWidget(self.table)

        # 버튼 영역
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("글쓰기")
        create_btn.clicked.connect(self.open_create.emit)
        btn_layout.addWidget(create_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        # 페이지가 열릴때 리스트 새로고침
        self.refresh()

    def handle_row_double_click(self, row, column):
        post_id = int(self.table.item(row, 0).text())
        self.open_detail.emit(post_id)

    def refresh(self):
        # DB에서 게시글 목록을 가져와 테이블에 반영
        posts = self.db.get_all_posts()
        self.table.setRowCount(len(posts))

        for row, post in enumerate(posts):
            post_id, title, content, author, created, updated = post

            self.table.setItem(row, 0, QTableWidgetItem(str(post_id)))
            self.table.setItem(row, 1, QTableWidgetItem(title))
            self.table.setItem(row, 2, QTableWidgetItem(author))

            # 삭제버튼 만들기
            delete_btn = QPushButton("삭제")
            delete_btn.clicked.connect(
                lambda _, pid=post_id: self.delete_post.emit(pid)
            )
            self.table.setCellWidget(row, 3, delete_btn)
