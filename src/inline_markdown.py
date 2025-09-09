import re
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter


def extract_markdown_images(text):
    """Extract image markdown syntax from text.

    Args:
        text (str): Text potentially containing image markdown

    Returns:
        list: List of tuples (alt_text, url) for each image found
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """Extract link markdown syntax from text.

    Args:
        text (str): Text potentially containing link markdown

    Returns:
        list: List of tuples (link_text, url) for each link found
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    """Split TextNodes containing image markdown into separate nodes.

    Args:
        old_nodes (list): List of TextNode objects

    Returns:
        list: List of TextNode objects with images split out
    """
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(old_node)
            continue

        current_text = text
        for image_alt, image_url in images:
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections) != 2:
                continue

            before_text, after_text = sections

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            current_text = after_text

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """Split TextNodes containing link markdown into separate nodes.

    Args:
        old_nodes (list): List of TextNode objects

    Returns:
        list: List of TextNode objects with links split out
    """
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(old_node)
            continue

        current_text = text
        for link_text, link_url in links:
            sections = current_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                continue

            before_text, after_text = sections

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            current_text = after_text

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """Convert text with inline markdown to TextNodes.

    Args:
        text (str): Raw text potentially containing inline markdown

    Returns:
        list: List of TextNode objects representing the parsed text
    """
    initial_node = TextNode(text, TextType.TEXT)
    nodes = [initial_node]

    # Process delimiters in order: bold first, then italic, then code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Process images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
