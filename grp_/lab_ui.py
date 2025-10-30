import os
import time
import survey
from termcolor import colored
from misc_.ui import Messages
from grp_.lab_models import LabUtils
from accs_.models import AuthUtils


class LabGroupHandler:

    def __init__(self, logged_in_user=None) -> None:
        self.ui = Messages()
        self.lab = LabUtils()
        self.lab.create_lab_table()
        self.logged_in_user = logged_in_user
        self.auth = AuthUtils()  # Added for role checking

    def set_logged_in_user(self, user):
        self.logged_in_user = user

    def create_group(self):
        os.system("clear")
        self.ui.default_message("Ｃｒｅａｔｅ Ａ Ｎｅｗ Ｌａｂ Ｇｒｏｕｐ")
        self.ui.leave_line()

        group_name = input(colored("> Ｇｒｏｕｐ Ｎａｍｅ :", "white"))
        self.ui.primary_line("grey", 80)
        time.sleep(1)

        if group_name.strip() == "":
            self.ui.error_message("Ｓｔａｔｕｓ： Ｇｒｏｕｐ ｎａｍｅ ｃａｎｎｏｔ ｂｅ ｅｍｐｔｙ")
            return ("MENU", self.logged_in_user)

        self.lab.add_group(group_name, self.logged_in_user)
        self.ui.success_message(
            f"Ｓｔａｔｕｓ： Ｇｒｏｕｐ '{group_name}' ｃｒｅａｔｅｄ ｗｉｔｈ {self.logged_in_user} ａｓ Ｔｅａｃｈｅｒ！"
        )

        while True:
            self.ui.default_message(
                "Ａｄｄ Ｓｔｕｄｅｎｔｓ ｔｏ ｔｈｅ ｇｒｏｕｐ\nＰｒｅｓｓ ＥＮＴＥＲ ｔｏ ｆｉｎｉｓｈ"
            )
            new_user = input(colored("> Ｕｓｅｒｎａｍｅ :", "white"))
            if new_user.strip() == "":
                break
            added = self.lab.add_member(group_name, new_user)
            if added:
                self.ui.success_message(
                    f"Ｓｔａｔｕｓ： {new_user} ａｄｄｅｄ ｔｏ ｇｒｏｕｐ ａｓ Ｓｔｕｄｅｎｔ"
                )
            else:
                self.ui.error_message(
                    f"Ｓｔａｔｕｓ： Ｆａｉｌｅｄ\nＲｅａｓｏｎ： Ｕｓｅｒ '{new_user}' ｄｏｅｓ ｎｏｔ ｅｘｉｓｔ"
                )

        return ("MENU", self.logged_in_user)

    def list_groups(self):
        os.system("clear")
        groups = self.lab.get_groups_by_user(self.logged_in_user)

        if not groups:
            print("Ｎｏ ｇｒｏｕｐｓ ｆｏｕｎｄ．")
        else:
            self.ui.primary_line("grey", 80)
            print(f"List of group you are a member of is below:")
            self.ui.primary_line("grey", 80)
            print("""
+------+-----------------------+
|  ID  |     GROUP NAME        |
+------+-----------------------+""")
            for m in groups:
                ID = colored(f"{str(m[0])}{' '*(4-len(str(m[0])))}", "grey")
                GROUPNAME = colored(f"{m[1]}{' '*(21-len(m[1]))}", "grey")
                print(f"| {ID} | {GROUPNAME} |")
                print("+------+-----------------------+")

        self.ui.primary_line("grey", 80)
        input("Ｐｒｅｓｓ ＥＮＴＥＲ ｔｏ ｇｏ ｂａｃｋ．．．")
        return ("MENU", self.logged_in_user)

    def view_members(self):
        os.system("clear")
        self.ui.default_message("Ｖｉｅｗ Ｇｒｏｕｐ Ｍｅｍｂｅｒｓ")
        all_groups = self.lab.get_all_groups()

        if not all_groups:
            print("Ｎｏ ｇｒｏｕｐｓ ｅｘｉｓｔ．")
            input("Ｐｒｅｓｓ ＥＮＴＥＲ ｔｏ ｇｏ ｂａｃｋ．．．")
            return ("MENU", self.logged_in_user)

        index = survey.routines.select(
            'Ｓｅｌｅｃｔ ａ ｇｒｏｕｐ ｔｏ ｖｉｅｗ ｍｅｍｂｅｒｓ:\n',
            options=[g + "\n" for g in all_groups],
            focus_mark='> ',
            evade_color=survey.colors.basic('white'),
            insearch_color=survey.colors.basic('white'))

        group_name = all_groups[index]
        members = self.lab.get_members(group_name)

        os.system("clear")
        self.ui.primary_line("grey", 80)
        print(f"List of group members in {group_name} is below:")
        self.ui.primary_line("grey", 80)
        print("""
+--------------------+-------------+
|     USERNAME       |    ROLE     |
+--------------------+-------------+""")
        for m in members:
            username = colored(f"{m[0]}{' '*(18-len(m[0]))}", "grey")
            role = colored(f"{m[1]}{' '*(11-len(m[1]))}", "grey")
            print(f"| {username} | {role} |")
            print("+--------------------+-------------+")
        self.ui.primary_line("grey", 80)
        self.ui.leave_line()
        input("Ｐｒｅｓｓ ＥＮＴＥＲ ｔｏ ｇｏ ｂａｃｋ．．．")

        return ("MENU", self.logged_in_user)

    def handler(self):
        os.system("clear")
        self.ui.default_message("\t\t\t\tＬａｂ Ｇｒｏｕｐ Ｍａｎａｇｅｍｅｎｔ")

        # 🔍 Determine user role
        creds = self.auth.get_details(self.logged_in_user)
        if creds and creds[3] == "Ｔｅａｃｈｅｒ":
            # Teacher view
            options = [
                "Ｃｒｅａｔｅ Ｎｅｗ Ｇｒｏｕｐ\n",
                "Ｖｉｅｗ Ｍｙ Ｇｒｏｕｐｓ\n",
                "Ｖｉｅｗ Ａｌｌ Ｇｒｏｕｐ Ｍｅｍｂｅｒｓ\n",
                "Ｂａｃｋ\n"
            ]
        else:
            # Student view (restricted)
            options = [
                "Ｖｉｅｗ Ｍｙ Ｇｒｏｕｐｓ\n",
                "Ｂａｃｋ\n"
            ]

        index = survey.routines.select(
            '\nＰｌｅａｓｅ ｓｅｌｅｃｔ ａｎ ｏｐｔｉｏｎ:\n',
            options=options,
            focus_mark='> ',
            evade_color=survey.colors.basic('white'),
            insearch_color=survey.colors.basic('white'))

        # Teacher options
        if creds and creds[3] == "Ｔｅａｃｈｅｒ":
            if index == 0:
                return self.create_group()
            elif index == 1:
                return self.list_groups()
            elif index == 2:
                return self.view_members()
            else:
                return ("MENU", self.logged_in_user)
        else:
            # Student options
            if index == 0:
                return self.list_groups()
            else:
                return ("MENU", self.logged_in_user)
