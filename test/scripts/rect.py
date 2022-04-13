from dataclasses import dataclass




@dataclass
class Rect:
    """
    Holds position data and area data

    - pos [float, float]
    - area [float, float]

    Wow, amazing
    """

    x: float
    y: float
    w: float
    h: float

    cx: int = 0
    cy: int = 0


    @property
    def center(self):
        """Get's center of the object"""
        return (self.x + self.w // 2, self.y + self.h // 2)
    
    @property
    def left(self):
        """Get's left of object"""
        return self.x
    
    @property
    def right(self):
        """Get's right of object"""
        return self.x + self.w
    
    @property
    def top(self):
        """Get's top of object"""
        return self.y
    
    @property
    def bottom(self):
        """Get's bottom of object"""
        return self.y + self.h
    
    @property
    def topright(self):
        """Get top right"""
        return (self.x + self.w, self.y)
    
    @property
    def topleft(self):
        """Get top left"""
        return (self.x, self.y)
    
    @property
    def bottomright(self):
        """Get bottom right"""
        return (self.x + self.w, self.y + self.h)
    
    @property
    def bottomleft(self):
        """Get bottom left"""
        return (self.x, self.y + self.h)

    @property
    def width(self):
        """Get the width parameter"""
        return self.w
    
    @width.setter
    def width(self, other):
        """Set the width"""
        self.w = other

    @property
    def height(self):
        """Get the height parameter"""
        return self.h

    @height.setter
    def height(self, other):
        """Set the height parameter"""
        self.h = other

    @property
    def area(self):
        """Area getter"""
        return (self.w, self.h)

    @area.setter
    def area(self, a):
        """Area setter"""
        self.w = a[0]
        self.h = a[1]

    @property
    def pos(self):
        """Get the object position"""
        return self.m_pos

    @pos.setter
    def pos(self, a):
        """Set the position"""
        self.x = a[0]
        self.y = a[1]



r = Rect(0, 0, 100, 100)

print(r)
print(r.topleft, r.topright, r.bottomright, r.bottomleft)
print(r.left, r.top, r.right, r.bottom)
print(r.center, r.width, r.height)
print(r.cx)
