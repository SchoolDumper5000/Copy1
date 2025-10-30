import os
import time
import survey
from termcolor import colored
from misc_.ui import Messages
from Experiments_.expt_models import ExptUtils
from accs_.models import AuthUtils
from grp_.lab_models import LabUtils


class ExperimentHandler:

    def __init__(self, logged_in_user=None) -> None:
        self.ui = Messages()
        self.expt = ExptUtils()
        self.expt.create_tables()
        self.lab = LabUtils()
        self.auth = AuthUtils()
        self.logged_in_user = logged_in_user

    def set_logged_in_user(self, user):
        self.logged_in_user = user

    # ========== TEACHER SECTION ==========
    def create_experiment(self):
        os.system("clear")
        self.ui.default_message("Ｃｒｅａｔｅ Ａ Ｎｅｗ Ｅｘｐｅｒｉｍｅｎｔ")
        self.ui.leave_line()

        # 1️⃣ Filter groups: show only groups where this teacher is a member
        teacher_groups = self.lab.get_groups_by_user(self.logged_in_user)
        teacher_groups = [g[1] for g in teacher_groups if g[3] == "Teacher"]

        if not teacher_groups:
            self.ui.error_message("Ｎｏ ｇｒｏｕｐｓ ａｓｓｏｃｉａｔｅｄ ｗｉｔｈ ｙｏｕ．")
            return ("MENU", self.logged_in_user)

        index = survey.routines.select(
            'Ｓｅｌｅｃｔ ａ ｇｒｏｕｐ ｔｏ ａｓｓｉｇｎ:\n',
            options=[g + "\n" for g in teacher_groups],
            focus_mark='> ',
            evade_color=survey.colors.basic('white'),
            insearch_color=survey.colors.basic('white'))
        group = teacher_groups[index]

        name = input(colored("> Ｅｘｐｅｒｉｍｅｎｔ Ｎａｍｅ :", "white")).strip()

        # 2️⃣ Cancel if experiment name is null
        if not name:
            self.ui.indicator_message("Ｃｒｅａｔｅ ｅｘｐｅｒｉｍｅｎｔ ｃａｎｃｅｌｌｅｄ （Ｎｏ ｎａｍｅ ｇｉｖｅｎ）")
            return ("MENU", self.logged_in_user)

        aim = input(colored("> Ａｉｍ :", "white"))
        procedure = input(colored("> Ｐｒｏｃｅｄｕｒｅ (Ｍｕｌｔｉ－Ｌｉｎｅ) :", "white"))
        due = input(colored("> Ｄｕｅ Ｄａｔｅ :", "white"))

        status_options = ["Ａｃｔｉｖｅ", "Ｏｆｆｌｉｎｅ"]
        status_index = survey.routines.select("Ｓｅｌｅｃｔ Ｓｔａｔｕｓ:\n", options=status_options)
        status = status_options[status_index]

        self.expt.add_experiment(name, group, aim, procedure, due, status, self.logged_in_user)
        self.ui.success_message(f"Ｅｘｐｅｒｉｍｅｎｔ '{name}' ｃｒｅａｔｅｄ ｓｕｃｃｅｓｓｆｕｌｌｙ！")

        return ("MENU", self.logged_in_user)

    def teacher_view_experiments(self):
        os.system("clear")
        expts = self.expt.get_experiments_by_teacher(self.logged_in_user)

        if not expts:
            self.ui.error_message("Ｎｏ ｅｘｐｅｒｉｍｅｎｔｓ ｆｏｕｎｄ！")
            return ("MENU", self.logged_in_user)

        options = [f"{e[1]}  ({e[5]})\n" for e in expts]
        index = survey.routines.select("Ｓｅｌｅｃｔ ａｎ ｅｘｐｅｒｉｍｅｎｔ:\n", options=options)
        selected = expts[index]

        while True:
            os.system("clear")
            print(f"""
ＡＩＭ: {selected[3]}
ＰＲＯＣＥＤＵＲＥ: {selected[4]}
ＳＴＡＴＵＳ: {selected[5]}
ＤＵＥ ＤＡＴＥ: {selected[6]}
""")
            # 3️⃣ Add "Delete Experiment" option
            sub_options = ["Ｃｈａｎｇｅ Ｓｔａｔｕｓ", "Ｖｉｅｗ Ｒｅｓｕｌｔｓ", "Ｄｅｌｅｔｅ Ｅｘｐｅｒｉｍｅｎｔ", "Ｂａｃｋ"]
            sub_index = survey.routines.select("Ｓｅｌｅｃｔ ａｎ ｏｐｅｒａｔｉｏｎ:\n", options=sub_options)

            if sub_index == 0:
                new_status = "Ｏｆｆｌｉｎｅ" if selected[5] == "Ａｃｔｉｖｅ" else "Ａｃｔｉｖｅ"
                self.expt.update_status(selected[1], new_status)
                selected = self.expt.get_experiment(selected[1])
                self.ui.success_message(f"Ｓｔａｔｕｓ ｃｈａｎｇｅｄ ｔｏ {new_status}")
            elif sub_index == 1:
                self.view_results(selected[1], selected[2])
            elif sub_index == 2:
                confirm = input(colored("Ａｒｅ ｙｏｕ ｓｕｒｅ ｙｏｕ ｗａｎｔ ｔｏ ｄｅｌｅｔｅ ？ (y/n): ", "red")).strip().lower()
                if confirm == "y":
                    self.expt.delete_experiment(selected[1])
                    self.ui.success_message("Ｅｘｐｅｒｉｍｅｎｔ ｄｅｌｅｔｅｄ ｓｕｃｃｅｓｓｆｕｌｌｙ！")
                    break
            else:
                break

        return ("MENU", self.logged_in_user)

    def view_results(self, experiment_name, group_name):
        os.system("clear")
        results = self.expt.get_results_for_experiment(experiment_name)
        members = self.lab.get_members(group_name)
        all_students = [m[0] for m in members if m[1] == "Student"]
        students_with_results = [r[1] for r in results]

        print(f"\nＲｅｓｕｌｔｓ ｆｏｒ ｅｘｐｅｒｉｍｅｎｔ: {experiment_name}\n")
        print("+--------------------+--------------------+--------------------+")
        print("| Student Name       | Username           | Result             |")
        print("+--------------------+--------------------+--------------------+")
        for r in results:
            print(f"| {r[0]:18} | {r[1]:18} | {str(r[2]):18} |")
        print("+--------------------+--------------------+--------------------+")

        # 4️⃣ Add missing-students table
        missing_students = [s for s in all_students if s not in students_with_results]
        if missing_students:
            print("\nStudents who have yet to give their result:\n")
            print("+--------------------+")
            print("| Student Username   |")
            print("+--------------------+")
            for s in missing_students:
                print(f"| {s:18} |")
            print("+--------------------+")

        input("\nＰｒｅｓｓ ＥＮＴＥＲ ｔｏ ｇｏ ｂａｃｋ．．．")

    # ========== STUDENT SECTION ==========
    def student_view_experiments(self):
        os.system("clear")
        creds = self.auth.get_details(self.logged_in_user)
        name = creds[4]
        groups = self.lab.get_groups_by_user(self.logged_in_user)

        if not groups:
            self.ui.error_message("Ｎｏ ｇｒｏｕｐ ｆｏｕｎｄ．")
            return ("MENU", self.logged_in_user)

        all_expts = []
        for g in groups:
            all_expts += self.expt.get_experiments_by_group(g[1])

        if not all_expts:
            self.ui.error_message("Ｎｏ ｅｘｐｅｒｉｍｅｎｔｓ ｆｏｕｎｄ！")
            return ("MENU", self.logged_in_user)

        options = [f"{e[1]} ({e[5]})\n" for e in all_expts]
        index = survey.routines.select("Ｓｅｌｅｃｔ ａｎ ｅｘｐｅｒｉｍｅｎｔ:\n", options=options)
        selected = all_expts[index]

        os.system("clear")
        print(f"""
ＳＴＡＴＵＳ: {selected[5]}
ＤＵＥ ＤＡＴＥ: {selected[6]}
ＡＩＭ: {selected[3]}
ＰＲＯＣＥＤＵＲＥ: {selected[4]}
""")

        existing_result = self.expt.get_result(selected[2], selected[1], self.logged_in_user)

        if selected[5] == "Ａｃｔｉｖｅ":
            result = input(colored("> Ｅｎｔｅｒ ｙｏｕｒ ｒｅｓｕｌｔ :", "white"))
            if existing_result is None:
                self.expt.add_result(selected[2], selected[1], name, self.logged_in_user, result)
            else:
                self.expt.update_result(selected[2], selected[1], self.logged_in_user, result)
            self.ui.success_message("Ｒｅｓｕｌｔ ｓｕｂｍｉｔｔｅｄ ｓｕｃｃｅｓｓｆｕｌｌｙ！")
        else:
            print(f"\nＥｘｐｅｒｉｍｅｎｔ ｉｓ ｏｆｆｌｉｎｅ． Ｙｏｕｒ ｒｅｓｕｌｔ: {existing_result}")
            input("Ｐｒｅｓｓ ＥＮＴＥＲ ｔｏ ｇｏ ｂａｃｋ．．．")

        return ("MENU", self.logged_in_user)

    # ========== MAIN HANDLER ==========
    def handler(self):
        os.system("clear")
        creds = self.auth.get_details(self.logged_in_user)
        user_type = creds[3]

        if user_type == "Ｔｅａｃｈｅｒ":
            options = [
                "Ｃｒｅａｔｅ Ｎｅｗ Ｅｘｐｅｒｉｍｅｎｔ\n",
                "Ｖｉｅｗ Ａｌｌ Ｅｘｐｅｒｉｍｅｎｔｓ\n",
                "Ｂａｃｋ\n"
            ]
            index = survey.routines.select('\nＰｌｅａｓｅ ｃｈｏｏｓｅ:\n', options=options)
            if index == 0:
                return self.create_experiment()
            elif index == 1:
                return self.teacher_view_experiments()
            else:
                return ("MENU", self.logged_in_user)
        else:
            options = [
                "Ｖｉｅｗ Ａｌｌ Ｅｘｐｅｒｉｍｅｎｔｓ\n",
                "Ｂａｃｋ\n"
            ]
            index = survey.routines.select('\nＰｌｅａｓｅ ｃｈｏｏｓｅ:\n', options=options)
            if index == 0:
                return self.student_view_experiments()
            else:
                return ("MENU", self.logged_in_user)



#YEEEEEEEEESSSSSSSSSSSSSSSS