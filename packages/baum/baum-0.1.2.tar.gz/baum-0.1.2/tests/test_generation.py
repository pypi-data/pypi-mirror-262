import unittest
import textwrap

from baum.node import Node
from baum.generate import generate
from baum.options import Options
from baum.style import STYLES, Style

class TestGeneration(unittest.TestCase):
    def test_generation(self):
        tree = Node(
            name='the',
            children=[
                Node(name='quick', children=[Node(name='brown'), Node(name='fox')]),
                Node(name='jumps'),
            ]
        )

        self.assertEqual(self.generate(tree, 'unicode'), textwrap.dedent('''\
            the
            ├─ quick
            │  ├─ brown
            │  └─ fox
            └─ jumps'''))
        self.assertEqual(self.generate(tree, 'ascii'), textwrap.dedent('''\
            the
            +- quick
            |  +- brown
            |  \\- fox
            \\- jumps'''))
        self.assertEqual(self.generate(tree, 'ascii-compact'), textwrap.dedent('''\
            the
            + quick
            | + brown
            | \\ fox
            \\ jumps'''))
        self.assertEqual(self.generate(tree, 'ascii2-compact'), textwrap.dedent('''\
            the
            + quick
            | + brown
            | ` fox
            ` jumps'''))
        self.assertEqual(self.generate(tree, 'arrows'), textwrap.dedent('''\
            the
            -> quick
            |  -> brown
            |  -> fox
            -> jumps'''))
        self.assertEqual(self.generate(tree, 'harrows'), textwrap.dedent('''\
            the
            #> quick
            |  #> brown
            |  #> fox
            #> jumps'''))
        self.assertEqual(self.generate(tree, 'bars'), textwrap.dedent('''\
            the
            | quick
            | | brown
            | | fox
            | jumps'''))
        self.assertEqual(self.generate(tree, 'yaml'), textwrap.dedent('''\
            the
            - quick
              - brown
              - fox
            - jumps'''))
        self.assertEqual(self.generate(tree, 'empty'), textwrap.dedent('''\
            the
             quick
              brown
              fox
             jumps'''))
        self.assertEqual(self.generate(tree, 'compact'), textwrap.dedent('''\
            the
            ├ quick
            │ ├ brown
            │ └ fox
            └ jumps'''))
        self.assertEqual(self.generate(tree, 'emoji'), textwrap.dedent('''\
            📁 the
              📁 quick
                📄 brown
                📄 fox
              📄 jumps'''))

    def make_options(self, style: Style) -> Options:
        return Options(
            style=style,
            spaces=1,
            include_root=style.include_root,
            debug=False
        )
    
    def generate(self, node: Node, style: str) -> str:
        return generate(node, self.make_options(STYLES[style]))
