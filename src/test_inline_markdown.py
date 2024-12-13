import unittest

from textnode import *
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    
    def test_delim_italics(self):
        node = TextNode("This is a text with an *italicized* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("italicized", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,               
        )
        
    def test_delim_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,               
        )

    def test_delim_bold_and_italics(self):
        node = TextNode("**Bold** and *italicized* words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italicized", TextType.ITALIC),
                TextNode(" words", TextType.TEXT),
            ],
            new_nodes,               
        )
    
    def test_multiwords(self):
        node = TextNode("This is a **bold word** and so is **this**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" and so is ", TextType.TEXT),
                TextNode("this", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code block", TextType.CODE)
            ],
            new_nodes
        )
        
    def test_extract_link(self):
        s = "This is a text with a link [anime](https://www.crunchyroll.com)"
        test = extract_markdown_links(s)
        lst = [('anime', 'https://www.crunchyroll.com')]
        
        self.assertListEqual(test, lst)
        
    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test = extract_markdown_links(text)
        lst = [('to boot dev', 'https://www.boot.dev'), ('to youtube','https://www.youtube.com/@bootdotdev')]
        
        self.assertListEqual(test, lst)
        
    def test_extract_image(self):
        text = "this is a text with a ![anime](https://i.imgur.com/aKaOqIh.gif)"
        test = extract_markdown_images(text)
        lst = [('anime', 'https://i.imgur.com/aKaOqIh.gif')]
        
        self.assertListEqual(test, lst)
        
    def test_extract_images(self):
        text = "This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test = extract_markdown_images(text)
        lst = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        
        self.assertListEqual(test, lst)
        
class TestImageAndLinkSplits(unittest.TestCase):
    
    def test_split_image(self):
        node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
            TextType.TEXT
        )
        new_nodes =(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
            ]
        )
        test = split_nodes_images([node])
        self.assertListEqual(test, new_nodes)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT
        )
        new_nodes =(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )
        test = split_nodes_images([node])
        self.assertListEqual(test, new_nodes)
        
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT
        )
        new_nodes =(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ]
        )
        test = split_nodes_links([node])
        self.assertListEqual(test, new_nodes)
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes =(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ]
        )
        test = split_nodes_links([node])
        self.assertListEqual(test, new_nodes)
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        lst = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        test = text_to_textnodes(text)
        print(test)
        self.maxDiff = None
        self.assertListEqual(lst, test)

        
if __name__ == "__main__":
    unittest.main()

    # def test_split_nodes(self):
    #     node = TextNode("This is text with a `code block` word", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
    #     expected_nodes = [
    #         TextNode("This is text with a ", TextType.TEXT),
    #         TextNode("code block", TextType.CODE),
    #         TextNode(" word", TextType.TEXT)
    #     ]
    #     print(new_nodes)
    #     self.assertEqual(new_nodes, expected_nodes)
    
    # def test_no_split(self):
    #     node = TextNode("Just normal text", TextType.TEXT)
    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node], "", TextType.TEXT)
    
    # def test_split_noMatchDelims(self):
    #     node = TextNode("A string without a *code block", TextType.TEXT)
    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node],"*", TextType.CODE)     
    
    # def test_split_at_beginning(self):
    #     node = TextNode("**Italics** with normal text", TextType.TEXT)

    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node], "**", TextType.TEXT)
    
    # def test_unmatched_delims(self):
    #     node = TextNode("This text has and *unmatched delimiter", TextType.TEXT)
    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node], "*", TextType.BOLD)
    
    # def test_empty_delims(self):
    #     node = TextNode("This text has ``empty block", TextType.TEXT)
    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node], "`", TextType.CODE)
    
    # def test_multiple_delims(self):
    #     node = TextNode("This is *bold text* with more *bold text*", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
    #     expected_nodes = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("bold text", TextType.BOLD),
    #         TextNode(" with more ", TextType.TEXT),
    #         TextNode("bold text", TextType.BOLD)
    #     ]
    #     print(new_nodes)
    #     self.assertEqual(new_nodes, expected_nodes)
        