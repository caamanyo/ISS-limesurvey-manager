"""Limesurvey invitation sender."""

from limesurveyrc2api.limesurvey import LimeSurvey
from credentials import set_creds


def run():
    """Fetch a number of participants from a survey and sends them the invite."""

    # Configuration:
    # Survey to fetch from.
    survey_id = 292257

    # This limit determines how many emails will be sent.
    limit = 10

    # Set the credentials.
    creds = set_creds()

    # Instatiate LS remote control.
    ls = LimeSurvey(creds.url, creds.username)

    # Start connection.
    ls.open(creds.password)

    # Fetch participants with unsent invitations and uncompleted responses.
    res = ls.token.list_participants(
        survey_id,
        limit=limit,
        conditions={"sent": "N", "completed": "N"}
    )

    # Grab the token ids only.
    token_ids = [part["tid"] for part in res]

    # Send invitations with the token ids.
    # ls.token.invite_participants(618941, token_ids)
    print(res)
    print("correus enviats.")

    # End connection to LS
    ls.close()


if __name__ == "__main__":
    run()
