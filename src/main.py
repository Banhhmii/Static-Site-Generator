import os
import shutil
from textnode import TextNode,TextType
from htmlnode import *
from recursive_copy_files import copy_contents_recursively
from generate_page import generate_page, generate_page_recursively


def main():
    # location = "./github.com/Banhhmii/src/"
    # source_path = os.path.join(location, "static")
    # dest_path = os.path.join(location, "public")
    
    #source_path = os.path.abspath("./State-Site-Generator/src/static")
    source_path = os.path.abspath("./github.com/Banhhmii/Static-Site-Generator/src/static")
    dest_path = "./github.com/Banhhmii/Static-Site-Generator/src/public"
    dir_path_content = "./github.com/Banhhmii/Static-Site-Generator/src/content"
    dir_path_template = "./github.com/Banhhmii/Static-Site-Generator/src/template.html"
    
    # print("Absolute source path:", source_path)
    # print(os.getcwd())
    # print("Source path exists:", os.path.exists(dest_path))
    # print("Deleting public directory")
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    print("Copying files: ")
    copy_contents_recursively(source_path, dest_path)
    print("Generating page ")
    # generate_page(os.path.join(dir_path_content,"index.md"), dir_path_template, os.path.join(dest_path, "index.html") )
    generate_page_recursively(dir_path_content, dir_path_template, dest_path)
    
    
    
main()