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

input_file_bypassed = "lf347.json"


def test_that_format_json_works_as_expected():
    tmp_dir = makeTmpDirOrDie(time.time())
    testargs = [
        "prog",
        "--format",
        "json",
        "--into",
        tmp_dir,
        os.path.join(".", "tests", "data", input_file),
        os.path.join(".", "tests", "data", input_file_bypassed),
    ]
    with patch.object(sys, "argv", testargs):
        SymbolGeneratorCli().run()
        # Checks that json source files are skipped
        assert os.path.exists(os.path.join(tmp_dir, output_file))
        assert not os.path.exists(os.path.join(tmp_dir, input_file_bypassed))
        assert (
            len(
                [
                    name
                    for name in os.listdir(tmp_dir)
                    if os.path.isfile(os.path.join(tmp_dir, name))
                ]
            )
            == 1
        )
    shutil.rmtree(tmp_dir)
