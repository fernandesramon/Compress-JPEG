"""Compress given jpeg or folder containing jpegs
"""

import os
import sys
from PIL import Image

def usage():
    """Prints usage message to console
    """
    print("Usage:")
    print("     compressjpeg.py path")

def exit_with_error(msg=None):
    """Exits with error, printing the given message and usage
    """
    if msg is not None:
        print(msg)
    usage()
    sys.exit(1)

def check_image(path):
    """Checks if the given path is an image
    """
    try:
        with Image.open(path) as img:
            pass
    except IOError:
        return False
    
    return True

def compress_image(path):
    """Replaces given image with same image at quality 75
    """
    with Image.open(path) as img:
        exif_dict = img.info.get("exif")
        if exif_dict:
            img.save(path, quality=75, exif=exif_dict)
        else:
            img.save(path, quality=75)

def get_files_in_directory(path):
    """Returns the root files at the given path. Does not look in subdirs
    """
    files = []
    for (_, _, filenames) in os.walk(path):
        files.extend(filenames)
        break
    return files

def compress_path(path):
    """Compresses the given file or directory
    """
    if os.path.isfile(path):
        if not check_image(path):
            print("{} is not an image.".format(path))
        else:
            print("Processing {}".format(path))
            compress_image(path)
    elif os.path.isdir(path):
        files = get_files_in_directory(path)
        for file in files:
            compress_path(path + "/" + file)
    else:
        exit_with_error("Invalid path.")

def main():
    """Main runner
    """
    if len(sys.argv) < 2:
        exit_with_error("No file or folder specified.")

    path = sys.argv[1]
    compress_path(path)

if __name__ == "__main__":
    main()