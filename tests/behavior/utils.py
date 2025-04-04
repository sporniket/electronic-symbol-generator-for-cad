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
import sys
import filecmp
from typing import List
from unittest.mock import patch
from electronic_symbol_generator_for_cad import SymbolGeneratorCli


def makeTmpDirOrDie(suffix: str = None) -> str:
    newdir = os.path.join(".", f"tmp.{suffix}" if suffix != None else "tmp")
    if os.path.exists(newdir):
        if os.path.isdir(newdir):
            return newdir
        raise (ResourceWarning(f"{newdir} is not a directory"))
    os.mkdir(newdir)
    return newdir


def assert_that_source_is_converted_as_expected(pathActual: str, pathExpected: str):
    assert filecmp.cmp(pathActual, pathExpected, shallow=False)


def perform_test(
    tmp_dir: str,
    source_dir: str,
    expected_dir: str,
    baseArgs: List[str],
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
        assert_that_source_is_converted_as_expected(
            actualResultPath, expectedResultPath
        )
