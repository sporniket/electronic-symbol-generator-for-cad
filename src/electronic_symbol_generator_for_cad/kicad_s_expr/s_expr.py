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

import re
from typing import Self

_MATCHER__NUMBER = re.compile("^[-+]?\\d*([.]\\d+)$")
_MATCHER__TOKEN = re.compile("^[a-z_]+$")


class SymbolicAttribute:
    def __init__(self, value: int | float | bool | str):
        if value is None:
            self._isNumber = False
            self._value = ""
        elif isinstance(value, bool):
            self._isNumber = True
            self._value = "yes" if value else "no"
        elif isinstance(value, int | float):
            self._isNumber = True
            self._value = f"{value}"
        elif _MATCHER__NUMBER.match(value):
            self._isNumber = True
            self._value = value
        else:
            sanitizedValue = value.replace("\\", "\\\\")
            sanitizedValue = sanitizedValue.replace('"', '\\"')
            self._isNumber = False
            self._value = sanitizedValue

    def toString(self):
        return self._value if self._isNumber else f'"{self._value}"'


class SymbolicExpression:
    def __init__(
        self,
        token: str,
        attributes: list[int | float | bool | str | Self | SymbolicAttribute],
    ):
        if not _MATCHER__TOKEN.match(token):
            raise RuntimeError(f"Not a token : {token}")
        self._token = token
        self._attributes = [
            (
                a
                if isinstance(a, SymbolicExpression | SymbolicAttribute)
                else SymbolicAttribute(a)
            )
            for a in attributes
        ]

    @property
    def symbolCount(self) -> int:
        length = 1
        for a in self._attributes:
            if isinstance(a, SymbolicExpression):
                length = length + a.symbolCount
            else:
                length = length + 1
        return length

    def hasSymbolCountUnder(self, thresholdInSymbolsCount: int) -> bool:
        if thresholdInSymbolsCount <= 1:
            return False
        elif thresholdInSymbolsCount == 2 and len(self._attributes) > 0:
            return False
        available = thresholdInSymbolsCount - 1
        for a in self._attributes:
            if available <= 1:
                return False
            if isinstance(a, SymbolicExpression):
                if not a.hasSymbolCountUnder(available):
                    return False
                available = available - a.symbolCount
            else:
                available = available - 1
        return True
