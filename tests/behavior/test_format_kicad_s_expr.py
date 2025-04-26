"""
---
(c) 2022 David SPORN
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

import os
import shutil
import time
import sys
import pytest
from unittest.mock import patch

from .utils import makeTmpDirOrDie, perform_test

from electronic_symbol_generator_for_cad import SymbolGeneratorCli
from electronic_symbol_generator_for_cad.s_expr import SymbolicStreamComparator

input_file = "mc_68000_plcc68.md"
input_files = [
    # "dac0802.md",
    # "dram-256Kx1.md",
    "mc_68000_plcc68.md",
    # "lf347.json",
    # "pal20r6.md",
    # "simm-30.md",
]
output_files = [
    # "dac0802.kicad_sym",
    # "dram-256Kx1.kicad_sym",
    "mc_68000_plcc68.kicad_sym",
    # "lf347.kicad_sym",
    # "pal20r6.kicad_sym",
    # "simm-30.kicad_sym",
]


def perform_test_s_expr(
    tmp_dir: str,
    source_dir: str,
    expected_dir: str,
    baseArgs: list[str],
    inputFileName: str,
    outputFileName: str,
):
    with patch.object(
        sys, "argv", baseArgs + [os.path.join(source_dir, inputFileName)]
    ):
        SymbolGeneratorCli().run()
        # Checks that json source files are skipped
        actualResultPath = os.path.join(tmp_dir, outputFileName)
        expectedResultPath = os.path.join(expected_dir, outputFileName)
        assert os.path.exists(actualResultPath)
        with open(actualResultPath, encoding="utf-8") as actual:
            with open(expectedResultPath, encoding="utf-8") as expected:
                comparator = SymbolicStreamComparator(actual, expected)
                result = comparator.areEqual(actual, expected)
                if not (result.result):
                    for i in result.context:
                        print(f"<=  {i[0]}")
                        print(f" => {i[1]}")
                        print()
                    assert result.result


def test_that_format_kicad6_works_as_expected():
    tmp_dir = makeTmpDirOrDie(time.time())
    source_dir = os.path.join(".", "tests", "data")
    expected_dir = os.path.join(".", "tests", "data.expected")
    baseArgs = ["prog", "--format", "kicad-s-expr", "--into", tmp_dir]
    for input_file, output_file in zip(input_files, output_files):
        perform_test_s_expr(
            tmp_dir, source_dir, expected_dir, baseArgs, input_file, output_file
        )
