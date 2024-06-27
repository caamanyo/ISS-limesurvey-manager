import argparse
from json import dump
from os import unlink
from os.path import join

from limesurvey_manager.export_participant_files import export_files
from limesurvey_manager.send_invitations import main


class File:
    def __init__(self, data):
        self.data = data
        self.file_path = join("file.json")

    def save_as_json(self):
        with open(self.file_path, "w") as f:
            dump(self.data, f)

    def remove(self):
        unlink(self.file_path)


def menu():
    parser = argparse.ArgumentParser(prog="Limesurvey Manager")
    subparsers = parser.add_subparsers(help="prova", required=True)

    parser_export = subparsers.add_parser("export", help="export functionality")
    parser_export.add_argument(
        "selection",
        choices=["files", "responses"],
        help="Choose between exporting participant files or responses.",
    )

    parser_send = subparsers.add_parser("send", help="send mails")
    parser_send.add_argument("selection", choices=["invitations", "reminder"])

    return parser.parse_args()


def select_option(option):
    match option.selection:
        case "files":
            export_files.export_participant_files()
        case "responses":
            pass
        case "invitations":
            main.invite_participants()


if __name__ == "__main__":
    selection = menu()
    select_option(selection)
