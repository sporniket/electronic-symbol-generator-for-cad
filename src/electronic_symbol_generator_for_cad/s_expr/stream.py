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

import io
from enum import Enum
import string

_MARKER_PARENTHESIS = ["(", ")"]
_MARKER_QUOTES = ['"']


class SymbolicInputStream:
    def __init__(self, source: io.TextIOBase):
        self._source = source

    def _readFirstNonWhiteChar(self) -> str | None:
        while nextChar := self._source.read(1):
            if nextChar not in string.whitespace:
                return nextChar
        return None

    def readNext(self) -> str | None:
        quoteMark = None
        accumulator = self._readFirstNonWhiteChar()
        if accumulator is None:
            return None
        if accumulator in _MARKER_PARENTHESIS:
            return accumulator
        if accumulator in _MARKER_QUOTES:
            quoteMark = accumulator

        escape = False
        while (nextChar := self._source.read(1)) is not None:
            if quoteMark:
                if not escape and nextChar == quoteMark:
                    return accumulator + nextChar
            else:
                if nextChar in string.whitespace:
                    return accumulator
            accumulator = accumulator + nextChar
            if escape:
                escape = False
            elif nextChar == "\\" and quoteMark:
                escape = True
        if not quoteMark:
            return accumulator
        raise ValueError("premature.stream.end")
