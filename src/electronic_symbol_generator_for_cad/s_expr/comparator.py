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

_MARKER_BEGIN = "((BEGIN))"
_MARKER_END = "((END))"


class DebugContext:
    def __init__(self, size: int = 20):
        if size <= 0:
            raise ValueError("wrong.context.size:{size}")
        self._size = size
        self._context = [("", "") for i in range(size)]
        self._head = 0
        self._tail = 0
        self.append(_MARKER_BEGIN, _MARKER_BEGIN)

    def append(self, left: str, right: str):
        contextItem = (
            _MARKER_END if left is None else left,
            _MARKER_END if right is None else right,
        )
        self._context[self._tail] = contextItem
        self._tail = (self._tail + 1) % self._size
        if self._tail == self._head:
            self._head = (self._head + 1) % self._size

    def __getitem__(self, index):
        if index >= self.__len__():
            raise IndexError(index)
        actualItem = (self._head + index) % self._size
        return self._context[actualItem]

    def __len__(self):
        result = self._tail - self._head
        return result + self._size if result < 0 else result


class SymbolicStreamComparatorResult:
    def __init__(self, result: bool, context: list[tuple]):
        self.result = result
        self.context = context


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

    def __init__(
        self, left: io.TextIOBase, right: io.TextIOBase, *, debugContextSize: int = 20
    ):
        self._left = SymbolicInputStream(left)
        self._right = SymbolicInputStream(right)
        self._debug = DebugContext(debugContextSize)
        self._latestLeft = None
        self._latestRight = None

    def _compareNextChunk(self) -> bool:
        return self._latestLeft == self._latestRight

    def _hasNextChunk(self) -> bool:
        self._latestLeft = self._left.readNext()
        self._latestRight = self._right.readNext()
        self._debug.append(self._latestLeft, self._latestRight)
        return self._latestLeft is not None or self._latestRight is not None

    @staticmethod
    def areEqual(
        left: io.TextIOBase, right: io.TextIOBase
    ) -> SymbolicStreamComparatorResult:
        comparator = SymbolicStreamComparator(left, right)
        while comparator._hasNextChunk():
            if comparator._compareNextChunk():
                continue
            else:
                return SymbolicStreamComparatorResult(False, list(comparator._debug))
        return SymbolicStreamComparatorResult(True, list(comparator._debug))
