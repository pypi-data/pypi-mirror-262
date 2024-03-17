from enum import Enum
from typing import Iterable
from baum.node import Node
from baum.options import Options

def prefix_with(prefix: str, lines: list[str]) -> Iterable[str]:
    for line in lines:
        yield prefix + line

class NodeKind(Enum):
    DEFAULT = 0
    LAST = 1
    ROOT = 2

def generate_node(node: Node, opts: Options, kind: NodeKind=NodeKind.DEFAULT) -> Iterable[str]:
    # Compute prefix
    if kind == NodeKind.ROOT:
        prefix = ''
    else:
        if node.children is None and opts.style.leaf_prefix:
            prefix = opts.style.leaf_prefix
        elif kind == NodeKind.DEFAULT:
            prefix = opts.style.t_prefix
        elif kind == NodeKind.LAST:
            prefix = opts.style.last_prefix if opts.style.last_prefix is not None else opts.style.t_prefix
        else:
            raise ValueError(f'Unimplemented node kind: {kind}')
        prefix += ' ' * opts.spaces

    # Compute indent
    if kind == NodeKind.ROOT:
        indent = ''
    elif kind == NodeKind.LAST:
        indent = ' ' * len(prefix)
    else:
        indent = opts.style.indent_prefix + (' ' * (len(prefix) - len(opts.style.indent_prefix)))

    # Assemble lines
    yield prefix + node.name
    if node.children is not None:
        for i, child in enumerate(node.children):
            child_kind = NodeKind.LAST if i == len(node.children) - 1 else NodeKind.DEFAULT
            yield from prefix_with(indent, list(generate_node(child, opts, child_kind)))

def generate(node: Node, opts: Options) -> str:
    if opts.debug:
        return str(node)
    return '\n'.join(generate_node(node, opts, NodeKind.LAST if opts.include_root else NodeKind.ROOT))
