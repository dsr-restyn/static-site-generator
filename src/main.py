from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    test_node = TextNode("Hello, World!", TextType.BOLD, "https://www.example.com")
    print(test_node)

def text_node_to_html(text_node):
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

if __name__ == "__main__":
    main()
