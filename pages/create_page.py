from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox

class CreatePage(QWidget):
    def __init__(self, db, go_back_callback):
        super().__init__()
        self.db = db
        self.go_back_callback = go_back_callback

        # 레이아웃
        layout = QVBoxLayout()

        # 제목 입력
        layout.addWidget(QLabel("제목"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        # 작성자 입력
        layout.addWidget(QLabel("작성자"))
        self.author_input = QLineEdit()
        layout.addWidget(self.author_input)

        # 내용 입력
        layout.addWidget(QLabel("내용"))
        self.content_input = QTextEdit()
        layout.addWidget(self.content_input)

        # 저장 버튼
        save_btn = QPushButton("저장")
        save_btn.clicked.connect(self.save_post)
        layout.addWidget(save_btn)

        # 취소 버튼
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.go_back_callback)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)

    def save_post(self):
        title = self.title_input.text()
        author = self.author_input.text()
        content = self.content_input.toPlainText()

        # 유효성 검사
        if not title or not content:
            QMessageBox.warning(self, "오류", "제목과 내용은 반드시 입력해야 합니다!")
            return

        # DB 저장
        self.db.create_post(title, content, author)

        QMessageBox.information(self, "성공", "게시글이 저장되었습니다!")

        # 저장 후 목록 페이지로 돌아가기
        self.go_back_callback()
