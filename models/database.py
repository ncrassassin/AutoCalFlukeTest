import sqlite3, time

class Database:
    def __init__(self, db_name='resources/test_results.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                          timestamp TEXT,
                          test_point TEXT,
                          expected REAL,
                          measured REAL,
                          error REAL,
                          result TEXT)''')
        self.conn.commit()

    def log_result(self, test_point, expected, measured, result):
        cursor = self.conn.cursor()
        error = measured - expected
        cursor.execute('INSERT INTO results VALUES (?,?,?,?,?,?)',
                       (time.strftime('%Y-%m-%d %H:%M:%S'), test_point, expected, measured, error, result))
        self.conn.commit()

    def close(self):
        self.conn.close()