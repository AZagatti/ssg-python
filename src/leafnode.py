from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        props_html = ""
        if self.props:
            props_html = " " + self.props_to_html().strip()

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
