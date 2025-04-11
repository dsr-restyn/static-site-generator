from src.helpers import *
import os
import shutil


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


def main():
    print("Static Site Generator started...")
    print("Parsing markdown...")
    copy_static_to_public("static", "public")
    generate_page(
        "content/index.md", "template.html", "public/index.html"
    )
    print("Static Site Generator finished...")

if __name__ == "__main__":
    main()
