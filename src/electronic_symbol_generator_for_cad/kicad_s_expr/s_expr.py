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

    def __getitem__(self, key: int):
        return self._token if key == 0 else self._attributes[key - 1]

    @property
    def attributes(self) -> list[Self | SymbolicAttribute]:
        return [a for a in self._attributes]

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


class SymbolicStylesheet:
    def __init__(self, rules={}):
        self._lineWidth = 80 if "line-width" not in rules else rules["line-width"]
        self._leftTrimmedLineMinWidth = (
            48
            if "left-trimmed-line-min-width" not in rules
            else rules["left-trimmed-line-min-width"]
        )
        self._secabilityThreshold = (
            5 if "secability-threshold" not in rules else rules["secability-threshold"]
        )
        self._indentWidth = 2 if "indent-width" not in rules else rules["indent-width"]

    def dump(self) -> str:
        representation = {
            "line-width": self._lineWidth,
            "left-trimmed-line-min-width": self._minLineWidth,
            "secability-threshold": self._secabilityThreshold,
            "indent-width": self._indentWidth,
        }

    @property
    def line_width(self) -> int:
        return self._lineWidth

    @property
    def left_trimmed_line_min_width(self) -> int:
        return self._leftTrimmedLineMinWidth

    @property
    def secability_threshold(self) -> int:
        return self._secabilityThreshold

    @property
    def indent_width(self) -> int:
        return self._indentWidth


class SymbolicSerdes:
    def __init__(self, stylesheet=SymbolicStylesheet()):
        self._stylesheet = stylesheet  # or default

    def deserialize(self, source: str) -> SymbolicExpression:
        return None

    def serialize(self, source: SymbolicExpression, stylesheet) -> str:
        return None


class SymbolicComparator:
    def __init__(self):
        pass

    def compare(self, left: SymbolicExpression, right: SymbolicExpression) -> bool:
        return False
