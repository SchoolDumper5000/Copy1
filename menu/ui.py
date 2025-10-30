import misc_.ui as ui
import time
import survey
import os
from accs_.models import AuthUtils

class MenuInterface:

  def __init__(self) -> None:
    self.ui = ui.Messages()
    self.logged_in_user = None 
    self.creds = None
    self.auth = AuthUtils()

  def set_logged_in_user(self, user):
    self.logged_in_user = user
    self.creds = self.auth.get_details(self.logged_in_user)
    

  def MenuUI(self) -> str:
    self.ui.default_message("                          ＭＡＩＮ ＭＥＮＵ")
    self.ui.leave_line()
    print(f"""
ＷＥＬＣＯＭＥ ＢＡＣＫ {self.creds[4]}, ＧＯＯＤ ＴＯ ＨＡＶＥ ＹＯＵ ＡＧＡＩＮ！
    """)
    self.ui.primary_line("grey", 90)
    options = [
        'Ｍａｎａｇｅ Ａｃｃｏｕｎｔ\n', 'Ｌａｂ Ｇｒｏｕｐs\n', 'Ｅｘｐｅｒｉｍｅｎｔｓ\n', 'Ｌｏｇ Ｏｕｔ\n'
    ]
    index = survey.routines.select(
        '\nＰｌｅａｓｅ  ｓｅｌｅｃｔ  ｏｎｅ  ｏｆ  ｔｈｅ  ｆｏｌｌｏｗｉｎｇ  ｏｐｔｉｏｎｓ:\n',
        options=options,
        focus_mark='> ',
        evade_color=survey.colors.basic('white'),
        insearch_color=survey.colors.basic('white'))
    if index == 1:
      os.system('clear')
      return ("LAB_GROUPS", self.logged_in_user)
    elif index == 2:
      os.system('clear')
      return ("EXPERIMENTS", self.logged_in_user)
    if index == 3:
      os.system('clear')
      self.ui.indicator_message("                  Ｌｏｇｇｉｎｇ Ｏｕｔ")
      return ("AUTH",)
    elif index == 0:
      os.system('clear')
      return ("MANAGE_ACCOUNT",)
    
    time.sleep(10)
