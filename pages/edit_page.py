from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QMessageBox

class EditPage(QWidget):
    def __init__(self, db, post_id, on_done):
        super().__init__()
        self.db = db
        self.post_id = post_id
        self.on_done = on_done

        post = self.db.get_post(post_id)

        layout = QVBoxLayout()

        self.title_input = QLineEdit(post[1])
        self.content_input = QTextEdit(post[2])

        layout.addWidget(QLabel("제목"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("내용"))
        layout.addWidget(self.content_input)

        btns = QHBoxLayout()
        save_btn = QPushButton("저장")
        save_btn.clicked.connect(self.save_post)
        btns.addWidget(save_btn)

        layout.addLayout(btns)
        self.setLayout(layout)

    def save_post(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()

        if not title or not content:
            QMessageBox.warning(self, "경고!", "제목과 내용은 비워둘 수 없습니다!")
            return

        self.db.update_post(self.post_id, title, content)
        self.on_done()
