import os
from misc_ import home
from misc_ import auth
from accs_.models import AuthUtils
from accs_.login_ui import login_handler
from accs_.signup_ui import SignUpHandler
from menu.ui import MenuInterface
from grp_.lab_ui import LabGroupHandler
from Experiments_.expt_ui import ExperimentHandler
import time

auth_utils = AuthUtils()
auth_utils.create_user_table()
sign_up_handler = SignUpHandler()
labHandler = LabGroupHandler()
menuHandler = MenuInterface()
expHandler = ExperimentHandler()
#manageHandler = AccManageInterface()
CURR_SLIDE: str = "HOME"
SLIDES: dict = {
    "HOME": home.handler,
    "AUTH": auth.handler,
    "LOGIN": login_handler,
    "SIGNUP": sign_up_handler.main_display,
    "MENU": menuHandler.MenuUI,
    "LAB_GROUPS": labHandler.handler,
    "EXPERIMENTS": expHandler.handler
}

while True:
  try:
    print("\033[0m")
    os.system("clear")
    next = SLIDES[CURR_SLIDE]()
    if next[0] == "MENU":
      menuHandler.set_logged_in_user(next[1])
    #elif next[0] == "MANAGE_ACCOUNT":
    #manageHandler.logged_in_user = menuHandler.logged_in_user
    elif next[0] == "LAB_GROUPS":
      labHandler.set_logged_in_user(menuHandler.logged_in_user)
    elif next[0] == "EXPERIMENTS":
      expHandler.set_logged_in_user(menuHandler.logged_in_user)
    CURR_SLIDE = next[0]
  except KeyboardInterrupt:
    print("Force Shutting.....")
    break
