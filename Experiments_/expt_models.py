import sqlite3
from accs_.models import AuthUtils


class ExptUtils:

    def __init__(self) -> None:
        self.sqlite = sqlite3
        self.auth = AuthUtils()

    def get_cur(self):
        db = self.sqlite.connect('auth.db')
        return db, db.cursor()

    def shut(self, db):
        db.commit()
        db.close()

    def create_tables(self):
        db, cursor = self.get_cur()
        # Experiments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT NOT NULL,
                group_name TEXT NOT NULL,
                aim TEXT NOT NULL,
                procedure TEXT NOT NULL,
                status TEXT NOT NULL,
                due_date TEXT NOT NULL,
                teacher TEXT NOT NULL
            )
        ''')

        # Results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL,
                experiment_name TEXT NOT NULL,
                student_name TEXT NOT NULL,
                student_username TEXT NOT NULL,
                result TEXT
            )
        ''')
        self.shut(db)

    def add_experiment(self, name, group, aim, procedure, due_date, status, teacher):
        db, cursor = self.get_cur()
        cursor.execute('''
            INSERT INTO experiments (experiment_name, group_name, aim, procedure, status, due_date, teacher)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, group, aim, procedure, status, due_date, teacher))
        self.shut(db)

    def delete_experiment(self, experiment_name):
        db, cursor = self.get_cur()
        cursor.execute('DELETE FROM experiments WHERE experiment_name = ?', (experiment_name,))
        cursor.execute('DELETE FROM results WHERE experiment_name = ?', (experiment_name,))
        self.shut(db)

    def get_experiments_by_teacher(self, teacher):
        db, cursor = self.get_cur()
        cursor.execute('SELECT * FROM experiments WHERE teacher = ?', (teacher,))
        rows = cursor.fetchall()
        self.shut(db)
        return rows

    def get_experiments_by_group(self, group_name):
        db, cursor = self.get_cur()
        cursor.execute('SELECT * FROM experiments WHERE group_name = ?', (group_name,))
        rows = cursor.fetchall()
        self.shut(db)
        return rows

    def get_experiment(self, experiment_name):
        db, cursor = self.get_cur()
        cursor.execute('SELECT * FROM experiments WHERE experiment_name = ?', (experiment_name,))
        result = cursor.fetchone()
        self.shut(db)
        return result

    def update_status(self, experiment_name, new_status):
        db, cursor = self.get_cur()
        cursor.execute('UPDATE experiments SET status = ? WHERE experiment_name = ?', (new_status, experiment_name))
        self.shut(db)

    def add_result(self, group_name, experiment_name, student_name, username, result):
        db, cursor = self.get_cur()
        cursor.execute('''
            INSERT INTO results (group_name, experiment_name, student_name, student_username, result)
            VALUES (?, ?, ?, ?, ?)
        ''', (group_name, experiment_name, student_name, username, result))
        self.shut(db)

    def update_result(self, group_name, experiment_name, username, result):
        db, cursor = self.get_cur()
        cursor.execute('''
            UPDATE results
            SET result = ?
            WHERE group_name = ? AND experiment_name = ? AND student_username = ?
        ''', (result, group_name, experiment_name, username))
        self.shut(db)

    def get_result(self, group_name, experiment_name, username):
        db, cursor = self.get_cur()
        cursor.execute('''
            SELECT result FROM results
            WHERE group_name = ? AND experiment_name = ? AND student_username = ?
        ''', (group_name, experiment_name, username))
        res = cursor.fetchone()
        self.shut(db)
        return res[0] if res else None

    def get_results_for_experiment(self, experiment_name):
        db, cursor = self.get_cur()
        cursor.execute('SELECT student_name, student_username, result FROM results WHERE experiment_name = ?', (experiment_name,))
        rows = cursor.fetchall()
        self.shut(db)
        return rows
