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

from electronic_symbol_generator_for_cad.s_expr import SymbolicInputStream


def test_read_can_read_symbols_from_streams():
    source = """(a "b c" 3.14 (
    d "\\"e\\\\\\"f")(g)
)"""
    stream = SymbolicInputStream(io.StringIO(source))
    for expected in [
        "(",
        "a",
        '"b c"',
        "3.14",
        "(",
        "d",
        '"\\"e\\\\\\"f"',
        ")",
        "(",
        "g",
        ")",
        ")",
    ]:
        assert stream.readNext() == expected
