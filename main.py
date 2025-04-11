from src.helpers import *
import os
import shutil
import sys

BASEPATH = sys.argv[1] or "/"


def copy_static_to_public(static_dir, public_dir):
    # Clear the public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

    # Recursive function to copy files and directories
    def copy_recursive(src, dest):
        if os.path.isdir(src):
            os.makedirs(dest, exist_ok=True)
            for item in os.listdir(src):
                copy_recursive(os.path.join(src, item), os.path.join(dest, item))
        else:
            shutil.copy2(src, dest)
            print(f"Copied {src} to {dest}")

    # Start copying from static to public
    copy_recursive(static_dir, public_dir)


def copy_and_generate_content(content_dir, public_dir, template_file):
    # Recursive function to process markdown files and directories
    def process_content(src, dest):
        if os.path.isdir(src):
            os.makedirs(dest, exist_ok=True)
            for item in os.listdir(src):
                process_content(os.path.join(src, item), os.path.join(dest, item))
        elif src.endswith(".md"):
            output_file = dest.replace(".md", ".html")
            generate_page(src, template_file, output_file, BASEPATH)
            print(f"Generated page from {src} to {output_file}")
        else:
            shutil.copy2(src, dest)
            print(f"Copied {src} to {dest}")

    # Start processing from content to public
    process_content(content_dir, public_dir)


def main():
    print("Static Site Generator started...")
    print("Parsing markdown...")
    copy_static_to_public("static", "docs")
    copy_and_generate_content("content", "docs", "template.html")
    print("Static Site Generator finished...")

if __name__ == "__main__":
    main()
