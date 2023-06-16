"""Limesurvey invitation sender."""

import logging

from limesurveyrc2api.exceptions import LimeSurveyError
from limesurveyrc2api.limesurvey import LimeSurvey

from credentials import set_creds

logging.basicConfig(filename="./status.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s",
                    datefmt="%y-%m-%d %H:%M:%S")


def send_invites():
    """Fetch a number of participants from a survey and sends them the invite."""
    # Configuration:
    # Survey to fetch from.
    survey_id = 292257

    # This limit determines how many emails will be sent.
    limit = 10

    # Fetch participants with unsent invitations and uncompleted responses.
    conditions = {"sent": "N", "completed": "N"}

    try:
        res = ls.token.list_participants(
            survey_id,
            limit=limit,
            conditions=conditions
        )

        # Grab the token ids only.
        token_ids = [part["tid"] for part in res]

        # Send invitations with the token ids.
        result = ls.token.invite_participants(survey_id, token_ids)
    except LimeSurveyError as e:
        logging.warning(e)


if __name__ == "__main__":
    # Set the credentials.
    creds = set_creds()

    # Instatiate LS remote control.
    ls = LimeSurvey(creds.url, creds.username)

    # Start connection.
    ls.open(creds.password)
    send_invites()

    # End connection to LS.
    ls.close()
