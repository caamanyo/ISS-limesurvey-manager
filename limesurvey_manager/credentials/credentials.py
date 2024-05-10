"""Set limesurvey credentials."""


import os

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Credentials:
    """Store LS credentials."""

    url: str
    username: str
    password: str


def set_creds():
    """Initialize credentials and returns Credentials class."""
    url = os.getenv("url")
    username = os.getenv("ls_user")
    password = os.getenv("password")

    return Credentials(url, username, password)
