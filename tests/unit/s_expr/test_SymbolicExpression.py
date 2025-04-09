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

from electronic_symbol_generator_for_cad.kicad_s_expr.s_expr import (
    SymbolicAttribute,
    SymbolicExpression,
)


def test_symbolCount_should_count_symbols_recursively():
    assert (
        SymbolicExpression(
            "a", ["b", "c", 0xD, SymbolicExpression("e", ["f", 3.14, True]), "i"]
        ).symbolCount
        == 9
    )


def test_hasSymbolCountUnder_should_verify_the_number_of_symbols_against_provided_threshold():
    assert (
        SymbolicExpression(
            "a", ["b", "c", 0xD, SymbolicExpression("e", ["f", 3.14, True]), "i"]
        ).hasSymbolCountUnder(4)
        == False
    )
    # various expressions of 4 symbols
    assert (
        SymbolicExpression(
            "a",
            [
                SymbolicExpression(
                    "b", [SymbolicExpression("c", [SymbolicExpression("d", [])])]
                )
            ],
        ).hasSymbolCountUnder(4)
        == False
    )
    assert (
        SymbolicExpression(
            "a", [SymbolicExpression("b", [SymbolicExpression("c", ["d"])])]
        ).hasSymbolCountUnder(4)
        == False
    )
    assert (
        SymbolicExpression(
            "a", ["b", SymbolicExpression("c", ["d"])]
        ).hasSymbolCountUnder(4)
        == False
    )
    # various expressions of 3 symbols
    assert (
        SymbolicExpression(
            "a", [SymbolicExpression("b", [SymbolicExpression("c", [])])]
        ).hasSymbolCountUnder(4)
        == True
    )
    assert (
        SymbolicExpression("a", [SymbolicExpression("b", ["c"])]).hasSymbolCountUnder(4)
        == True
    )
    assert SymbolicExpression("a", ["b", "c"]).hasSymbolCountUnder(4) == True


def test_attributes_should_return_the_list_of_attributes():
    attributes = SymbolicExpression(
        "a", ["b", "c", 0xD, SymbolicExpression("e", ["f", 3.14, True]), "i"]
    ).attributes

    for i, a in enumerate(attributes):
        assert (
            isinstance(a, SymbolicExpression)
            if i == 3
            else isinstance(a, SymbolicAttribute)
        )
    assert attributes[0].toString() == '"b"'
    assert attributes[1].toString() == '"c"'
    assert attributes[2].toString() == "13"
    assert attributes[4].toString() == '"i"'

    attributes = attributes[3].attributes
    for i, a in enumerate(attributes):
        assert isinstance(a, SymbolicAttribute)
    assert attributes[0].toString() == '"f"'
    assert attributes[1].toString() == "3.14"
    assert attributes[2].toString() == "yes"
