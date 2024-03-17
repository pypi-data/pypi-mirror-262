from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    name: str
    children: Optional[list[Node]] = None
