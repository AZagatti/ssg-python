import os
from block_markdown import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from markdown content using a template.

    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML file will be saved
        basepath (str): Base path for the site (default: "/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title from markdown
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace absolute paths with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Write the final HTML to destination file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages for all markdown files in a directory.

    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory for generated HTML files
        basepath (str): Base path for the site (default: "/")
    """
    # List all entries in the content directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(entry_path):
            # If it's a markdown file, generate an HTML page
            if entry.endswith(".md"):
            # Convert .md to .html for destination filename
                html_filename = entry.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, html_filename)
                generate_page(entry_path, template_path, dest_path, basepath)
        else:
            # If it's a directory, create corresponding directory in destination
            # and recursively process it
            dest_subdir = os.path.join(dest_dir_path, entry)
            if not os.path.exists(dest_subdir):
                os.makedirs(dest_subdir)

            # Recursively process the subdirectory
            generate_pages_recursive(entry_path, template_path, dest_subdir, basepath)
