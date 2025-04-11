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
        self._left = left
        self._right = right

    def compareNextChunk(self) -> bool:
        return False

    def hasNextChunk(self) -> bool:
        return False

    @staticmethod
    def areEqual(left: io.TextIOBase, right: io.TextIOBase) -> bool:
        comparator = SymbolicStreamComparator(left, right)
        while comparator.hasNextChunk():
            if comparator.compareNextChunk():
                continue
            else:
                return False
        return True
