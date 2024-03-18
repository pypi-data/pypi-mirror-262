"""
Library of nodes for common use cases.
"""

from typing import Any

from .ast import BaseNode, BaseBlockNode


class InlineTextNode(BaseNode):

    text: str

    def __init__(self, text: str):
        super().__init__(text=text)

    def visit(self) -> str:
        return self.text


class BlockTextNode(BaseNode):

    lines: list[str]

    def __init__(self, lines: list[str]):
        super().__init__(lines=lines)

    def visit(self) -> list[str]:
        return self.lines


# TODO: handle multi-block: ... } else if (...) { ...)
# - iter() / depart()?
#   - multiple iter() invocations, single depart()
#   - iter(): wraps visit() in a loop until StopIteration raised?


class TokenBlockNode(BaseBlockNode):
    """
    Block with descriptor and start/end tokens.

    [descriptor][spacer][start_token]
        [children]
    [end_token]
    """

    descriptor: str = ""

    spacer: str = " "
    """
    Provide optional whitespace between descriptor and block content.

    Examples with `descriptor = "void foo(void)"`:

    `spacer = " "`:

    ```c
    void foo(void) {
        ...
    }
    ```

    `spacer = "\n"`:

    ```c
    void foo(void)
    {
        ...
    }
    ```
    """

    start_token: str = ""

    end_token: str = ""

    def model_post_init(self, __context: Any):
        self._prolog = InlineTextNode(
            f"{self.descriptor}{self.spacer}{self.start_token}"
        )
        self._epilog = InlineTextNode(f"{self.end_token}")


class CurlyBracketBlockNode(TokenBlockNode):
    start_token: str = "{"
    end_token: str = "}"


class SquareBracketBlockNode(TokenBlockNode):
    start_token: str = "["
    end_token: str = "]"


class AngleBracketBlockNode(TokenBlockNode):
    start_token: str = "<"
    end_token: str = ">"
