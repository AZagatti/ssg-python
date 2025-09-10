import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive


def main():
    # Get basepath from command line argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (parent of src)
    project_root = os.path.dirname(script_dir)

    dir_path_static = os.path.join(project_root, "static")
    dir_path_docs = os.path.join(project_root, "docs")
    dir_path_content = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    # Generate all pages recursively from content directory
    print("Generating pages from content directory...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()
