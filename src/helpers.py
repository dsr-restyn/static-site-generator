from src.htmlnode import HTMLNode, ParentNode, LeafNode
from src.textnode import TextNode, TextType
from src.nodetonode import markdown_to_blocks, text_to_textnodes, text_node_to_html
from src.blocks import block_to_blocktype, BlockType

import re

def generate_page(from_path, template_path, to_path, basepath):
    with open(from_path, "r") as f:
        content = f.read()
        title = extract_h1_header(content)
    with open(template_path, "r") as f:
        template = f.read()
    html_content = markdown_to_html_node(content).to_html()
    with open(to_path, "w") as f:
        new_content = template.replace("{{ Content }}", html_content).replace("{{ Title }}", title).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
        f.write(new_content)

def extract_h1_header(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_blocktype(block)[0] == BlockType.HEADING and block.startswith("# "):
            return block[2:].strip()
    raise ValueError("No H1 header found")

def code_block_to_html_node(text: str) -> ParentNode:
    """
    Converts a code block to an HTML node while preserving its original formatting,
    including tabbing and newlines.
    """
    # Ensure the block starts and ends with ```
    if not text.strip().startswith("```") or not text.strip().endswith("```"):
        raise ValueError("Code block must start and end with ```")
    
    # Remove the enclosing backticks but preserve the inner content as-is
    lines = text.split("\n")
    content = "\n".join(lines[1:-1])  # Exclude the first and last lines (``` delimiters)
    code_text_node = TextNode(content, TextType.CODE)
    return ParentNode("pre", [LeafNode("code", code_text_node.text)])

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            children.append(LeafNode(None, node.text))
        else:
            children.append(text_node_to_html(node))
    return children

def strip_block_of_delimiters(block: str, delimiter: str) -> str:
    if delimiter == "> ":
        print(f"strip_block_of_delimiters: {block=}")
        lines = block.split("\n")
        for line in lines:
            print(f"strip_block_of_delimiters: {line=}")
        return "\n".join([line.strip().lstrip(delimiter) for line in block.split("\n")])
    return block.strip(delimiter).strip()

def get_block_delimiter(block: str) -> str:
    return block[0]

def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block = block.strip()
        block_type, md_delimiter = block_to_blocktype(block)
        if block_type == BlockType.HEADING:
            heading_level = block.count("#")
            tag = block_type.value + str(heading_level)
            block = strip_block_of_delimiters(block, "#" * heading_level + " ")
            text_children = text_to_children(block.replace("\n", " "))
            children.append(ParentNode(tag, text_children))
        elif block_type == BlockType.CODE:
            # Use the updated code_block_to_html_node function
            children.append(code_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            block = strip_block_of_delimiters(block, "> ")
            raw_text_node = LeafNode(None, block.replace("\n", "<br>"))  # Preserve newlines as <br>
            children.append(ParentNode(block_type.value, [raw_text_node]))
        elif block_type in [BlockType.ULIST, BlockType.OLIST]:
            list_items = block.split("\n")
            list_children = []
            for item in list_items:
                if block_type == BlockType.OLIST:
                    item = re.sub(r"^\d+\.\s*", "", item)
                else:
                    item = strip_block_of_delimiters(item, md_delimiter if md_delimiter else "")
                list_children.append(ParentNode("li", text_to_children(item)))
            children.append(ParentNode(block_type.value, list_children))
        else:
            text_children = text_to_children(block.replace("\n", " "))
            children.append(ParentNode(block_type.value, text_children))
    return ParentNode("div", children)
