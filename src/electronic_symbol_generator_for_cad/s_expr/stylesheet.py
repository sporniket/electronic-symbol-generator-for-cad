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
