from helpers import *

def main():
    print("Static Site Generator started...")
    print("Parsing markdown...")
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    print(f"{md=}")
    node = markdown_to_html_node(md)
    # print(f"{node=}")
    html = node.to_html()
    # print(f"{html=}")
    with open("template.html", "w") as f:
        f.write(html)
        f.write("\n\n")
        f.write("node:\n")
        f.write(str(node))
    print("Static Site Generator finished...")

if __name__ == "__main__":
    main()
