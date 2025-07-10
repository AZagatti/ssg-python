from enum import Enum


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text_type = text_type
        self.text = text
        self.url = url

    def __eq__(self, text_node):
        if not isinstance(text_node, TextNode):
            return False
        return (
            self.text_type == text_node.text_type
            and self.text == text_node.text
            and self.url == text_node.url
        )

    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"

    def to_html(self) -> str:
        if self.text_type == TextType.PLAIN:
            return self.content
        elif self.text_type == TextType.BOLD:
            return f"<strong>{self.content}</strong>"
        elif self.text_type == TextType.ITALIC:
            return f"<em>{self.content}</em>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.content}</code>"
        elif self.text_type == TextType.LINK:
            return f'<a href="{self.content}">{self.content}</a>'
        elif self.text_type == TextType.IMAGE:
            return f'<img src="{self.content}" alt="Image">'
        else:
            raise ValueError(f"Unknown text type: {self.text_type}")
