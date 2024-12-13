from markdown_blocks import *
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise ValueError ("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as md_file:
        md_content = md_file.read()
        md_file.close()
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
        template_file.close()
    html_node = markdown_to_html(md_content)
    html_string = html_node.to_html()
    title = extract_title(md_content)
    
    template_content = template_content.replace(f"{{ Title }}", title)
    template_content = template_content.replace(f"{{ Content }}", html_string)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path == "":
        os.makedirs(dest_dir_path, exist_ok=True)
    write_file = open(dest_path, "w")
    write_file.write(template_content)
    write_file.close()
    
def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    for files in entries:
        

    