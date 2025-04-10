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

import json

from electronic_symbol_generator_for_cad.s_expr import (
    SymbolicStylesheet,
)


def test_SymbolicStylesheet_should_use_default_values_when_none_provided():
    stylesheet = SymbolicStylesheet()
    assert stylesheet.line_width == 80
    assert stylesheet.left_trimmed_line_min_width == 48
    assert stylesheet.secability_threshold == 5
    assert stylesheet.indent_width == 2


def test_SymbolicStylesheet_should_use_provided_values():
    configuration = json.loads(
        """{
    "line-width":120,
    "left-trimmed-line-min-width":40,
    "secability-threshold":3,
    "indent-width":4
}"""
    )
    stylesheet = SymbolicStylesheet(configuration)
    assert stylesheet.line_width == 120
    assert stylesheet.left_trimmed_line_min_width == 40
    assert stylesheet.secability_threshold == 3
    assert stylesheet.indent_width == 4
