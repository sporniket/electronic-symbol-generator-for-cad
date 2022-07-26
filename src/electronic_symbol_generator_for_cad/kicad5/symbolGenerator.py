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
from typing import List, Dict

from electronic_package_descriptor import *
from ..symbolGenerator import (
    SymbolGenerator,
    SingleSymbolGenerator,
    writeLinesWithSeparator,
)

from .comments import *
from .pins import *
from .symbols import *

metrics = {
    "spacing": 100,  # space between 2 pins
    "margin": 200,  # minimal spacing between the border and the first pin, and the spacing between pins of the other side (north-south, and west-east)
    "glyphWidth": 50,  # 90% of the glyphs MUST be have a width up to this value.
}

typesOfPowerDistributionPins = [
    TypeOfPin.POWER,
    TypeOfPin.OUTPUT_POWER,
    TypeOfPin.GROUND,
]


class SymbolGeneratorForKicad5_Functionnal_MultiUnit(SingleSymbolGenerator):
    """
    Symbol generator for functionnal, multi-unit symbols.

    Given that each unit will have a variable width, depending on the pins of the unit :
    * the top-left corner of the main rectangle will be stucked at (0,0)
    * the text fields and the text describing the unit will be tacked at x = 0 and just above the main rectangle
      (no pins on the north side of the unit, ever)
    """

    def __init__(self, p: PackageDescription, metrics: Dict[str:int] = metrics):
        self.p = p
        self.metrics = metrics

    def organisePins(self, g):
        main = RectangularHolderOfRailsOfPins()
        if g.pattern == PatternOfGroup.BUS:
            pass
        elif g.pattern == PatternOfGroup.AMPOP_IO:
            pass
        elif g.pattern == PatternOfGroup.AMPOP_VREF:
            pass
        elif g.pattern == PatternOfGroup.POWER:
            pass
        else:
            # -- compute building metrics
            hasTwoGroupsAtWest = 0 if "in" not in g or "others" not in g else 1
            expectedLengthWest = (
                (0 if "in" not in g.slots else len(g.slots["in"]))
                + (0 if "others" not in g else len(g.slots["others"]))
                + hasTwoGroupsAtWest
            )
            hasTwoGroupsAtEast = 0 if "out" not in g or "bi" not in g else 1
            expectedLengthEast = (
                (0 if "out" not in g.slots else len(g.slots["out"]))
                + (0 if "bi" not in g else len(g.slots["bi"]))
                + (0 if "out" not in g or "bi" not in g else 1)
            )
            fillerSizeWest = (
                0
                if expectedLengthWest >= expectedLengthEast
                else expectedLengthEast - expectedLengthWest
            )
            fillerSizeEast = (
                0
                if expectedLengthEast >= expectedLengthWest
                else expectedLengthWest - expectedLengthEast
            )
            # -- build west rail
            if "in" in g.slots:
                main.west.push(g.slots["in"])
            if hasTwoGroupsAtWest == 1:
                main.west.pushSinglePin(None)
            if fillerSizeWest > 0:
                main.west.push([None for p in range(fillerSizeWest)])
            if "others" in g.slots:
                main.west.push(g.slots["others"])
            # -- build east rail
            if "out" in g.slots:
                main.east.push(g.slots["out"])
            if hasTwoGroupsAtEast == 1:
                main.east.pushSinglePin(None)
            if fillerSizeEast > 0:
                main.east.push([None for p in range(fillerSizeEast)])
            if "out" in g.slots:
                main.east.push(g.slots["out"])
        # -- Begin surface
        return main

    @property
    def symbol(self) -> List[str]:
        result = []
        # --- prepare ---
        ungroupedOthers = [
            pin for pin in p.ungrouped if pin.type not in typesOfPowerDistributionPins
        ]
        ungroupedPower = [
            pin for pin in p.ungrouped if pin.type in typesOfPowerDistributionPins
        ]
        numberOfUnits = (
            len(p.groupedPins)
            + (1 if len(ungroupedOthers) > 0 else 0)
            + (1 if len(ungroupedPower) > 0 else 1)
        )

        # --- generate statements ---
        # prolog
        result.extend(toTitle(f"{self.p.name} -- Multiple units symbol"))
        # main text
        result.extend(toBeginSymbol((p.name + "_mu").upper(), numberOfUnits))

        currentUnit = 1
        for g in self.p.groupedPins:
            # prolog
            result.extend(toSubtitle(f"{g.designator} -- {g.comment}"))
            # specific text
            # pins
            # -- prepare rails
            main = self.organisePins(g)
            result.extend(toSurface(0,0,metrics["spacing"]*main.width, -metrics["spacing"]*main.height,currentUnit))
            # epilog
            # next
            currentUnit += 1
        # ungrouped pins : others (no pwr, opwr or gnd)
        # ungrouped pins : power distribution (pwr, opwr and gnd)
        # epilog
        result.extend(toEndSymbol())
        return result


class SymbolGeneratorForKicad5(SymbolGenerator):
    def __init__(self, p: PackageDescription):
        self.p = p
        self.generators = {
            "functionnal_multi_unit": SymbolGeneratorForKicad5_Functionnal_MultiUnit(p)
        }

    @property
    def symbolSet(self) -> Dict[str, List[str]]:
        return {key: self.generators[key].symbol for key in self.generators}

    def emitSymbolSet(self, out):
        # emit prolog
        writeLinesWithSeparator(out, toBeginSymbolSet(self.p.name))
        # body
        sset = self.symbolSet
        for k in sset:
            writeLinesWithSeparator(out, sset[k])
        # emit epilog
        writeLinesWithSeparator(out, toEndSymbolSet())
