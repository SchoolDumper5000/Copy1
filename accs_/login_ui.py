from termcolor import colored
from accs_.models import AuthUtils
import getpass
import os
from misc_.ui import Messages

ui = Messages()


def login_handler():
    print("""
                ------------------------------------------
                |     ▒█░░░ ▒█▀▀▀█ ▒█▀▀█ ▀█▀ ▒█▄░▒█      |
                |     ▒█░░░ ▒█░░▒█ ▒█░▄▄ ▒█░ ▒█▒█▒█      |
                |     ▒█▄▄█ ▒█▄▄▄█ ▒█▄▄█ ▄█▄ ▒█░░▀█      |
                ------------------------------------------


""")
    choice = ui.input_message("Ｗｏｕｌｄ ｙｏｕ ｌｉｋｅ ｔｏ ｏｐｅｎ ｔｈｅ ｌｏｇｉｎ ｆｏｒｍ [Y/N]: ")

    if choice.lower().startswith("y"):
        os.system("clear")
        ui.primary_line("grey", 70)
        print(colored("        ＥＮＴＥＲ ＹＯＵＲ ＣＲＥＤＥＮＴＩＡＬＳ ＢＥＬＯＷ", "white"))
        ui.primary_line("grey", 70)
        username = ""
        password = ""
        ui.leave_line()
        ui.leave_line()
        ui.primary_line("grey", 70)
        username = input(colored("Ｕｓｅｒｎａｍｅ    :", "white"))
        if username == "": return ("LOGIN", )
        ui.primary_line("grey", 70)
        ui.leave_line()
        ui.primary_line("grey", 70)
        password = getpass.getpass(colored("Ｐａｓｓｗｏｒｄ    :", "white"))
        ui.primary_line("grey", 70)
        ui.leave_line()
        os.system('clear')
        ui.indicator_message("            Ａｕｔｈｅｎｔｉｃａｔｉｎｇ Ｉｎｆｏｒｍａｔｉｏｎ")
        auth_obj = AuthUtils()
        user_exists = auth_obj.user_exists(username)
        if not user_exists:
            os.system("clear")
            ui.error_message(
                f"""Ｓｔａｔｕｓ： Ｌｏｇｉｎ Ｆａｉｌｅｄ\nＲｅａｓｏｎ： Ｔｈｅ ｕｓｅｒｎａｍｅ ＂{username}＂ ｄｏｅｓ ｎｏｔ ｅｘｉｓｔ"""
            )
            return ("LOGIN", )
        elif user_exists:
            os.system("clear")
            matched = auth_obj.verify_user(username, password)
            if matched:
                ui.success_message("            Ｓｔａｔｕｓ： Ｌｏｇｉｎ ｓｕｃｃｅｓｓｆｕｌ")
                return ("MENU", username)
            else:
                os.system("clear")
                ui.error_message(
                    "Ｓｔａｔｕｓ： Ｌｏｇｉｎ Ｆａｉｌｅｄ\nＲｅａｓｏｎ： Ｉｎｖａｌｉｄ Ｐａｓｓｗｏｒｄ")
                return ("LOGIN", )

    else:
        return ("AUTH", )
