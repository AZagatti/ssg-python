import os
import shutil

from copystatic import copy_files_recursive


def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (parent of src)
    project_root = os.path.dirname(script_dir)

    dir_path_static = os.path.join(project_root, "static")
    dir_path_public = os.path.join(project_root, "public")

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
