from limesurveyrc2api.limesurvey import LimeSurvey
from collections import OrderedDict
import os
import shutil
from dotenv import load_dotenv
import base64
import time as t

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
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@log_time
def run():
    """Initialize program."""
    url = os.getenv("url")
    username = os.getenv("ls_user")
    password = os.getenv("password")
    exported_path = "fitxers exportats"
    GENERAL_FORM_ID = 292257

    # Open a session.
    api = LimeSurvey(url=url, username=username)
    api.open(password=password)

    # Participant token to search for.
    token = input("Token de l'alumne: ")

    al_data = api.token.get_participant_properties(
        GENERAL_FORM_ID, token_query_properties={"token": token})
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

    params = OrderedDict([
        ("sessionkey", api.session_key),
        ("surveyid", al_data["attribute_4"]),
        ("token", token)
    ])

    # Get a list of all the files related to that participant
    cicle_response = api.query("get_uploaded_files", params)
    cicle_files = ensure_dictionary(cicle_response)

    # TODO: Extract files form the general form.
    params["surveyid"] = GENERAL_FORM_ID
    general_response = api.query("get_uploaded_files", params)
    general_files = ensure_dictionary(general_response)

    results = {**cicle_files, **general_files}

    for [key, value] in results.items():
        # Check if table exists
        if key == "status":
            print("La taula de participants no existeix.")
            continue

        # Decode file
        with open(f"{al_path}/{al_fullname} - {value['meta']['question']['title']}.pdf", "wb") as f:
            f.write(base64.b64decode(value["content"]))

    # Close the session.
    api.close()


if (__name__ == "__main__"):
    run()
