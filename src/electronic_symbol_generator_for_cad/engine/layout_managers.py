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

typesOfPowerDistributionPins = (
    TypeOfPin.POWER,
    TypeOfPin.OUTPUT_POWER,
    TypeOfPin.GROUND,
)


class LayoutManager:
    """
    Interface to implement.

    Subclass this class, define a constructor with any appliable parameters, then use apply to regenerate a the model of the symbol pins.
    """

    def apply(self) -> RectangularHolderOfRailsOfPins:
        return RailOfPins()

class LayoutManagerForSingleUnit(LayoutManager):
    def __init__(self, p: PackageDescription):
        self.p = p
    
   
    def apply(self) -> RectangularHolderOfRailsOfPins:
        result = RectangularHolderOfRailsOfPins()

        # algorithm
        # 2 slots for north : ungrouped power in and power out
        # 2 slots for south : ungrouped ground and dnc
        # 1 slots for ungrouped others : either first bi (rank 0) or last monodirectionnal (rank 99999)

        # retrieve grouped pins, append group of ungrouped others if any.
        # 4 lists to sort : BI, IN, OUT, BI_BUS (bi buses are out of bi/in/out)
        # for each BI : append to result, fill to length, store last position for separator
        # for each IN : append to west, store last position for separator
        # for each OUT : append to east, store last position for separator
        # sort bus by decreasing size
        # for each BI_BUS : append to shortest side, store last position for separator
        
        # render the 4 sides
        # render the bloc separators
        # the end

        return result

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
            expectedLengthWest = 0 if "in" not in slots else len(slots["in"])

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
            if fillerSizeWest > 0:
                main.west.push([None for p in range(fillerSizeWest)])
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
            others = slots["others"]
            # -- pins that are not power/ground
            needSpacerAtEast = True if main.east.length > 0 else False
            for pin in others:
                if pin.type not in typesOfPowerDistributionPins:
                    if needSpacerAtEast:
                        main.east.push([None, pin])
                        needSpacerAtEast = False
                    else:
                        main.east.pushSinglePin(pin)

            # -- pins that are power/ground
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
                elif pin.type == TypeOfPin.OUTPUT_POWER:
                    if needSpacerAtEast:
                        main.east.push([None, pin])
                        needSpacerAtEast = False
                    else:
                        main.east.pushSinglePin(pin)
        # -- Begin surface
        return main


class LayoutManagerForPhysicalSingleUnit(LayoutManager):
    def __init__(self, p: PackageDescription):
        self.p = p

    @property
    def pins(self) -> List[PinDescription]:
        """Gathers all the pins from the package into a list"""
        allThePins = []
        allThePins += self.p.ungroupedPins
        for g in self.p.groupedPins:
            allThePins += g.pins
        return sorted(allThePins, key=lambda p: p.designator.fullname)

    def apply(self) -> RectangularHolderOfRailsOfPins:
        layout = self.p.layoutOfPins.value
        return getattr(self, f"apply_{layout}")()

    def apply_BRD(self):
        sortedPins = self.pins
        halfLength = int(len(sortedPins) / 2)

        result = RectangularHolderOfRailsOfPins()
        result.west.push(sortedPins[:halfLength])
        result.east.push(sortedPins[halfLength:])

        return result

    def apply_DIM(self):
        sortedPins = self.pins

        result = RectangularHolderOfRailsOfPins()
        result.west.push(sortedPins[0::2])
        result.east.push(sortedPins[1::2])

        return result

    def apply_DIP(self):
        sortedPins = self.pins
        halfLength = int(len(sortedPins) / 2)

        result = RectangularHolderOfRailsOfPins()
        result.west.push(sortedPins[:halfLength])
        result.east.push(list(reversed(sortedPins[halfLength:])))

        return result

    def apply_LCC(self):
        sortedPins = self.pins
        sideLength = int(len(sortedPins) / 4)
        deltaLeft = int(sideLength / 2) + 1

        result = RectangularHolderOfRailsOfPins()
        result.west.push(sortedPins[deltaLeft : deltaLeft + sideLength])
        result.south.push(
            sortedPins[deltaLeft + sideLength : deltaLeft + 2 * sideLength]
        )
        result.east.push(
            list(
                reversed(
                    sortedPins[deltaLeft + 2 * sideLength : deltaLeft + 3 * sideLength]
                )
            )
        )
        result.north.push(
            list(
                reversed(
                    sortedPins[deltaLeft + 3 * sideLength : len(sortedPins)]
                    + sortedPins[0:deltaLeft]
                )
            )
        )

        return result

    def apply_QFP(self):
        sortedPins = self.pins
        sideLength = int(len(sortedPins) / 4)

        result = RectangularHolderOfRailsOfPins()
        result.west.push(sortedPins[0:sideLength])
        result.south.push(sortedPins[sideLength : 2 * sideLength])
        result.east.push(list(reversed(sortedPins[2 * sideLength : 3 * sideLength])))
        result.north.push(list(reversed(sortedPins[3 * sideLength : len(sortedPins)])))

        return result

    def apply_SIM(self):
        sortedPins = self.pins

        result = RectangularHolderOfRailsOfPins()
        result.west.push(sortedPins)

        return result
