from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        #(type) string
        self.value = value
        #(type) dictionary
        self.children = children 
        #a dictionary of key-value pairs representing attributes of html tags
        self.props = props 
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        prop_html = ""
        for prop in self.props:
            prop_html +=  f' {prop}="{self.props[prop]}"'
        return prop_html
    
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError ("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return (f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
    
    def __repr__(self):

        return (f"LeafNode({self.tag}, {self.value}, {self.props})")
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
        
    def to_html(self):
        if self.tag == None:
            raise ValueError ("All parent nodes must have a tag")
        if self.children == None:
            raise ValueError ("All parent nodes must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
        
        