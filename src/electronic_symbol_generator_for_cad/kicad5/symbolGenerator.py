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
from .kutils import *

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

    def __init__(self, p: PackageDescription, m: Dict[str, int] = metrics):
        self.p = p
        self.metrics = m

    def organisePins(self, g) -> RectangularHolderOfRailsOfPins:
        main = RectangularHolderOfRailsOfPins()
        slots = g.slots
        if g.pattern == PatternOfGroup.BUS:
            if g.directionnality == Directionnality.IN:
                main.west.push(slots["bus"])
            else:
                main.east.push(slots["bus"])
        elif g.pattern == PatternOfGroup.AMPOP_IO:
            ins = slots["in"]
            main.west.push([ins[0], None, ins[1]])
            main.east.push([None] + slots["out"] + [None])
        elif g.pattern == PatternOfGroup.AMPOP_VREF:
            ins = slots["in"]
            main.north.pushSinglePin(ins[0])
            main.south.pushSinglePin(ins[1])
        elif g.pattern == PatternOfGroup.POWER:
            pass
        else:
            # -- compute building metrics
            hasTwoGroupsAtWest = 0 if "in" not in slots or "others" not in slots else 1
            expectedLengthWest = (
                (0 if "in" not in slots else len(slots["in"]))
                + (0 if "others" not in slots else len(slots["others"]))
                + hasTwoGroupsAtWest
            )
            hasTwoGroupsAtEast = 0 if "out" not in slots or "bi" not in slots else 1
            expectedLengthEast = (
                (0 if "out" not in slots else len(slots["out"]))
                + (0 if "bi" not in slots else len(slots["bi"]))
                + (0 if "out" not in slots or "bi" not in slots else 1)
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
            if "in" in slots:
                main.west.push(slots["in"])
            if hasTwoGroupsAtWest == 1:
                main.west.pushSinglePin(None)
            if fillerSizeWest > 0:
                main.west.push([None for p in range(fillerSizeWest)])
            if "others" in slots:
                main.west.push(slots["others"])
            # -- build east rail
            if "out" in slots:
                main.east.push(slots["out"])
            if hasTwoGroupsAtEast == 1:
                main.east.pushSinglePin(None)
            if fillerSizeEast > 0:
                main.east.push([None for p in range(fillerSizeEast)])
            if "out" in slots:
                main.east.push(slots["out"])
        # -- Begin surface
        return main

    def renderGroup(
        self, g: GroupOfPins, spacing: int, currentUnit: int, result: List[str]
    ):
        # prolog
        result.extend(toSubtitle(f"{g.designator} -- {g.comment}"))
        # specific text
        # pins
        # -- prepare rails
        main = self.organisePins(g)
        result.extend(
            toSurface(
                0,
                0,
                spacing * main.width,
                -spacing * main.height,
                currentUnit,
            )
        )
        result.extend(
            toStackOfPins(
                0,
                spacing * main.paddingNorth,
                SideOfComponent.WEST,
                spacing,
                [None] + main.west.items,
                currentUnit,
            ),
        )
        result.extend(
            toStackOfPins(
                spacing * main.width,
                spacing * main.paddingNorth,
                SideOfComponent.EAST,
                spacing,
                [None] + main.east.items,
                currentUnit,
            ),
        )
        # epilog

    @property
    def symbol(self) -> List[str]:
        result = []
        # --- prepare ---
        ungroupedOthers = [
            pin
            for pin in self.p.ungroupedPins
            if pin.type not in typesOfPowerDistributionPins
        ]
        ungroupedPower = [
            pin
            for pin in self.p.ungroupedPins
            if pin.type in typesOfPowerDistributionPins
        ]
        numberOfUnits = (
            len(self.p.groupedPins)
            + (1 if len(ungroupedOthers) > 0 else 0)
            + (1 if len(ungroupedPower) > 0 else 0)
        )

        # --- generate statements ---
        spacing = metrics["spacing"]
        # prolog
        result.extend(toTitle(f"{self.p.name} -- Multiple units symbol"))
        # main text
        result.extend(toBeginSymbol((self.p.name + "_mu").upper(), numberOfUnits))
        if len(self.p.aliases) > 0:
            result.extend(toAliases(self.p.aliases))
        result += toFieldVisible(0, self.p.prefix, 0, 300, StyleOfField.NORMAL)
        result += toFieldVisible(1, self.p.name, 0, 200, StyleOfField.BOLD)
        if self.p.footprintDesignator != None:
            result += toFieldInvisible(
                2, self.p.footprintDesignator, 0, 400, StyleOfField.NORMAL
            )
        if self.p.datasheet != None:
            result += toFieldInvisible(3, self.p.datasheet, 0, 500, StyleOfField.NORMAL)
        result.extend(toBeginDraw())

        currentUnit = 1
        for g in self.p.groupedPins:
            self.renderGroup(g, spacing, currentUnit, result)
            currentUnit += 1
        # ungrouped pins : others (no pwr, opwr or gnd)
        if len(ungroupedOthers) > 0:
            self.renderGroup(
                GroupOfPins("OTHERS", 9999, "Other pins", ungroupedOthers),
                spacing,
                currentUnit,
                result,
            )
            currentUnit += 1
        # ungrouped pins : power distribution (pwr, opwr and gnd)
        if len(ungroupedPower) > 0:
            self.renderGroup(
                GroupOfPins("POWER", 9999, "Power distribution", ungroupedPower),
                spacing,
                currentUnit,
                result,
            )
            currentUnit += 1
        # epilog
        result.extend(toEndDraw())
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
