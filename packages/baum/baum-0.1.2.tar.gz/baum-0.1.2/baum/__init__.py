import argparse

from baum.options import Options
from baum.parse import parse
from baum.generate import generate
from baum.style import STYLES

def main():
    parser = argparse.ArgumentParser(description='Generates ASCII/Unicode trees')
    parser.add_argument('--style', type=str, default='unicode', choices=sorted(STYLES.keys()), metavar='STYLE', help=f"The tree style (one of {', '.join(sorted(STYLES.keys()))})")
    parser.add_argument('--spaces', type=int, default=1, help='Number of spaces before each label')
    parser.add_argument('--include-root', action='store_true', help='Whether to prefix the root with a stylized node')
    parser.add_argument('--debug', action='store_true', help="Prints the tree's Python expression")
    parser.add_argument('expr', type=str, help='The parenthesized tree expression')

    args = parser.parse_args()
    style = STYLES[args.style]
    opts = Options(
        style=style,
        spaces=args.spaces,
        include_root=args.include_root or style.include_root,
        debug=args.debug
    )

    node = parse(args.expr)
    generated = generate(node, opts)

    print(generated)
