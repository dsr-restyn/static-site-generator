from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html(text_node: TextNode):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("strong", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("em", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", '', {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    delimited_nodes = []
    for node in old_nodes:
        if node.text_type != node.text_type.TEXT:
            delimited_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    delimited_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    delimited_nodes.append(TextNode(part, text_type))
    return delimited_nodes
