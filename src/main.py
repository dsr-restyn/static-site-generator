from helpers import *

def main():
    print("Static Site Generator started...")
    print("Parsing markdown...")
    md = """# Sample Markdown

    This is some basic, sample markdown.

    ## Second Heading

      - One
      - Two
      - Three

    > Blockquote

    > More Blockquote

    And **bold**, _italics_, and even _italics and later **bold**__. Even ~~strikethrough~~. [A link](https://markdowntohtml.com) to somewhere.

    And code highlighting:

    ```js
    var foo = 'bar';

    function baz(s) {
       return foo + ':' + s;
    }
    ```

    Or inline code like `var foo = 'bar';`.

    Or an image of bears

    ![bears](http://placebear.com/200/200)

    The end ...

        """
    # print(f"{md=}")
    node = markdown_to_html_node(md)
    # print(f"{node=}")
    html = node.to_html()
    with open("template.html", "w") as f:
        f.write(html)
        f.write("\n\n")
        f.write("node:\n")
        f.write(str(node))
    print("Static Site Generator finished...")

if __name__ == "__main__":
    main()
