"""Limesurvey invitation sender."""

import logging
import pprint
import time
from collections import OrderedDict
from json import load

from limesurveyrc2api.exceptions import LimeSurveyError  # type:ignore
from limesurveyrc2api.limesurvey import LimeSurvey  # type:ignore

from limesurvey_manager.credentials.credentials import set_creds

logging.basicConfig(
    filename="./status.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
)


def log_errors(func, *args, **kwargs):
    """Log Limesurvey errors to file."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LimeSurveyError as e:
            logging.warning(e.message)

    return wrapper


def fetch_participants(survey_id: str, limit: int, conditions: dict) -> list:
    """Fetch a number of participants from a survey."""
    try:
        res = ls.token.list_participants(
            survey_id, limit=limit, conditions=conditions
        )
        return res
    except LimeSurveyError as e:
        if "No survey participants found." in e.message:
            return []
        else:
            raise e


def send_invites(survey_id: str, token_ids: list):
    """Fetch a number of participants from a survey and sends them the invite."""
    # Send invitations with the token ids.
    result = ls.token.invite_participants(survey_id, token_ids)
    return result


def get_survey_group_id(survey_id: int) -> int:
    survey_properties = ls.query(
        "get_survey_properties",
        OrderedDict(sSessionKey=ls.session_key, iSurveyID=survey_id),
    )
    return survey_properties["gsid"]


@log_errors
def invite_participants(survey_id: str, email_limit: int = 10):
    """Invite participants to a specific survey. Returns False if there is no more participants."""
    # Fetch participants with unsent invitations and uncompleted responses.
    conditions = {"sent": "N", "completed": "N"}

    parts = fetch_participants(survey_id, email_limit, conditions)
    if not parts:
        return False
    # Grab the token ids only.
    token_ids = [part["tid"] for part in parts]

    # Send invitations.
    # pprint.pp(parts)
    send_invites(survey_id, token_ids)
    return True


if __name__ == "__main__":
    # Set the credentials.
    creds = set_creds()
    with open("forms_config.json") as f:
        survey_list = load(f)

    # Instatiate LS remote control.
    ls = LimeSurvey(creds.url, creds.username)

    # Start connection.
    ls.open(creds.password)

    all_surveys = ls.survey.list_surveys()
    active_surveys = [sur["sid"] for sur in all_surveys if sur["active"] == "Y"]

    survey_list = list(
        filter(lambda sur: sur["survey_id"] in active_surveys, survey_list)
    )

    print("***Formularis seleccionats:***")
    pprint.pp(survey_list)

    confirm = input("Enviar correus?")

    if confirm not in ["Y", "y"]:
        exit(1)

    for survey in survey_list:
        print(survey["code"])
        participants_left = invite_participants(survey["survey_id"])
        while participants_left:
            time.sleep(60)
            participants_left = invite_participants(survey["survey_id"])

    print("No hi ha més invitacions a enviar.")
    ls.close()
