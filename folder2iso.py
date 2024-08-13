#!/bin/python3

import pycdlib
import os

FOLDER2ISO_VERSION = "0.0.1"


def create_iso_from_folder(dir_path, iso_path):
    print(f"reading '{dir_path}'...")
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    for root, dirs, files in os.walk(dir_path):
        # create all folders first
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            in_iso = "/" + os.path.relpath(folder_path, dir_path).replace(os.sep, "/")
            iso.add_directory(in_iso)
        # add the files
        for file in files:
            file_path = os.path.join(root, file)
            iso_path_in_iso = "/" + os.path.relpath(file_path, dir_path).replace(
                os.sep, "/"
            )
            print(f" + {iso_path_in_iso}")
            iso.add_file(file_path, iso_path_in_iso)

    iso.write(iso_path)
    print(f"{iso_path} created")
    iso.close()

    print("done!")
    return 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(f"folder2iso version {FOLDER2ISO_VERSION}")
        print(f"usage: {sys.argv[0]} </path/to/folder> [output.iso] ")
        exit(1)

    folder_path = sys.argv[1]
    output_iso = "output.iso"
    if len(sys.argv) > 2:
        output_iso = os.path.abspath(sys.argv[2])

    exit(create_iso_from_folder(folder_path, output_iso))
