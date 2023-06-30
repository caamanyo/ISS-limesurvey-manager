"""Limesurvey invitation sender."""

import logging
import time

from limesurveyrc2api.exceptions import LimeSurveyError
from limesurveyrc2api.limesurvey import LimeSurvey

from credentials import set_creds

logging.basicConfig(filename="./status.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s",
                    datefmt="%y-%m-%d %H:%M:%S")


def log_errors(func):
    """Log Limesurvey errors to file."""
    def wrapper():
        try:
            return func()
        except LimeSurveyError as e:
            logging.warning(e.message)
    return wrapper


def fetch_participants(survey_id: int, limit: int, conditions: dict):
    """Fetch a number of participants from a survey."""
    try:
        res = ls.token.list_participants(
            survey_id,
            limit=limit,
            conditions=conditions
        )
        return res
    except LimeSurveyError as e:
        if "No survey participants found." in e.message:
            return []
        else:
            raise e


def send_invites(survey_id: int, token_ids: list):
    """Fetch a number of participants from a survey and sends them the invite."""
    # Send invitations with the token ids.
    result = ls.token.invite_participants(survey_id, token_ids)


@log_errors
def invite_participants():
    """Invite participants to a specific survey. Returns False if there is no more participants."""
    # Survey to fetch from.
    survey_id = 292257
    # Fetch participants with unsent invitations and uncompleted responses.
    conditions = {"sent": "N", "completed": "N"}
    # This limit determines how many emails will be sent.
    email_limit = 10

    parts = fetch_participants(survey_id, email_limit, conditions)
    if not parts:
        return False
    # Grab the token ids only.
    token_ids = [part["tid"] for part in parts]

    # Send invitations.
    send_invites(survey_id, token_ids)
    return True


if __name__ == "__main__":
    # Set the credentials.
    creds = set_creds()

    # Instatiate LS remote control.
    ls = LimeSurvey(creds.url, creds.username)

    # Start connection.
    ls.open(creds.password)

    participants_left = invite_participants()
    while participants_left:
        time.sleep(60)
        participants_left = invite_participants()

    print("No hi ha més invitacions a enviar.")
    # End LS connection.
    ls.close()
