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

from electronic_symbol_generator_for_cad.kicad_s_expr.s_expr import SymbolicAttribute


def test_that_toString_outputs_numbers_without_quotes():
    assert SymbolicAttribute(0).toString() == "0"
    assert SymbolicAttribute(0.10).toString() == "0.1"
    assert SymbolicAttribute(-10).toString() == "-10"
    assert SymbolicAttribute(".").toString() == '"."'
    assert SymbolicAttribute("+3.14").toString() == "+3.14"


def test_that_toString_outputs_boolean_as_yes_or_no_without_quotes():
    assert SymbolicAttribute(True).toString() == "yes"
    assert SymbolicAttribute(False).toString() == "no"


def test_that_toString_outputs_None_as_quoted_empty_string():
    assert SymbolicAttribute(None).toString() == '""'


def test_that_toString_outputs_strings_as_quoted_sanitized_strings():
    assert SymbolicAttribute("Whatever").toString() == '"Whatever"'
    assert SymbolicAttribute("What\\never").toString() == '"What\\\\never"'
    assert (
        SymbolicAttribute('Simon says "nevermind me"').toString()
        == '"Simon says \\"nevermind me\\""'
    )
