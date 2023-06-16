"""Limesurvey invitation sender."""

from limesurveyrc2api.limesurvey import LimeSurvey
from credentials import set_creds


def run():
    """Start script."""
    creds = set_creds()
    ls = LimeSurvey(creds.url, creds.username)
    ls.open(creds.password)
    res = ls.token.list_participants(
        292257,
        limit=10,
        conditions={"sent": "N", "completed": "N"}
    )
    token_ids = [part["tid"] for part in res]
    # ls.token.invite_participants(618941, token_ids)
    print(res)
    print("correus enviats.")
    ls.close()


if __name__ == "__main__":
    run()
