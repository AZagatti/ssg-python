# Main module for markdown processing
# This module re-exports functions from the specialized modules

# Import inline markdown functions
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

# Import block markdown functions
from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_to_html_node,
    text_to_children,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    ordered_list_to_html_node,
    unordered_list_to_html_node,
    quote_to_html_node,
)

# Main functions that might be used directly
__all__ = [
    # Inline functions
    "extract_markdown_images",
    "extract_markdown_links",
    "split_nodes_image",
    "split_nodes_link",
    "text_to_textnodes",
    # Block functions
    "BlockType",
    "markdown_to_blocks",
    "block_to_block_type",
    "markdown_to_html_node",
    "block_to_html_node",
    "text_to_children",
    "paragraph_to_html_node",
    "heading_to_html_node",
    "code_to_html_node",
    "ordered_list_to_html_node",
    "unordered_list_to_html_node",
    "quote_to_html_node",
]
