import sqlite3
from accs_.models import AuthUtils   


class LabUtils:

    def __init__(self) -> None:
        self.sqlite = sqlite3
        self.auth = AuthUtils()

    def get_cur(self):
        db = self.sqlite.connect('auth.db')   
        return db, db.cursor()

    def shut(self, db):
        db.commit()
        db.close()

    def create_lab_table(self):
        db, cursor = self.get_cur()
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS lab_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            username TEXT NOT NULL,
            role TEXT NOT NULL
          )
        ''')
        self.shut(db)

    def add_group(self, group_name, teacher_username):
        """Create a new group and add creator as Teacher"""
        db, cursor = self.get_cur()
        cursor.execute(
            'INSERT INTO lab_groups (group_name, username, role) VALUES (?, ?, ?)',
            (group_name, teacher_username, "Teacher")
        )
        self.shut(db)

    def delete_group(self, group_name):
        db, cursor = self.get_cur()
        cursor.execute('DELETE FROM lab_groups WHERE group_name = ?', (group_name,))
        self.shut(db)

    def add_member(self, group_name, username):
        """Add a member as Student if they exist in users table"""
        if not self.auth.user_exists(username):
            return False   # user not found
        db, cursor = self.get_cur()
        cursor.execute(
            'INSERT INTO lab_groups (group_name, username, role) VALUES (?, ?, ?)',
            (group_name, username, "Student")
        )
        self.shut(db)
        return True

    def get_groups_by_user(self, username):
        """All groups where this user is a member"""
        db, cursor = self.get_cur()
        cursor.execute('SELECT * FROM lab_groups WHERE username = ?', (username,))
        results = cursor.fetchall()
        self.shut(db)
        return results

    def get_members(self, group_name):
        """List all members of a group"""
        db, cursor = self.get_cur()
        cursor.execute('SELECT username, role FROM lab_groups WHERE group_name = ?', (group_name,))
        results = cursor.fetchall()
        self.shut(db)
        return results

    def get_all_groups(self):
        db, cursor = self.get_cur()
        cursor.execute('SELECT DISTINCT group_name FROM lab_groups')
        results = cursor.fetchall()
        self.shut(db)
        return [r[0] for r in results]
