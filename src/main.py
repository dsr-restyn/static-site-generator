from textnode import TextNode, TextType
from nodetonode import split_nodes_link

def main():
    print("Static Site Generator started...")
    test_node = TextNode("Hello, [link](https://www.example.com)", TextType.TEXT)
    print(split_nodes_link([test_node]))

if __name__ == "__main__":
    main()
