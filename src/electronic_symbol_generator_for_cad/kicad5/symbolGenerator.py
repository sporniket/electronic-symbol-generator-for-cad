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
from ..sygen import SymbolGenerator, SingleSymbolGenerator
from electronic_package_descriptor import *

class SymbolGeneratorForKicad5_Functionnal_MultiUnit(SingleSymbolGenerator):
    def __init__(self, p:PackageDescription):
        self.p = p
    
    @property
    def symbol(self) -> List[str]:
        return []



class SymbolGeneratorForKicad5(SymbolGenerator):

    def __init__(self, p:PackageDescription):
        self.generators = {
            'functionnal_multi_unit':SymbolGeneratorForKicad5_Functionnal_MultiUnit(p)
        }
    
    @property
    def symbolSet(self) -> Dict[str, List[str]]:
        return {key:gen.symbol() for key,gen in self.generators}

    def emitSymbolSet(self, out):
        # emit prolog
        for gen in self.generators:
            out.writelines(gen.symbol())
        # emit epilog