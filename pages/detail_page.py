from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,QHBoxLayout, QMessageBox
from PySide6.QtCore import Signal

class DetailPage(QWidget):
    back = Signal()
    edit = Signal(int)
    deleted = Signal()

    def __init__(self, db, post_id):
        super().__init__()
        self.db = db
        self.post_id = post_id

        # DB에서 작성글 정보 가져오기
        post = self.db.get_post(post_id)

        layout = QVBoxLayout()

        self.title_label = QLabel(f"제목 : {post[1]}")
        self.author_label = QLabel(f"작성자 : {post[3]}")
        self.content = QTextEdit()
        self.content.setText(post[2])
        self.content.setReadOnly(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.author_label)
        layout.addWidget(self.content)


        btns = QHBoxLayout()

        back_btn = QPushButton("돌아가기")
        back_btn.clicked.connect(self.back.emit)

        edit_btn = QPushButton("수정")
        edit_btn.clicked.connect(lambda: self.edit.emit(self.post_id))

        delete_btn = QPushButton("삭제")
        delete_btn.clicked.connect(self.handle_delete)

        btns.addWidget(back_btn)
        btns.addWidget(edit_btn)
        btns.addWidget(delete_btn)

        layout.addLayout(btns)
        self.setLayout(layout)

    def handle_delete(self):
        reply = QMessageBox.question(
            self, 
            "삭제 확인",
            "정말 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No 
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_post(self.post_id)
            QMessageBox.information(self,"삭제됨", "정상적으로 삭제되었습니다!")
            self.deleted.emit()    