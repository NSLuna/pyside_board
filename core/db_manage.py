import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path="db/database.sqlite3"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    def create_post(self, title, content, author):
        now = datetime.now().isoformat(" ").split(".")[0]
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO posts (title, content, author, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, content, author, now, now))
        conn.commit()
        conn.close()

    def get_all_posts(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_post(self, post_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def get_post(self, post_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("select * from posts where id = ?", (post_id,))
        post = cursor.fetchone()
        conn.close()
        return post

    def update_post(self, post_id, title, content):
        now = datetime.now().isoformat(" ").split(".")[0]
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE posts SET title=?, content=?, updated_at=? WHERE id=?
        """, (title, content, now, post_id))
        conn.commit()
        conn.close()

    def delete_post(self, post_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))
        conn.commit()
        conn.close()
