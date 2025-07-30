from termcolor import colored
import time


class Messages:

  def __init__(self) -> None:
    self.color = colored

  def primary_line(self, color, length) -> None:
    print(self.color("-" * length, color))

  def error_message(self, message) -> None:
    self.primary_line("red", 80)
    print(colored(message, "red"))
    self.primary_line("red", 80)
    time.sleep(2)

  def default_message(self, message) -> None:
    self.primary_line("grey", 80)
    print(colored(message, "grey"))
    self.primary_line("grey", 80)

  def highlighter_message(self, message) -> None:
    self.primary_line("grey", 80)
    print(colored(message, "white"))
    self.primary_line("grey", 80)

  def success_message(self, message) -> None:
    self.primary_line("green", 80)
    print(colored(message, "green"))
    self.primary_line("green", 80)
    time.sleep(2)

  def indicator_message(self, message) -> None:
    self.primary_line("yellow", 80)
    print(colored(message, "yellow"))
    self.primary_line("yellow", 80)
    time.sleep(2)

  def input_message(self, message) -> str:
    self.primary_line("grey", 80)
    inp = input(message)
    self.primary_line("grey", 80)
    return inp

  def leave_line(self) -> None:
    print("")
