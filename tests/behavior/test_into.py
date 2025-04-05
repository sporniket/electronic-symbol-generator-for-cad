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
from unittest.mock import patch

from .utils import makeTmpDirOrDie

from electronic_symbol_generator_for_cad import SymbolGeneratorCli

input_file = "mc_68000_plcc68.md"
output_file = "mc_68000_plcc68.json"


def test_that_into_is_taken_into_account():
    tmp_dir = makeTmpDirOrDie(time.time())
    testargs = [
        "prog",
        "--format",
        "json",
        "--into",
        tmp_dir,
        os.path.join(".", "tests", "data", input_file),
    ]
    with patch.object(sys, "argv", testargs):
        SymbolGeneratorCli().run()
        assert os.path.exists(os.path.join(tmp_dir, output_file))
    shutil.rmtree(tmp_dir)


def test_that_output_is_beside_source_when_into_is_not_specified():
    tmp_dir = makeTmpDirOrDie(time.time())
    tmp_src = os.path.join(".", tmp_dir, input_file)
    shutil.copy(os.path.join(".", "tests", "data", input_file), tmp_src)
    testargs = ["prog", "--format", "json", tmp_src]
    with patch.object(sys, "argv", testargs):
        SymbolGeneratorCli().run()
        assert os.path.exists(os.path.join(tmp_dir, output_file))
