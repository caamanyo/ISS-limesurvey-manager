"""Handle all file relates operations."""

import os
import shutil
import base64


def remove_all_files(path):
    """Remove all files from a selected folder."""
    for filename in os.listdir(path):
        file_path = path
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def decode_file(file: str):
    """Expect a base64 string to decode."""
    return base64.b64decode(file)


def write_file(file_path: str, contents):
    """Write a file with a given path."""
    with open(file_path, "wb") as f:
        f.write(contents)


def create_folder(self, path: str) -> None:
    """Create a folder if not already present."""
    if not os.path.exists(path):
        os.makedirs(path)
