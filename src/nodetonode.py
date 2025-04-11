from textnode import TextType, TextNode
from htmlnode import LeafNode
from blocks import block_to_blocktype, BlockType

import re

def text_node_to_html(text_node: TextNode):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text.strip("`"))
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", '', {"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.LIST_ITEM:
        return LeafNode("li", text_node.text)
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
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            original_text = node.text
            if not images:
                new_nodes.append(node)
            else:
                for img_alt, img_src in images:
                    sections = original_text.split(f"![{img_alt}]({img_src})", 1)
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_src))
                    if len(sections) > 1:
                        original_text = sections[1]
                    else:
                        original_text = ""
                if original_text and original_text != node.text:
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            original_text = node.text
            if not links:
                new_nodes.append(node)
            else:
                for link_txt, link_src in links:
                    sections = original_text.split(f"[{link_txt}]({link_src})", 1)
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(link_txt, TextType.LINK, link_src))
                    if len(sections) > 1:
                        original_text = sections[1]
                    else:
                        original_text = ""
                if original_text and original_text != node.text:
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    init_node = TextNode(text, TextType.TEXT)
    delimiters = [
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("- ", TextType.LIST_ITEM),
        ("1. ", TextType.LIST_ITEM),
    ]
    nodes = []
    for char, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes or [init_node], char, text_type)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    current_block = []
    in_code_block = False
    for line in markdown.split("\n"):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            current_block.append(line)
            if not in_code_block:
                blocks.append("\n".join(current_block))
                current_block = []
        elif in_code_block:
            current_block.append(line)
        elif line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks
