from dataclasses import dataclass
from baum.style import Style

@dataclass
class Options:
    style: Style
    spaces: int
    include_root: bool
    debug: bool
