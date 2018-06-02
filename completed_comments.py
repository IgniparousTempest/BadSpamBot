import sqlite3


class Comments(object):
    def __init__(self):
        self.conn = sqlite3.connect('comments.db')
        c = self.conn.cursor()

        sql = 'create table if not exists Comments (id integer)'
        c.execute(sql)
        c.close()

    def add(self, comment_id):
        c = self.conn.cursor()
        c.execute('INSERT INTO Comments (id) VALUES (?)', (comment_id,))
        self.conn.commit()
        c.close()

    def exists(self, comment_id) -> bool:
        c = self.conn.cursor()
        c.execute('SELECT * FROM Comments WHERE (id=?)', (comment_id,))
        result = c.fetchone()
        c.close()
        return result is not None

    def close(self):
        self.conn.close()
