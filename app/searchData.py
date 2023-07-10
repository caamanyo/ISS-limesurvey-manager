"""Convert form data to dictionary to send to LS API."""

from dataclasses import dataclass


@dataclass
class Conditions:
    sent: list
