from accs_.models import AuthUtils
from misc_.ui import Messages
import os
import getpass
import survey
import time
from termcolor import colored


class AccManageInterface:

  def __init__(self) -> None:
    self.auth = AuthUtils()
    self.gp = getpass
    self.logged_in_user: None = None
    self.ui = Messages()
    self.creds = None
    self.color = colored

  def change_name(self):
    breakit = False
    while not breakit:
      os.system("clear")
      self.ui.default_message(
          f"Ｃｕｒｒｅｎｔ ｎａｍｅ ｓｅｔ ｔｏ：'{self.creds[4]}'\nＴｏ ｇｏ ｂａｃｋ ｐｒｅｓｓ ［ ＥＮＴＥＲ ］")
      name = input(self.color("> Ｎａｍｅ :", "white"))
      self.ui.primary_line("grey", 80)
      time.sleep(1)
      if name == " " or name == "": break
      names = name.split()
      for e in names:
        if not e.isalpha():
          self.ui.error_message(
              "Ｓｔａｔｕｓ： Ｃｈａｎｇｉｎｇ Ｆａｉｌｅｄ\nＴｈｅ ｎａｍｅ ｃａｎ ｏｎｌｙ ｃｏｎｔａｉｎ ａｌｐｈａｂｅｔｓ")
          break
        else:
          self.ui.success_message("Ｓｔａｔｕｓ： Ｎａｍｅ ｕｐｄａｔｅｄ ｓｕｃｃｅｓｓｆｕｌｌｙ！")
          breakit = True
          self.auth.update_name(self.logged_in_user, self.creds[2], name)
          break

  def change_password(self):
    while True:

      os.system("clear")
      self.ui.default_message("                ＲＥＳＥＴ ＰＡＳＳＷＯＲＤ")
      self.ui.leave_line()
      print("Ｔｏ ｇｏ ｂａｃｋ ｐｒｅｓｓ ［ ＥＮＴＥＲ ］")
      self.ui.leave_line()
      self.ui.primary_line("grey",80)
      old_password = self.gp.getpass("> Ｏｌｄ ｐａｓｓｗｏｒｄ :")
      if old_password == "" or old_password == " ":break
      self.ui.primary_line("grey", 80)
      res = self.auth.verify_user(self.logged_in_user, old_password)
      if res:
        os.system('clear')
        self.ui.default_message("                ＲＥＳＥＴ ＰＡＳＳＷＯＲＤ")
        new_password = self.gp.getpass("> Ｎｅｗ ｐａｓｓｗｏｒｄ :")
        self.ui.leave_line()
        confirm_password = self.gp.getpass("> Ｃｏｎｆｉｒｍ ｐａｓｓｗｏｒｄ :")
  
        if new_password == confirm_password:
          self.auth.update_password(self.logged_in_user, old_password,
                                    new_password)
  
          self.ui.success_message("Ｓｔａｔｕｓ： ｐａｓｓｗｏｒｄ ｕｐｄａｔｅｄ ｓｕｃｃｅｓｓｆｕｌｌｙ！")
          break
        else:
          self.ui.error_message("Ｓｔａｔｕｓ： Ｅｎｔｅｒｅｄ ｐａｓｓｗｏｒｄｓ ｄｏ ｎｏｔ ｍａｔｃｈ")
          break
        
      else:
        self.ui.error_message(
            "Ｓｔａｔｕｓ： Ｐａｓｓｗｏｒｄ ｄｏｅｓ ｎｏｔ ｍａｔｃｈ") 

  def delete_account(self):
    os.system("clear")
    options = ["Ｙｅｓ\n", "Ｎｏ\n"]
    index = survey.routines.select('\nＳＥＬＥＣＴ Ａ ＯＰＥＲＡＴＩＯＮ:\n',
                                   options=options,
                                   focus_mark='>',
                                   evade_color=survey.colors.basic('white'),
                                   insearch_color=survey.colors.basic('white'))
    if index == 0:
      os.system("clear")
      self.ui.default_message("Ｅｎｔｅｒ ｔｈｅ ｐａｓｓｗｏｒｄ ｔｏ ｄｅｌｅｔｅ ｔｈｅ ａｃｃｏｕｎｔ")
      password = self.gp.getpass("> Ｐａｓｓｗｏｒｄ :")
      self.ui.primary_line("grey", 80)
      time.sleep(1)
      ret = self.auth.del_user(self.logged_in_user, password)
      if ret:
        self.ui.error_message("Ｓｔａｔｕｓ： Ａｃｃｏｕｎｔ ｄｅｌｅｔｅｄ ｓｕｃｃｅｓｓｆｕｌｌｙ！")
        return ("AUTH", )
      elif not ret:
        self.ui.error_message(
            "Ｓｔａｔｕｓ： Ａｃｃｏｕｎｔ ｄｅｌｅｔｉｏｎ ｆａｉｌｅｄ\nＲｅａｓｏｎ： ｉｎｃｏｒｒｅｃｔ ｐａｓｓｗｏｒｄ")
        return ("MANAGE_ACCOUNT", self.logged_in_user)
    else:
      return ("MANAGE_ACCOUNT", self.logged_in_user)

  def handler(self) -> tuple:
    os.system('clear')
    self.creds = self.auth.get_details(self.logged_in_user)

    print("""
---------------------------------------------------------------------------------------------------------------

─█▀▀█ ░█▀▀█ ░█▀▀█ ░█▀▀▀█ ░█─░█ ░█▄─░█ ▀▀█▀▀ 　 ░█▀▄▀█ ─█▀▀█ ░█▄─░█ ─█▀▀█ ░█▀▀█ ░█▀▀▀ ░█▀▄▀█ ░█▀▀▀ ░█▄─░█ ▀▀█▀▀ 
░█▄▄█ ░█─── ░█─── ░█──░█ ░█─░█ ░█░█░█ ─░█── 　 ░█░█░█ ░█▄▄█ ░█░█░█ ░█▄▄█ ░█─▄▄ ░█▀▀▀ ░█░█░█ ░█▀▀▀ ░█░█░█ ─░█── 
░█─░█ ░█▄▄█ ░█▄▄█ ░█▄▄▄█ ─▀▄▄▀ ░█──▀█ ─░█── 　 ░█──░█ ░█─░█ ░█──▀█ ░█─░█ ░█▄▄█ ░█▄▄▄ ░█──░█ ░█▄▄▄ ░█──▀█ ─░█──

---------------------------------------------------------------------------------------------------------------


""")
    self.ui.primary_line("grey", 100)

    print(
        f"""\nＵＳＥＲＮＡＭＥ: {self.creds[2]}\n\nＮＡＭＥ: {self.creds[4]}\n\nＡＣＣＯＵＮＴ-ＴＹＰＥ: {self.creds[3]}\n\nＵＳＥＲ－ＩＤ: {self.creds[1]}
    
    """)
    self.ui.primary_line("grey", 100)
    options = [
        "Ｃｈａｎｇｅ Ｐａｓｓｗｏｒｄ\n", "Ｃｈａｎｇｅ Ｎａｍｅ\n", "Ｄｅｌｅｔｅ Ａｃｃｏｕｎｔ\n", "Ｇｏ Ｂａｃｋ\n"
    ]
    index = survey.routines.select('\nＳＥＬＥＣＴ Ａ ＯＰＥＲＡＴＩＯＮ:\n',
                                   options=options,
                                   focus_mark='>',
                                   evade_color=survey.colors.basic('white'),
                                   insearch_color=survey.colors.basic('white'))

    if index == 3:
      return ("MENU", self.logged_in_user)
    elif index == 0:
      self.change_password()
      self.creds = self.auth.get_details(self.logged_in_user)
      return ("MANAGE_ACCOUNT", self.logged_in_user)
    elif index == 1:
      self.change_name()
      self.creds = self.auth.get_details(self.logged_in_user)
      return ("MANAGE_ACCOUNT", self.logged_in_user)
    elif index == 2:
      ret = self.delete_account()
      return ret
