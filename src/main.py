import os
import shutil
from ntpath import isfile

from generate import generate_page, generate_page_recursively

PUBLIC_DIR = "public/"
STATIC_DIR = "static/"

def copy_to_folder(source, destination, sub=""):
    full_source = os.path.join(source, sub)

    for item in os.listdir(full_source):
        full_item = os.path.join(full_source, item)

        if os.path.isfile(full_item):
            source_path = full_item
            destination_path = os.path.join(destination, sub)
            print(f"[log] copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            full_sub = os.path.join(destination, sub, item) 
            os.mkdir(full_sub)
            print(f"[log] created {full_sub}")
            copy_to_folder(source, destination, os.path.join(sub, item))

    return


def main():
    # setting up public/
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
        print(f"[log] cleaned {PUBLIC_DIR}")

    os.mkdir(PUBLIC_DIR)
    print(f"[log] created {PUBLIC_DIR}")

    if os.path.exists(STATIC_DIR):
        print(f"[log] {STATIC_DIR} found, copying to {PUBLIC_DIR}")
        copy_to_folder(STATIC_DIR, PUBLIC_DIR)

    # generating html
    source_path = "content/"
    template_path = "template.html"
    dest_path = "public/"
    generate_page_recursively(source_path, template_path, dest_path)


main()
