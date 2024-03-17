import unittest

from baum.node import Node
from baum.parse import parse

class TestParse(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse('a'), Node(name='a'))
        self.assertEqual(parse('a[]'), Node(name='a', children=[]))
        self.assertEqual(parse('a[b, c]'), Node(name='a', children=[Node(name='b'), Node(name='c')]))
        self.assertEqual(parse('the[quick[brown], fox[jumps, over], the lazy dog]'), Node(
            name='the',
            children=[
                Node(
                    name='quick',
                    children=[
                        Node(name='brown'),
                    ]
                ),
                Node(
                    name='fox',
                    children=[
                        Node(name='jumps'),
                        Node(name='over'),
                    ],
                ),
                Node(
                    name='the lazy dog',
                ),
            ],
        ))
