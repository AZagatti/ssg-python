import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_page


def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (parent of src)
    project_root = os.path.dirname(script_dir)

    dir_path_static = os.path.join(project_root, "static")
    dir_path_public = os.path.join(project_root, "public")
    dir_path_content = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Generate the main page
    index_markdown_path = os.path.join(dir_path_content, "index.md")
    index_html_path = os.path.join(dir_path_public, "index.html")

    generate_page(index_markdown_path, template_path, index_html_path)


if __name__ == "__main__":
    main()
