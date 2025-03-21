from textnode import TextType, TextNode
from htmlnode import LeafNode

import re

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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    image_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            image_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            for image in images:
                image_nodes.append(TextNode(image[0], image[1], TextType.IMAGE))
    return image_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    link_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            link_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            for link in links:
                link_nodes.append(TextNode(link[0], link[1], TextType.LINK))
    return link_nodes
