def extract_title(markdown):
    """
    Extract the h1 header from markdown content.

    Args:
        markdown (str): Markdown content

    Returns:
        str: The title text without the # and whitespace

    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            # Remove the '# ' and any trailing whitespace
            title = line[2:].strip()
            if title:
                return title

    raise ValueError("No h1 header found in markdown content")
