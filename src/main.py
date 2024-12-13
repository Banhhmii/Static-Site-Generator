import os
import shutil
from textnode import TextNode,TextType
from htmlnode import *
from recursive_copy_files import copy_contents_recursively
from generate_page import generate_page


def main():
    # location = "./github.com/Banhhmii/src/"
    # source_path = os.path.join(location, "static")
    # dest_path = os.path.join(location, "public")
    
    source_path = os.path.abspath("./src/static")
    dest_path = "./src/public"
    dir_path_content = "./src/content"
    dir_path_template = "./src/template.html"
    
    print("Absolute source path:", source_path)
    print("Source path exists:", os.path.exists(source_path))
    print("Deleting public directory")
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    print("Copying files: ")
    copy_contents_recursively(source_path, dest_path)
    print("Generating page ")
    generate_page(os.path.join(dir_path_content,"index.md"), dir_path_template, os.path.join(dest_path, "index.html") )
    
    
    
    
main()