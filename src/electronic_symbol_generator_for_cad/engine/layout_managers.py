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
from typing import List, Dict, Union
from electronic_package_descriptor import *

from .models import RectangularHolderOfRailsOfPins


class LayoutManager:
    """
    Interface to implement.

    Subclass this class, define a constructor with any appliable parameters, then use apply to regenerate a the model of the symbol pins.
    """

    def apply(self) -> RectangularHolderOfRailsOfPins:
        return RailOfPins()


class LayoutManagerForSingleGroup(LayoutManager):
    def __init__(self, g: GroupOfPins):
        self.g = g

    def apply(self) -> RectangularHolderOfRailsOfPins:
        main = RectangularHolderOfRailsOfPins()
        slots = self.g.slots
        if self.g.pattern == PatternOfGroup.BUS:
            if self.g.directionnality == Directionnality.IN:
                main.west.push(slots["bus"])
            else:
                main.east.push(slots["bus"])
        elif self.g.pattern == PatternOfGroup.AMPOP_IO:
            ins = slots["in"]
            main.west.push([ins[0], None, ins[1]])
            main.east.push([None] + slots["out"] + [None])
        elif self.g.pattern == PatternOfGroup.AMPOP_VREF:
            ins = slots["in"]
            main.north.pushSinglePin(ins[0])
            main.south.pushSinglePin(ins[1])
        elif self.g.pattern == PatternOfGroup.POWER:
            main.west.push(slots["in"])
            main.south.push(slots["out"])
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
            if "bi" in slots:
                main.east.push(slots["bi"])
        # manage others
        if "others" in slots:
            needSpacerAtWest = True if main.west.length > 0 else False
            needSpacerAtEast = True if main.east.length > 0 else False
            for pin in slots["others"]:
                if pin.type == TypeOfPin.POWER:
                    if needSpacerAtWest:
                        main.west.push([None, pin])
                        needSpacerAtWest = False
                    else:
                        main.west.pushSinglePin(pin)
                elif pin.type == TypeOfPin.GROUND:
                    main.south.pushSinglePin(pin)
                else:
                    if needSpacerAtEast:
                        main.east.push([None, pin])
                        needSpacerAtEast = False
                    else:
                        main.east.pushSinglePin(pin)
        # -- Begin surface
        return main
