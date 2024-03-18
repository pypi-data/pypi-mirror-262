"""
Abstract syntax tree for generating arbitrary structured code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

INDENT_WIDTH: int = 4
"""
Number of spaces for indentation.
"""


class BaseNode(BaseModel, ABC):
    """
    Base node -- the most important class of this package. Users instantiate
    a concrete class and invoke render(), which in turn invokes the
    concrete class's visit() recursively.
    """

    model_config = ConfigDict(extra="forbid")

    @abstractmethod
    def visit(self) -> str | Iterable[str]:
        """
        Return non-indented line or lines to produce upon
        visiting this node.

        This base class is considered a leaf node - it does not support
        child nodes. See the subclass subclass {obj}`BaseBranchNode`
        which supports child nodes.
        """
        ...

    def render(self) -> str:
        """
        Return rendered text of this node.
        """
        return "\n".join(self._render_lines())

    def render_file(self, path: Path, filename: str | None = None):
        """
        Render to provided file or folder path. If path is a folder
        and filename is not provided, filename defaults to the class name
        with .txt extension.
        """

        # get the file path
        path_file: Path

        if path.is_dir():
            filename_: str = (
                f"{self.__class__.__name__}.txt"
                if filename is None
                else filename
            )
            path_file = path / filename_
        else:
            path_file = path

        with open(path_file, "w") as fh:
            fh.write(self.render())

    def _render_lines(self, depth: int = 0) -> list[str]:
        """
        Return a list of indented lines representing this node.
        """

        # invoke visit() and normalize
        visit_lines: list[str] = self._normalize_lines(self.visit())

        # return indented lines
        return self._indent_lines(visit_lines, depth)

    def _normalize_lines(self, lines: str | list[str]) -> list[str]:

        if isinstance(lines, Iterable) and not isinstance(lines, str):
            return list(lines)
        else:
            return [lines]

    def _indent_line(self, line: str, depth: int) -> str:
        return f"{depth * INDENT_WIDTH * ' '}{line}"

    def _indent_lines(self, lines: Iterable[str], depth: int) -> list[str]:
        return [self._indent_line(line, depth) for line in lines]


class BaseBranchNode(BaseNode, ABC):
    """
    Node which can contain children, rendered in between visit()
    and depart() invocations.
    """

    children: list[BaseNode] = Field(default_factory=list)

    indent_children: bool = True

    @abstractmethod
    def depart(self) -> str | Iterable[str]:
        """
        Return non-indented line or lines to produce upon
        departing this node. Invoked after rendering children.
        """

    def add_child(self, node: BaseNode):
        self.children.append(node)

    def _render_lines(self, depth: int = 0) -> list[str]:

        # invoke visit() and get indented lines
        lines: list[str] = super()._render_lines(depth=depth)

        # render children at next depth
        for child in self.children:
            child_depth: int = depth + 1 if self.indent_children else depth
            lines += child._render_lines(depth=child_depth)

        # invoke depart() and normalize
        depart_lines: list[str] = self._normalize_lines(self.depart())

        # append indented depart lines
        lines += self._indent_lines(depart_lines, depth=depth)

        # return indented lines
        return lines


# TODO: hide fields with leading underscores in vscode
# - only for development convenience; enforced correctly at runtime
# - workaround here, but let's just wait until it's properly fixed in
#   the toolchain:
#   https://github.com/pydantic/pydantic/discussions/4563#discussioncomment-3727730
class BaseBlockNode(BaseBranchNode):
    """
    Base representation of an optional prolog/epilog with
    one or more child nodes, optionally surrounded by a
    prolog and/or epilog which constitute a "block".

    [prolog]
        [children]
    [epilog]
    """

    _prolog: BaseNode | None = PrivateAttr(default=None)

    _epilog: BaseNode | None = PrivateAttr(default=None)

    def visit(self) -> list[str]:
        return self._render_end_node(self._prolog)

    def depart(self) -> list[str]:
        return self._render_end_node(self._epilog)

    def _render_end_node(self, node: BaseNode | None) -> list[str]:
        return node._render_lines() if node is not None else []
