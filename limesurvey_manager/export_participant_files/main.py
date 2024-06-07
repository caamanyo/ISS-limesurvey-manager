import base64
import os
import shutil
import time as t
from collections import OrderedDict
from json import load

import pyperclip  # type:ignore
from dotenv import load_dotenv
from limesurveyrc2api.exceptions import LimeSurveyError  # type:ignore
from limesurveyrc2api.limesurvey import LimeSurvey  # type:ignore

from limesurvey_manager.credentials.credentials import set_creds

load_dotenv()
OPTIONS = ["d", "q"]


def log_time(func):
    def wrapper():
        start_execution = t.time()
        func()
        elapsed_time = t.time() - start_execution
        print(
            f"Function: {func.__name__}    "
            f"Time: It took {elapsed_time} seconds."
        )

    return wrapper


def ensure_dictionary(suspect):
    check = isinstance(suspect, dict)
    if not check:
        return {}
    return suspect


def remove_all_files(path):
    """Remove all files from a selected folder."""
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


@log_time
def run():
    """Initialize program."""
    creds = set_creds()
    # exported_path = "fitxers exportats"
    exported_path = "fitxers exportats"
    with open("forms_config.json") as f:
        course_list = load(f)

    GENERAL_FORM_ID = 292257

    # Open a session.
    api = LimeSurvey(url=creds.url, username=creds.username)
    api.open(password=creds.password)

    # Participant token to search for.
    token_list = pyperclip.paste().splitlines()
    if not all(len(token) == 15 for token in token_list):
        print("Invalid token found.")
        return

    print(f" Hi ha {len(token_list)} tokens.")
    while True:
        try:
            answer = input(
                "De quin cicle són? S'ha d'introduir el codi del cicle (HIG, TAP, etc...): "
            ).upper()
            course_conf = list(
                filter(lambda c: c["code"] == answer, course_list)
            )[0]
        except IndexError:
            print("Aquest cicle no existeix.")
        else:
            break

    if course_conf["single_form"]:
        survey_id = course_conf["survey_id"]
    else:
        survey_id = GENERAL_FORM_ID

    for token in token_list:
        try:
            al_data = api.token.get_participant_properties(
                survey_id, token_query_properties={"token": token}
            )
        except LimeSurveyError as e:
            print(e)
            return
        al_fullname = f"{al_data['lastname']}, {al_data['firstname']}"
        al_cicle = al_data["attribute_3"]
        if len(al_cicle) > 3:
            al_cicle = al_cicle[3]

        # Create alumnus folder
        al_path = f"{exported_path}/{al_cicle}/{al_fullname}"
        if not os.path.exists(al_path):
            os.makedirs(al_path)
        else:
            remove_all_files(al_path)

        params = OrderedDict(
            [
                ("sessionkey", api.session_key),
                ("surveyid", al_data["attribute_4"]),
                ("token", token),
            ]
        )

        cicle_response = api.query("get_uploaded_files", params)
        cicle_files = ensure_dictionary(cicle_response)
        results = cicle_files

        if not course_conf["single_form"]:
            params["surveyid"] = GENERAL_FORM_ID
            general_response = api.query("get_uploaded_files", params)
            general_files = ensure_dictionary(general_response)
            results = {**cicle_files, **general_files}

        for [key, value] in results.items():
            # Decode file
            if key == "status":
                print()
                print(f"\tL'alumne {al_fullname} no té fitxers per exportar.")
                print()
                continue
            with open(
                f"{al_path}/{al_fullname} - {value['meta']['question']['title']}.pdf",
                "wb",
            ) as f:
                f.write(base64.b64decode(value["content"]))

    # Close the session.
    api.close()
    print("Fitxers descarregats correctament.")


def show_menu():
    print()
    print("*** Exportació de fitxers Limesurvey ***")
    print("PASSOS:")
    print("1. Copiar tokens")
    print("2. Escull la opció desitjada (d,q) i prem ENTER:")
    print("\td. Descarregar fitxers dels tokens copiats.")
    print("\tq. Sortir")


if __name__ == "__main__":
    show_menu()
    while True:
        opt = input("=> ")
        match opt.lower():
            case "d":
                run()
            case "q":
                break
            case _:
                print("Aquesta opció no és vàlida. Opcions:", *OPTIONS)
        show_menu()
