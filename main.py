from LSHelper import LSHelper
import time as t
import os
from dotenv import load_dotenv

load_dotenv()


def log_time(func):
    def wrapper():
        start_execution = t.time()
        func()
        elapsed_time = t.time() - start_execution
        print(
            f"Function: {func.__name__}    "
            f"Time: It took {elapsed_time} seconds.")
    return wrapper


def menu():
    """Main menu."""
    print("Escull una opció:")
    print("1. Extreure documentació")
    print("2. Permetre a un alumne editar les seves respostes")
    print("0. Sortir del programa")
    choice = input("Opció? (0/1/2)")
    return choice


@log_time
def run():
    """Initialize program."""

    url = os.getenv("url")
    username = os.getenv("ls_user")
    password = os.getenv("password")
    exit_program = False

    # Initialize LS class
    ls = LSHelper(url, username, password)

    while not exit_program:
        option = menu()
        if option == "1":
            ls.extract_all_participant_files()
        elif option == "0":
            exit_program = True
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("***Aquesta opció no existeix. Prova una altra vegada.***")



if (__name__ == "__main__"):
    run()
