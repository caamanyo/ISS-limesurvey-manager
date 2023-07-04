"""Module to manage participant's data."""

from dataclasses import dataclass
from pandas.core import series
import config as cfg


@dataclass(kw_only=True)
class ParticipantFile:
    name: str
    content: str
    path: str = None

    def export_file(self):
        pass


@dataclass(kw_only=True)
class ParticipantData(ParticipantFile):
    data: series.Series
    files: list[ParticipantFile]

    def __init__(self, data, files=[]):
        self.data = data
        self.files = files
        self.fullname = f"{self.data.lastname}, {self.data.firstname}"

    def populate_files(self, files_list: list[dict]):
        for file in files_list:
            new_file = ParticipantFile(
                name=file["meta"]["name"], content=file["content"])
            self.files.append(new_file)
