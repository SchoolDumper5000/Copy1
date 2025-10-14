import sqlite3


class AuthUtils:

  def __init__(self) -> None:
    self.sqlite = sqlite3

  def get_cur(self):
    db = self.sqlite.connect('auth.db')
    return db, db.cursor()

  def shut(self, db):
    db.commit()
    db.close()

  def create_user_table(self):
    db, cursor = self.get_cur()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        acctype TEXT NOT NULL,
        name TEXT NOT NULL
      )
    ''')
    self.shut(db)

  def user_exists(self, username) -> bool:
    db, cursor = self.get_cur()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username, ))
    user = cursor.fetchone()
    if user is None:
      return False
    else:
      return True

  def get_details(self, username=None):
    db, cursor = self.get_cur()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username, ))
    result = cursor.fetchone()
    if result is not None:
      return (True,result[0], result[1], result[3], result[4])
    elif result is None:
      return ( False )
      

  def add_demo_accounts(self):
    db, cursor = self.get_cur()
    cursor.execute(
        'INSERT INTO users (username, password, acctype) VALUES (?, ?)',
        ('admin', 'admin', 'admin'))
    self.shut(db)

  def verify_user(self, username, password) -> bool:
    db, cursor = self.get_cur()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                   (username, password))
    user = cursor.fetchone()
    return (user is not None)

  def add_user(self, username, password, acctype, name):
    db, cursor = self.get_cur()
    cursor.execute(
        'INSERT INTO users (username, password, acctype,name) VALUES (?, ?, ?, ?)',
        (username, password, acctype, name))
    self.shut(db)

  def del_user(self, username, passwrod):
    db, cursor = self.get_cur()
    if self.verify_user(username, passwrod):
      cursor.execute('DELETE FROM users WHERE username = ? AND password = ?',
                     (username, passwrod))
      self.shut(db)
      return True
    else:
      return False

  def update_name(self, username, password, name):
    if self.verify_user(username, password):
      db, cursor = self.get_cur()
      cursor.execute('UPDATE users SET name = ? WHERE username = ?',
                     (name, username))
      self.shut(db)
      return True

  def update_password(self, username, password, new_password):
    if self.verify_user(username, password):
      db, cursor = self.get_cur()
      cursor.execute('UPDATE users SET password = ? WHERE username = ?',
                     (new_password, username))
      self.shut(db)
      return True
    else :
      return False

  
  #def
