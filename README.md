# Static Site Generator

A Python-based static site generator that converts Markdown content into HTML websites with support for GitHub Pages deployment.

## Features

- **Markdown to HTML conversion**: Complete support for markdown syntax including headers, paragraphs, lists, blockquotes, code blocks, bold, italic, links, and images
- **Template system**: Uses HTML templates with placeholder replacement
- **Static file copying**: Automatically copies CSS, images, and other static assets
- **Recursive page generation**: Processes entire directory structures of markdown files
- **GitHub Pages support**: Configurable base path for deployment to GitHub Pages
- **Local development server**: Built-in HTTP server for testing

## Project Structure

```
├── src/                    # Source code
│   ├── main.py            # Main entry point
│   ├── textnode.py        # Text node representation
│   ├── htmlnode.py        # HTML node classes
│   ├── inline_markdown.py # Inline markdown processing
│   ├── block_markdown.py  # Block markdown processing
│   ├── extract_title.py   # Title extraction from markdown
│   ├── generate_page.py   # Page generation functions
│   └── copystatic.py      # Static file copying
├── content/               # Markdown content files
├── static/                # Static assets (CSS, images)
├── template.html          # HTML template
├── docs/                  # Generated HTML output
├── main.sh               # Development build script
├── build.sh              # Production build script
└── test.sh               # Test runner
```

## Usage

### Local Development

```bash
# Build site for local development (uses "/" as base path)
python src/main.py

# Or use the development script
./main.sh

# Serve the site locally
cd docs && python -m http.server 8000
```

### Production Build (GitHub Pages)

```bash
# Build site for GitHub Pages (uses "/repo-name/" as base path)
./build.sh

# Or manually
python src/main.py "/your-repo-name/"
```

### Running Tests

```bash
./test.sh
```

## Content Structure

Place your markdown files in the `content/` directory. The generator will:

- Convert `content/index.md` to `docs/index.html`
- Convert `content/blog/post.md` to `docs/blog/post.html`
- Maintain the directory structure in the output

### Markdown File Format

Each markdown file should start with an H1 header for the page title:

```markdown
# Page Title

Your content here...
```

## Template System

The HTML template (`template.html`) uses two placeholders:

- `{{ Title }}`: Replaced with the H1 header from the markdown
- `{{ Content }}`: Replaced with the converted HTML content

## Static Assets

Place CSS, images, and other static files in the `static/` directory. They will be copied to the output directory maintaining their structure.

## GitHub Pages Deployment

1. Configure the base path in `build.sh` to match your repository name
2. Run `./build.sh` to generate the site
3. Commit and push the `docs/` directory
4. Configure GitHub Pages to serve from the `docs/` folder on the main branch

## Dependencies

- Python 3.6+
- Standard library modules only (no external dependencies)

## Architecture

The generator follows a modular design:

- **TextNode**: Represents text with type information (text, bold, italic, code, link, image)
- **HTMLNode**: Base class for HTML element representation
- **LeafNode/ParentNode**: Specific HTML node implementations
- **Markdown Processing**: Separate modules for inline and block-level markdown elements
- **Page Generation**: Template-based HTML generation with configurable base paths

## Testing

The project includes comprehensive unit tests covering all functionality:

- Text node creation and conversion
- HTML node generation
- Markdown parsing (inline and block)
- Page generation
- Static file copying

Run tests with: `./test.sh`
