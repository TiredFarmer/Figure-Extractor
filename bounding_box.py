# Box representing top left: (x0, y0) and bottom right of box (x1, y1)
class BoundingBox:

    def __init__(self, x0, y0, x1, y1, screen_size):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.CUTOFF = 50
        self.screen_size = screen_size

    def __str__(self):
        return f"Bounding Box({self.x0}, {self.y0}, {self.x1}, {self.y1})"
    
    def is_valid(self, b2) -> bool:
        """ produce true if b2 is (close enough) to current box """
        return self._is_x_valid(b2) and self._is_y_valid(b2)
    
    def _is_x_valid(self, b2) -> bool:
        """ produce true if b2.x0 or b2.x1 is within the inflated x-size of self """
        return (self.x0 - self.CUTOFF <= b2.x0 <= self.x1 + self.CUTOFF) or (self.x0 - self.CUTOFF <= b2.x1 <= self.x1 + self.CUTOFF)
    
    def _is_y_valid(self, b2, cutoff: int = 0) -> bool:
        """ produce true if b2.y0 or b2.y1 is within the inflated y-size of self """
        if cutoff == 0:
            return (self.y0 - self.CUTOFF <= b2.y0 <= self.y1 + self.CUTOFF) or (self.y0 - self.CUTOFF <= b2.y1 <= self.y1 + self.CUTOFF)
        
        return (self.y0 - cutoff <= b2.y0 <= self.y1 + cutoff) or (self.y0 - cutoff <= b2.y1 <= self.y1 + cutoff)
    
    def merge_boxes(self, b2) -> None:
        """" combine boxes with extreme coordinates of the two """
        self._merge_x0(b2.x0)
        self._merge_y0(b2.y0)
        self._merge_x1(b2.x1)
        self._merge_y1(b2.y1)
    
    def _merge_x0(self, b: float) -> None:
        """" set self.x0 to minimum of self.x0 and b """
        self.x0 = min(self.x0, b)
        if self.x0 < 0:
            self.x0 = 0
    
    def _merge_y0(self, b: float) -> None:
        """" set self.y0 to minimum of self.y0 and b """
        self.y0 = min(self.y0, b)
        if self.y0 < 0:
            self.y0 = 0

    def _merge_x1(self, b: float) -> None:
        """" set self.x1 to maximum of self.x1 and b """
        self.x1 = max(self.x1, b)
        if self.x1 > self.screen_size[0]:
            self.x1 = self.screen_size[0]

    def _merge_y1(self, b: float) -> None:
        """" set self.y1 to maximum of self.y1 and b """
        self.y1 = max(self.y1, b)
        if self.y1 > self.screen_size[1]:
            self.y1 = self.screen_size[1]
    
    def distance(self, b: float) -> float:
        """ distance formula from center of two boxes """
        center_x = (self.x0 + self.x1) / 2
        center_y = (self.y0 + self.y1) / 2
        center_x_2 = (b.x0 + b.x1) / 2
        center_y_2 = (b.y0 + b.y1) / 2

        return  ((center_x_2 - center_x) ** 2 + (center_y_2 - center_y) ** 2) ** 0.5

    def area(self) -> float:
        return (self.x1 - self.x0) * (self.y1 - self.y0)
    
    def expand(self, value: float) -> None:
        """ expand all borders by a fixed value, checking so it doesn't go off screen """
        self.x0 -= value
        if self.x0 < 0:
            self.x0 = 0
        
        self.y0 -= value
        if self.y0 < 0:
            self.y0 = 0
        
        self.x1 += value
        if self.x1 > self.screen_size[0]:
            self.x1 = self.screen_size[0]
        
        self.y1 += value
        if self.y1 > self.screen_size[1]:
            self.y1 = self.screen_size[1]
