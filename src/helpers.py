from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from nodetonode import markdown_to_blocks, text_to_textnodes, text_node_to_html

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            children.append(LeafNode(None, node.text))
        children.append(text_node_to_html(node))
    return children

# def markdown_to_html_node(markdown: str) -> ParentNode:
#     parent_node = ParentNode("div", [])
#     children = []
#     # split md into blocks
#     blocks = markdown_to_blocks(markdown)
#     print(blocks)
#     # iterate over blocks and create TextNodes
#     for block in blocks:
#         block = block.replace("\n", " ")
#         if not block.startswith("```"):
#             text_children = text_to_children(block)
#             children += text_children
#         else:
#             # if block is code, create HTMLNode as is without calling text_to_children
#             code_text_node = TextNode(block.strip(), TextType.CODE)
#             code_html_node = text_node_to_html(code_text_node)
#             children.append(ParentNode("pre", [code_html_node]))

#     return ParentNode("div", children)
