"""Module to manage participant's data."""

from dataclasses import dataclass
from pandas.core import series
import file_manager as fm
import config as cfg


@dataclass(kw_only=True)
class ParticipantFile:
    filename: str
    content: str

    def export_file(self, alumnus_dir: str):
        """Export a file to export directory."""

        # Decode and write the file to export
        decoded_file = fm.decode_file(self.content)
        fm.write_file([alumnus_dir, self.filename], decoded_file)


@dataclass(kw_only=True)
class ParticipantData(ParticipantFile):
    data: series.Series
    files: list[ParticipantFile]
    root_dir: str
    alumnus_dirs: list

    def __init__(self, data):
        self.data = data
        self.files = []
        breakpoint()
        self.root_dir = cfg.EXPORTATION_FOLDER
        self.fullname = f"{self.data.lastname}, {self.data.firstname}"
        self.alumnus_dirs = [self.data.attribute_3, self.fullname]

    def populate_files(self, files_list: list[dict]):
        """
        Initialize a list of ParticipantFile objects based on a list of
        dictionaries. Each dictionary must contain a 'meta' and 'content'
        keys retrieved from LS.
        """
        for file in files_list:
            new_file = ParticipantFile(
                filename=file["meta"]["name"],
                content=file["content"])
            self.files.append(new_file)

    def create_participant_folder(self):
        # Create directories where files will be exported
        return fm.create_folders(self.root_dir, *self.alumnus_dirs)

    def export_all_files(self):
        folder = self.create_participant_folder()
        fm.remove_all_files(folder)

        for file in self.files:
            file.export_file(folder)
            print(file.filename)
