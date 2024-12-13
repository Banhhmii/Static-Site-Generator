from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
    
        split_nodes = []
        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
    
        for i in range(len(sections)):
            #Don't add an empty string back into the node after split happens
            if sections[i] == "":
                continue
            #even index position typically means normal text where odd means different text type i.e. (bold, italic, code)
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))  #side note .append only adds one item at a time to a list
            else:
                split_nodes.append(TextNode(sections[i], text_type))
                
        new_nodes.extend(split_nodes) #extends can more than one item to the list

    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue 
        original_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        for image in images:
            image_syntax = f"![{image[0]}]({image[1]})"
            sections = original_text.split(image_syntax, 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))     
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    
    

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_images(nodes)

    return nodes
    
def extract_markdown_images(text):
    # list_of_tups = []
    image_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    # list_of_tups.append(f"{image_text}")

    return image_text

def extract_markdown_links(text):
    #list_of_tups = []
    links_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return links_text 



    # if delimiter == None or delimiter == "":
    #     raise ValueError ("Delimiter is empty or not found")  
    
    # for node in old_nodes:
    #     if node.text_type != TextType.TEXT:
    #         new_nodes.append(node)
    #     elif node.text_type == TextType.TEXT:
    #         first_delim = node.text.find(delimiter)
    #         second_delim = node.text.find(delimiter, first_delim + 1)
    #         delim_length = len(delimiter)
            
    #         if node.text.startswith(delimiter):
    #             raise ValueError("Cannot start with delimiter")
            
    #         if first_delim == -1:
    #             new_nodes.append(node)
    #             continue
            
    #         if second_delim == -1:
    #             raise ValueError("No closing delimiter pair found")      
                   
    #         if second_delim == first_delim + delim_length:
    #             raise ValueError("Empty delimiters")
            

    #         else:
                
    #         # Instead of splitting all at once, process one pair at a time
    #          before = node.text[:first_delim]
    #          middle = node.text[first_delim + delim_length:second_delim]
    #          after = node.text[second_delim + delim_length:]

    #         # Add nodes in order
    #         if before:
    #             new_nodes.append(TextNode(before, TextType.TEXT))
    #         new_nodes.append(TextNode(middle, text_type))
    #         if after:
    #             new_nodes.append(TextNode(after, TextType.TEXT))
            
    #             # for index, text_segment in enumerate(split_node):
    #             #     if index % 2 == 1 and text_segment == "":
    #             #         raise ValueError ("Empty delimiter")
    #             #     if index % 2 == 1:
    #             #         newText = TextNode(text_segment, text_type)
    #             #         new_nodes.append(newText)
    #             #     elif index % 2 == 0:
    #             #         newText = TextNode(text_segment, TextType.TEXT)
    #             #         new_nodes.append(newText)
