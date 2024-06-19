"""Set limesurvey credentials."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class MissingCredentialsError(Exception):
    pass


@dataclass
class Credentials:
    """Store LS credentials."""

    url: str
    username: str
    password: str


def set_creds() -> Credentials:
    """Initialize credentials. Raises MissingCredentials if environment variables are not present."""
    creds = {
        "url": os.getenv("url"),
        "username": os.getenv("ls_user"),
        "password": os.getenv("password"),
    }
    for k, v in creds.items():
        if not v:
            raise MissingCredentialsError(f"Missing credential: {k}")

    return Credentials(**creds)  # type:ignore
