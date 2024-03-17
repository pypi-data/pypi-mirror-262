from dataclasses import dataclass
from typing import Optional

@dataclass
class Style:
    indent_prefix: str = ''
    t_prefix: str = ''
    last_prefix: Optional[str] = None
    leaf_prefix: Optional[str] = None
    include_root: bool = False

STYLES = {
    'ascii': Style(indent_prefix='|', t_prefix='+-', last_prefix='\\-'),
    'ascii2': Style(indent_prefix='|', t_prefix='+-', last_prefix='`-'),
    'ascii-compact': Style(indent_prefix='|', t_prefix='+', last_prefix='\\'),
    'ascii2-compact': Style(indent_prefix='|', t_prefix='+', last_prefix='`'),
    'arrows': Style(indent_prefix='|', t_prefix='->'),
    'harrows': Style(indent_prefix='|', t_prefix='#>'),
    'bars': Style(indent_prefix='|', t_prefix='|'),
    'yaml': Style(t_prefix='-', last_prefix='-'),
    'empty': Style(),
    'compact': Style(indent_prefix='│', t_prefix='├', last_prefix='└'),
    'unicode': Style(indent_prefix='│', t_prefix='├─', last_prefix='└─'),
    'emoji': Style(t_prefix='📁', leaf_prefix='📄', include_root=True),
}
