"""Handle all file relates operations."""

import os
import shutil
import base64


def remove_all_files(dir):
    """Remove all files from a selected folder."""
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)

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


def write_file(file_path: list, contents):
    """Write a file with a given path."""
    path_to_write_to = os.path.join(*file_path)
    with open(path_to_write_to, "wb") as f:
        f.write(contents)


def create_folders(*args: str) -> bool:
    """Create a folder if not already present. Return false if path don't exists."""
    folders_path = os.path.join(*args)
    if not os.path.exists(folders_path):
        os.makedirs(folders_path)
    return folders_path
