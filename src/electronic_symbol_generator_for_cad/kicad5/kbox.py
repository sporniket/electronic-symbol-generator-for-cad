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


class KicadBox:
    """
    Model of a box for kicad schematic. 
    
    The coordinate system is different from the screen coordinate system : when the y-coordinate of a pixel goes increase, 
    its visual position is going down ; when the y-coordinate of a Kicad object increase, its visual position is going up.

    The box is modeled using the coordinates of the top-left corner, the width and the height.
    """
    def __init__(self, x: int, y:int, w:int, h:int):
        """
        Create a box in Kicad's coordonate system.

        Args:
            x (int): x coordinate of the top-left corner.
            y (int): y coordinate of the top-left corner.
            w (int): width of the rectangle.
            h (int): height of the rectangle.
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def x2(self) -> int:
        """
        X coordinate of the bottom-right corner.

        Returns:
            int: X coordinate of the bottom-right corner.
        """
        return self.x + self.w -1

    @property 
    def y2(self) -> int:
        """
        Y coordinate of the bottom-right corner.

        Returns:
            int: Y coordinate of the bottom-right corner.
        """
        return self.y - self.h + 1


class ContainerOfKicadBox(KicadBox):
    def __init__(self, x: int, y:int, w:int, h:int):
        super().__init__(x, y, w, h)
        self.slots={}
        self.layoutManager = None

    def append(self, box:KicadBox, slot:str = '__default__'):
        """
        Add the box, into a 'slot'. 

        Args:
            box (KicadBox): the box to add. The top-left corner coordinates is expressed relative to the top-left corner of the container.
            slot (str): the group of box to be added into, for the layout manager.
        """
        if slot not in slots:
            slots[slot] = [box]
        else:
            slots[slot] += box

    def updateContainer(self):
        if layoutManager != None:
            pass # reorganize 
        dx = 0 # change of x
        dy = 0 # change of y
        dx2 = 0 # change of x2
        dy2 = 0 # change of y2
        for s in slots:
            for b in slots[s]:
                if b.x < 0:
                    #here
                    pass
