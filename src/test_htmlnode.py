import unittest

from htmlnode import *

from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        
    def test_no_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode(
            "div", 
            "One to cut",
            None,
            {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(node.__repr__(), "HTMLNode(div, One to cut, None, {'href': 'https://www.google.com', 'target': '_blank'})")
        
    def test_Leaf_with_noProps(self):
        node = LeafNode("p", "This is a paragraph", None)
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
    
    def test_Leaf_with_noTag(self):
        node = LeafNode(None, "This is just a string", None)
        self.assertEqual(node.to_html(), "This is just a string")
        
        
    def test_ParentNode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold Text"),
                LeafNode(None, "Normal Text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold Text</b>Normal Text</p>")
    
    def test_nested_ParentNode(self):
        nested_node = ParentNode(
        "div",
        [
            ParentNode(
                "p",
                [
                    LeafNode("span", "Hello"),
                    LeafNode(None, " "),
                    LeafNode("b", "World")
                ]
            ),
            LeafNode(None, "!")
        ]
    )
        self.assertEqual(nested_node.to_html(), "<div><p><span>Hello</span> <b>World</b></p>!</div>")

    # def test_ParentNode_no_tag(self):
    #     node = ParentNode(
    #         "",  
    #         [
    #             LeafNode("b", "Bold text"),
    #             LeafNode(None, "Normal text")
    #         ]
    #     )
    #     with self.assertRaises(ValueError):
    #        node.to_html()
           
class TestTextToHTMLNode(unittest.TestCase):
           
    def test_textNode_bold(self):
        node = TextNode("This text is bold", TextType.BOLD)
        textToHTML = text_node_to_html_node(node)
        self.assertEqual(textToHTML.__repr__(), f"LeafNode({textToHTML.tag}, {textToHTML.value}, {textToHTML.props})")
    
    def test_textNode_text(self):
        node = TextNode("This is normal text", TextType.TEXT)
        textToHTML = text_node_to_html_node(node)
        self.assertEqual(textToHTML.__repr__(), f"LeafNode(None, This is normal text, None)")
    
    def test_textNode_code(self):
        node = TextNode("This text is code type", TextType.CODE)
        textToHTML = text_node_to_html_node(node)
        self.assertEqual(textToHTML.__repr__(), f"LeafNode(code, This text is code type, None)")
    
    def test_textNode_italics(self):
        node = TextNode("This text is italicized", TextType.ITALIC)
        textToHTML = text_node_to_html_node(node)
        self.assertEqual(textToHTML.__repr__(), f"LeafNode(i, This text is italicized, None)")
    
    def test_textNode_link(self):
        node = TextNode("This text is a link", TextType.LINK, "https://www.google.com")
        textToHTML = text_node_to_html_node(node)
        textToHTML.__repr__()
        self.assertEqual(textToHTML.__repr__(), f"LeafNode(a, This text is a link, {{'href': 'https://www.google.com'}})")
    
    def test_textNode_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "www.img.com")
        textToHTML = text_node_to_html_node(node)
        self.assertEqual(textToHTML.__repr__(), f"LeafNode(img, , {{'src': 'www.img.com', 'alt': 'This is an image'}})")

if __name__ == "__main__":
    unittest.main()