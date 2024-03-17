from dataclasses import dataclass
from baum.node import Node

OPENING = {'[', '('}
CLOSING = {']', ')'}
EOF = '<EOF>'
COMMA = ','
WHITESPACE = {' ', '\t'}
PUNCTUATION = OPENING.union(CLOSING).union({EOF, COMMA})

@dataclass
class ParseState:
    raw: str
    i: int = 0

    @property
    def current(self) -> str:
        if self.i < len(self.raw):
            return self.raw[self.i]
        else:
            return EOF

def skip_whitespace(state: ParseState):
    while state.current in WHITESPACE:
        state.i += 1

def parse_identifier(state: ParseState) -> str:
    ident = ''
    while state.current not in PUNCTUATION:
        ident += state.current
        state.i += 1
    return ident

def parse_comma(state: ParseState) -> bool:
    if state.current == COMMA:
        state.i += 1
        return True
    else:
        return False

def expect_opening(state: ParseState):
    if state.current not in OPENING:
        raise ValueError(f'Expected opening bracket at {state.i}')
    state.i += 1

def expect_closing(state: ParseState):
    if state.current not in CLOSING:
        raise ValueError(f'Expected closing bracket at {state.i}')
    state.i += 1

def parse_expr(state: ParseState) -> Node:
    children = None

    skip_whitespace(state)

    # Parse name identifier
    name = parse_identifier(state)

    # Parse children
    if state.current in OPENING:
        children = []
        expect_opening(state)
        skip_whitespace(state)

        if state.current not in CLOSING:
            children.append(parse_expr(state))
            skip_whitespace(state)

            while parse_comma(state):
                skip_whitespace(state)
                children.append(parse_expr(state))
                skip_whitespace(state)

        expect_closing(state)

    return Node(name.strip(), children)

def parse(raw: str) -> Node:
    return parse_expr(ParseState(raw))
