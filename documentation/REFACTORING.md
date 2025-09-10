# Project Architecture

## Module Organization

The static site generator follows a modular design with clear separation of responsibilities:

## Core Modules

### `textnode.py`
- **Purpose**: Base text representation classes
- **Content**: `TextNode`, `TextType`, `text_node_to_html_node()`
- **Responsibility**: Fundamental text structures and HTML conversion

### `htmlnode.py`, `leafnode.py`, `parentnode.py`
- **Purpose**: HTML node hierarchy
- **Responsibility**: HTML structure representation and generation

### `split_delimiter.py`
- **Purpose**: Markdown delimiter processing
- **Responsibility**: Split text based on delimiters (**bold**, _italic_, `code`)

### `inline_markdown.py`
- **Purpose**: Inline markdown processing
- **Key functions**:
  - `extract_markdown_images()` / `extract_markdown_links()`
  - `split_nodes_image()` / `split_nodes_link()`
  - `text_to_textnodes()` - main conversion function

### `block_markdown.py`
- **Purpose**: Block-level markdown processing
- **Key functions**:
  - `markdown_to_blocks()` - separate document into blocks
  - `block_to_block_type()` - identify block types
  - `markdown_to_html_node()` - main conversion
  - Specialized functions: `heading_to_html_node()`, `code_to_html_node()`, etc.

### `extract_title.py`
- **Purpose**: Extract H1 headers from markdown
- **Responsibility**: Title extraction for page metadata

### `generate_page.py`
- **Purpose**: Page generation from markdown to HTML
- **Responsibility**: Template processing and file generation

### `copystatic.py`
- **Purpose**: Static file copying
- **Responsibility**: Recursive file and directory copying

### `main.py`
- **Purpose**: Main entry point
- **Responsibility**: Orchestrate the build process

## Test Modules

### `test_*.py`
- Comprehensive test coverage for all functionality
- 176 tests covering text processing, HTML generation, and file operations
- Ensures reliability and correctness of all components

## Design Principles

1. **Single Responsibility**: Each module has a clear, focused purpose
2. **Modular Design**: Components can be tested and modified independently
3. **Clear Interfaces**: Simple function signatures and clear data flow
4. **Comprehensive Testing**: High test coverage ensures reliability
