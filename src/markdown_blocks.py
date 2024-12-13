import re
from htmlnode import *
from inline_markdown import text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        if block == "":
            continue
        block = block.strip()
        blocks.append(block)
    return blocks

       
def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_node = block_to_html(block)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes, None) 

def block_to_block_type(block):
    lines = block.split('\n')
    pattern = r"^#{1,6} .+"
    match = re.fullmatch(pattern, block)
    if match:
        return "header"
    if len(lines) > 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return "code"
    if block.startswith('> '):
        for line in lines:
            if not line.startswith('> '):
                return "paragraph"
        return "quote"
    if block.startswith('* '):
        for line in lines:
            if not line.startswith('* '):
                return "paragraph"
        return "unordered list"
    if block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return "paragraph"
        return "unordered list"
    if block.startswith('1. '):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered list"
    return "paragraph"



def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_to_html(block)
    if block_type == "header":
        return header_to_html(block)
    if block_type == "quote":
        return quote_to_html(block)
    if block_type == "unordered list":
        return ulist_to_html(block)
    if block_type == "ordered list":
        return olist_to_html(block)
    if block_type == "code":
        return code_to_html(block)
    raise ValueError("Invalid block type")
       
    
def text_to_childeren(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_childeren(paragraph)
    return ParentNode("p", children)

def header_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 == len(block):
        raise ValueError ("Invalid markdown")
    text = block[level + 1:]
    children = text_to_childeren(text)
    return ParentNode(f"h{level}", children)

def code_to_html(block):
    if not block.startswith("`") or not block.endswith("`"):
        raise ValueError("Invalid code block")
    code = block[4:-3]
    children = text_to_childeren(code)
    html_node = ParentNode("code", children)
    return ParentNode("pre", [html_node])

def quote_to_html(block):
    lines = block.split("\n")
    text = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        text.append(line[2:])
    quote = " ".join(text)
    children = text_to_childeren(quote)
    return ParentNode("blockquote", children)
        

def ulist_to_html(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_childeren(text)        
        html_node = ParentNode("li", children)  
        html_nodes.append(html_node)
    return ParentNode("ul",html_nodes) 

def olist_to_html(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        text = line[3:]
        children = text_to_childeren(text)
        html_node = ParentNode("li", children)
        html_nodes.append(html_node)
    return ParentNode("ol", html_nodes)