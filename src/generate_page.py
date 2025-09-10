import os
from block_markdown import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(entry_path):
            if entry.endswith(".md"):
                html_filename = entry.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, html_filename)
                generate_page(entry_path, template_path, dest_path, basepath)
        else:
            dest_subdir = os.path.join(dest_dir_path, entry)
            if not os.path.exists(dest_subdir):
                os.makedirs(dest_subdir)

            generate_pages_recursive(entry_path, template_path, dest_subdir, basepath)
