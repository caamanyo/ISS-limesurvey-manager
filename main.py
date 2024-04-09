import base64
import os
import time as t
from collections import OrderedDict

import pyperclip  # type:ignore
from dotenv import load_dotenv  # type:ignore
from limesurveyrc2api.limesurvey import LimeSurvey  # type:ignore

load_dotenv()


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


@log_time
def run():
    """Initialize program."""
    url = os.getenv("url")
    username = os.getenv("username")
    password = os.getenv("password")
    GENERAL_FORM_ID = 292257

    api = LimeSurvey(url=url, username=username)
    api.open(password=password)

    # Participant token to search for.
    token_list = pyperclip.paste().splitlines()
    if not all((len(token) == 15 for token in token_list)):
        print("Invalid Token found.")
        return

    for token in token_list:
        al_data = api.token.get_participant_properties(
            GENERAL_FORM_ID, token_query_properties={"token": token}
        )

        params = OrderedDict(
            [
                ("sessionkey", api.session_key),
                ("surveyid", al_data["attribute_4"]),
                ("token", token),
            ]
        )

        # Get a list of all the files related to that participant
        cicle_response = api.query("get_uploaded_files", params)
        cicle_files = ensure_dictionary(cicle_response)

        params["surveyid"] = GENERAL_FORM_ID
        general_response = api.query("get_uploaded_files", params)
        general_files = ensure_dictionary(general_response)

        results = {**cicle_files, **general_files}

        for [key, value] in results.items():
            # Check if table exists
            if key == "status":
                continue

            # Decode file
            with open(
                f"fitxers exportats/{al_data['lastname']}, {al_data['firstname']} - {value['meta']['question']['title']}.pdf",
                "wb",
            ) as f:
                f.write(base64.b64decode(value["content"]))

    # Close the session.
    api.close()


if __name__ == "__main__":
    run()
