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

from .stream import SymbolicInputStream


class SymbolicStreamComparator:
    """Try to answer whether two sources of symbolic expression of data are "the same" or not.

    Being "the same" means that without regards to whitespaces separing any meaningfull "chunk" of
    an s-expression, both sources emit the same sequence of "chunks".capitalize

    A "chunk" is one of :

    * '(', i.e. the opening of an s-expression
    * ')', i.e. the closing of an s-expression
    * the token of the s-expression
    * an attribute of the s-expression when it is not an sub-s-expression

    """

    def __init__(self, left: io.TextIOBase, right: io.TextIOBase):
        self._left = SymbolicInputStream(left)
        self._right = SymbolicInputStream(right)
        self._latestLeft = None
        self._latestRight = None

    def _compareNextChunk(self) -> bool:
        return self._latestLeft == self._latestRight

    def _hasNextChunk(self) -> bool:
        self._latestLeft = self._left.readNext()
        self._latestRight = self._right.readNext()
        print(f"next chunks : {self._latestLeft} <=> {self._latestRight}")
        return self._latestLeft is not None or self._latestRight is not None

    @staticmethod
    def areEqual(left: io.TextIOBase, right: io.TextIOBase) -> bool:
        comparator = SymbolicStreamComparator(left, right)
        while comparator._hasNextChunk():
            if comparator._compareNextChunk():
                continue
            else:
                return False
        return True
