class HTMLNode:
    def __init__(self, tag: str|None=None, value: str|None=None, children: list|None=None, props: dict|None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and \
        self.value == other.value and \
        self.children == other.children and \
        self.props == other.props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        return ""

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict|None=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and \
        self.children == other.children and \
        self.props == other.props

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be empty")
        if not self.children:
            raise ValueError("Children cannot be empty")
        return f"<{self.tag}{' '+self.props_to_html() if self.props else ''}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str, props: dict|None=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and \
        self.value == other.value and \
        self.props == other.props

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be empty")
        if self.tag is None or '':
            return self.value
        return f"<{self.tag}{' '+self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"
