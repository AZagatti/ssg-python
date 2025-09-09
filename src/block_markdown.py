import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Split markdown text into individual blocks.

    Args:
        markdown (str): Raw markdown text

    Returns:
        list: List of block strings
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks after stripping
            filtered_blocks.append(stripped_block)
    return filtered_blocks


def block_to_block_type(block):
    """
    Determine the type of a markdown block.

    Args:
        block (str): A single markdown block

    Returns:
        BlockType: The type of the block
    """
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith(("- ", "* ")):
        for line in lines:
            if not (line.startswith("- ") or line.startswith("* ")):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert text with inline markdown to list of child HTMLNodes.

    Args:
        text (str): Text potentially containing inline markdown

    Returns:
        list: List of HTMLNode objects
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    """
    Convert markdown document to complete HTMLNode tree.

    Args:
        markdown (str): Complete markdown document

    Returns:
        ParentNode: Root HTMLNode containing all converted blocks
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    """
    Convert a single markdown block to HTMLNode.

    Args:
        block (str): A single markdown block

    Returns:
        ParentNode or LeafNode: HTMLNode representing the block
    """
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError(f"Invalid block type: {block_type}")


def paragraph_to_html_node(block):
    """Convert paragraph block to HTMLNode."""
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert heading block to HTMLNode."""
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert code block to HTMLNode."""
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]  # Remove ``` from start and end
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block):
    """Convert ordered list block to HTMLNode."""
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]  # Remove "1. ", "2. ", etc.
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block):
    """Convert unordered list block to HTMLNode."""
    items = block.split("\n")
    html_items = []
    for item in items:
        # Handle both "- " and "* " prefixes
        if item.startswith("- "):
            text = item[2:]
        elif item.startswith("* "):
            text = item[2:]
        else:
            text = item[2:]  # fallback
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    """Convert quote block to HTMLNode."""
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
