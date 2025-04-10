"""
---
(c) 2025 David SPORN
---
This is part of Electronic Symbol Generator for CAD.

Electronic Symbol Generator for CAD is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Electronic Symbol Generator for CAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Electronic Symbol Generator for CAD.
If not, see <https://www.gnu.org/licenses/>.
---
"""

from .base import SymbolicExpression
from .stylesheet import SymbolicStylesheet


class SymbolicSerializer:
    def __init__(self):
        pass

    def serialize(
        self, source: SymbolicExpression, stylesheet: SymbolicStylesheet
    ) -> str:
        return None


class SymbolicSerializerContext:
    def __init__(self, stylesheet: SymbolicStylesheet):
        self._lineAccumulator = ""  # or a string IO ?
        self._lineIndents = [""]
        self._currentIndentLevel = 0
        self._stylesheet = stylesheet

    def canAppendToLine(self, value: str):
        if (
            len(self._lineAccumulator.ltrim())
            < self._stylesheet.left_trimmed_line_min_width
        ):
            return True
        elif len(self._lineAccumulator) < self._stylesheet.line_width:
            return True
        return False

    def incrementIndent(self):
        if self._currentIndentLevel + 1 == len(self._lineIndents):
            self._lineIndents.append(
                self._lineIndents[-1] + " " * self._stylesheet.indent_width
            )
        self._currentIndentLevel = self._currentIndentLevel + 1

    def decrementIndent(self):
        if self._currentIndentLevel > 0:
            self._currentIndentLevel = self._currentIndentLevel - 1

    @property
    def accumulator(self) -> str:
        return self._lineAccumulator

    def consumeAccumulator(self) -> str:
        result = self._lineAccumulator
        self._lineAccumulator = "" + self._lineIndents[self._currentIndentLevel]


class SymbolicSerializerToString(SymbolicSerializer):

    def __init__(self):
        pass

    def serialize(
        self, source: SymbolicExpression, stylesheet: SymbolicStylesheet
    ) -> str:
        lineAccumulator = ""
        lineIndent = [""]
        stack = [source]

        return None
