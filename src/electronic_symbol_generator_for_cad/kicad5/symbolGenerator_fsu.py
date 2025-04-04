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

from electronic_package_descriptor import PackageDescription
from ..symbolGenerator import (
    SymbolGenerator,
    SingleSymbolGenerator,
    writeLinesWithSeparator,
)
from ..engine import RectangularHolderOfRailsOfPins, LayoutManagerForSingleUnit

from .comments import toTitle
from .pins import PinDescription, SideOfComponent, toStackOfPins
from .symbols import (
    StyleOfField,
    toAliases,
    toBeginDraw,
    toBeginSymbol,
    toContour,
    toEndDraw,
    toEndSymbol,
    toFieldInvisible,
    toFieldVisible,
    toSurface,
)
from .metrics import metrics


class SymbolGeneratorForKicad5_Functionnal(SingleSymbolGenerator):
    """
    Symbol generator for functionnal layout, single-unit symbols.

    The symbol main rectangle will be centered around origin. The text will be rendered above the
    top-right corner.
    """

    def __init__(self, p: PackageDescription, m: Dict[str, int] = metrics):
        self.p = p
        self.metrics = m

    def renderStackOfPins(
        self,
        x: int,
        y: int,
        sideOfComponent: SideOfComponent,
        offset: int,
        pins: List[PinDescription],
    ) -> List[str]:
        return toStackOfPins(x, y, sideOfComponent, offset, pins)

    def renderOutlines(
        self,
        x: int,
        y: int,
        widthFull: int,
        widthWest: int,
        widthEast: int,
        offset: int,
        outlinesThrough: List[int],
        outlinesWest: List[int],
        outlinesEast: List[int],
    ) -> List[str]:
        result = []
        halfOffset = int(offset / 2)
        if len(outlinesThrough) > 1:
            x2 = x + widthFull * offset
            for i in range(len(outlinesThrough) - 1):
                y1 = y - outlinesThrough[i] * offset - offset
                y2 = y - outlinesThrough[i + 1] * offset - offset
                result += toContour(x, y1, x2, y2)
        if len(outlinesWest) > 1:
            x2 = x + widthWest * offset
            for i in range(len(outlinesWest) - 1):
                y1 = y - outlinesWest[i] * offset - offset
                y2 = y - outlinesWest[i + 1] * offset - offset
                result += toContour(x, y1, x2, y2)
        if len(outlinesEast) > 1:
            x2 = x + widthFull * offset
            x1 = x2 - widthEast * offset
            for i in range(len(outlinesEast) - 1):
                y1 = y - outlinesEast[i] * offset - offset
                y2 = y - outlinesEast[i + 1] * offset - offset
                result += toContour(x1, y1, x2, y2)
        return result

    def render(
        self,
        main: RectangularHolderOfRailsOfPins,
        outlinesThrough: List[int],
        outlinesWest: List[int],
        outlinesEast: List[int],
        x: int,
        y: int,
        spacing: int,
        result: List[str],
    ):
        # -- prepare
        mainWidth = main.width * spacing
        mainHeight = main.height * spacing

        # prolog
        # pins
        # -- prepare rails
        result.extend(toSurface(x, y, x + mainWidth, y - mainHeight))
        result.extend(
            self.renderOutlines(
                x,
                y - main.paddingNorth * spacing,
                main.width,
                main.paddingWest,
                main.paddingEast,
                spacing,
                outlinesThrough,
                outlinesWest,
                outlinesEast,
            )
        )
        result.extend(
            self.renderStackOfPins(
                x,
                y - spacing * main.paddingNorth,
                SideOfComponent.WEST,
                spacing,
                [None] + main.west.items,
            )
        )
        result.extend(
            self.renderStackOfPins(
                x + spacing * main.paddingWest,
                y,
                SideOfComponent.NORTH,
                spacing,
                [None] + main.north.items,
            )
        )
        result.extend(
            self.renderStackOfPins(
                x + mainWidth,
                y - spacing * main.paddingNorth,
                SideOfComponent.EAST,
                spacing,
                [None] + main.east.items,
            )
        )
        result.extend(
            self.renderStackOfPins(
                x + spacing * main.paddingWest,
                y - mainHeight,
                SideOfComponent.SOUTH,
                spacing,
                [None] + main.south.items,
            )
        )
        # epilog

    @property
    def symbol(self) -> List[str]:
        result = []
        # --- prepare ---
        suffix = self.suffix
        lm = LayoutManagerForSingleUnit(self.p)
        main = lm.apply()
        outlinesThrough = lm.outlineThrough
        outlinesWest = lm.outlineWest
        outlinesEast = lm.outlineEast

        spacing = metrics["spacing"]
        mainWidth = main.width * spacing
        mainHeight = main.height * spacing
        xLeft = -int(mainWidth / 2)
        yTop = int(mainHeight / 2)
        xRight = xLeft + mainWidth - 1
        yBottom = yTop - mainHeight + 1
        xText = (
            xLeft
            if main.north.length == 0
            else xLeft + spacing * (main.paddingWest + main.north.length + 1)
        )

        # --- generate statements ---
        # prolog
        result.extend(toTitle(self.title))
        # main text
        result.extend(toBeginSymbol((self.p.name + suffix).upper()))
        if len(self.p.aliases) > 0:
            result.extend(toAliases([a + suffix for a in self.p.aliases]))
        result += toFieldVisible(
            0, self.p.prefix, xText, yTop + 200, StyleOfField.NORMAL
        )
        result += toFieldVisible(1, self.p.name, xText, yTop + 100, StyleOfField.BOLD)
        if self.p.footprintDesignator != None:
            result += toFieldInvisible(
                2, self.p.footprintDesignator, xText, yTop + 300, StyleOfField.NORMAL
            )
        if self.p.datasheet != None:
            result += toFieldInvisible(
                3, self.p.datasheet, xText, yTop + 400, StyleOfField.NORMAL
            )
        result.extend(toBeginDraw())

        self.render(
            main,
            outlinesThrough,
            outlinesWest,
            outlinesEast,
            xLeft,
            yTop,
            spacing,
            result,
        )

        # epilog
        result.extend(toEndDraw())
        result.extend(toEndSymbol())
        return result
