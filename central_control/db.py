import pymysql


class DBUtil:
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host=host, user=user, password=password, port=3306, database=database)
        self.cursor = self.db.cursor()

    def close(self):
        if self.db and self.cursor:
            self.cursor.close()
            self.db.close()
        return True

    def query_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def query_all(self, sql, args=None):
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def update(self, sql, args=None):
        self.cursor.execute(sql, args)

    def insert(self, sql, args=None):
        self.cursor.executemany(sql, args)

    def commit(self):
        if self.db:
            self.db.commit()

    def rollback(self):
        if self.db:
            self.db.rollback()
