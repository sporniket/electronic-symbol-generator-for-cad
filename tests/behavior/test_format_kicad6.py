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

from .utils import makeTmpDirOrDie

from electronic_symbol_generator_for_cad import SymbolGeneratorCli

input_file = "mc_68000_plcc68.md"


def test_that_format_kicad6_works_as_expected():
    tmp_dir = makeTmpDirOrDie(time.time())
    testargs = [
        "prog",
        "--format",
        "kicad-s-expr",
        "--into",
        tmp_dir,
        os.path.join(".", "tests", "data", input_file),
    ]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(RuntimeError):
            SymbolGeneratorCli().run()
