from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Shape:
    def contains(self, point) -> bool:
        """Determine if a point is inside this shape."""
        if not isinstance(point, Point):
            raise TypeError(f"Expected an instance of Point, got {type(point).__name__} instead.")
        raise NotImplementedError("This method should be implemented differently for different shapes.")

    def overlaps(self, other: 'Shape') -> bool:
        """Determine if this shape overlaps with another shape."""
        if not isinstance(other, Shape):
            raise TypeError(f"Expected an instance of Shape, got {type(other).__name__} instead.")
        raise NotImplementedError("This method should be implemented differently for different shapes.")
    
    def visualize(self):
        """Visualize the shape using matplotlib."""
        raise NotImplementedError("This method should be implemented differently for different shapes.")

class Rectangle(Shape):
    def __init__(self, bottom_left: Point, width: float, height: float):
        self.bottom_left = bottom_left
        self.width = width
        self.height = height
        self.top_right = Point(bottom_left.x + width, bottom_left.y + height)

    @property
    def vertices(self):
        return [self.bottom_left, self.top_right, Point(self.bottom_left.x, self.top_right.y), Point(self.top_right.x, self.bottom_left.y)]
    
    def contains(self, point: Point) -> bool:
        return (self.bottom_left.x <= point.x <= self.top_right.x) and \
                (self.bottom_left.y <= point.y <= self.top_right.y)
    
    def overlaps(self, other: Shape) -> bool:
        if isinstance(other, Rectangle):
            return not (self.top_right.x < other.bottom_left.x or 
                        self.bottom_left.x > other.top_right.x or 
                        self.top_right.y < other.bottom_left.y or 
                        self.bottom_left.y > other.top_right.y)

        elif isinstance(other, Circle):
            x_closest = max(self.bottom_left.x, min(other.center.x, self.top_right.x))
            y_closest = max(self.bottom_left.y, min(other.center.y, self.top_right.y))

            distance_squared = (other.center.x - x_closest)**2 + (other.center.y - y_closest)**2

            return distance_squared <= other.radius ** 2
    
    def visualize(self, ax):
        shape = patches.Rectangle((self.bottom_left.x, self.bottom_left.y), 
                                      self.width, self.height, linewidth=5, edgecolor='black', facecolor='red', alpha=0.5)
        ax.add_patch(shape)

        for vertex in self.vertices:
            plt.scatter(vertex.x, vertex.y, color='red', label="Point")
            plt.text(vertex.x + 0.1, vertex.y + 0.1, f"({vertex.x}, {vertex.y})", fontsize=12, color='black')

class Circle(Shape):
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def contains(self, point: Point) -> bool:
        distance_squared = (self.center.x - point.x)**2 + (self.center.y - point.y)**2
        return (distance_squared <= self.radius**2)
            
    def overlaps(self, other: Shape) -> bool:
        if isinstance(other, Rectangle):
            return other.overlaps(self)

        if isinstance(other, Circle):
            distance_squared = (self.center.x - other.center.x)**2 + (self.center.y - other.center.y)**2
            return distance_squared <= (self.radius + other.radius)**2
    
    def visualize(self, ax):
        shape = patches.Circle((self.center.x, self.center.y), self.radius, linewidth=5, edgecolor='black', facecolor='green', alpha=0.5)
        ax.add_patch(shape)
        ax.scatter(self.center.x, self.center.y, color='red', label="Point")
        ax.text(self.center.x + 0.1, self.center.y + 0.1, f"({self.center.x}, {self.center.y})", fontsize=12, color='black')

        
class Triangle(Shape):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.vertices = [(p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y)]
        self._triangle_check()

    def area(self, q1: Point, q2: Point, q3: Point) -> float:
        return abs(q1.x * (q2.y - q3.y) + q2.x * (q3.y - q1.y) + q3.x * (q1.y - q2.y)) / 2.0

    def _triangle_check(self):
        """Check if the 3 points can form a triangle; otherwise raise an exception."""
        if self.area(self.p1, self.p2, self.p3) == 0:
            raise ValueError("The given points cannot form a triangle.")
    
    def contains(self, point: Point) -> bool:
        main_area = self.area(self.p1, self.p2, self.p3)
        area1 = self.area(point, self.p2, self.p3)
        area2 = self.area(self.p1, point, self.p3)
        area3 = self.area(self.p1, self.p2, point)

        return abs(main_area - (area1 + area2 + area3)) < 1e-9  # Allowing for floating-point error

    def overlaps(self, other: Shape) -> bool:
        if isinstance(other, Triangle):
            return any(other.contains(v) for v in [self.p1, self.p2, self.p3]) or \
                   any(self.contains(v) for v in [other.p1, other.p2, other.p3])
        
        elif isinstance(other, Rectangle) or isinstance(other, Circle):
            return any(other.contains(v) for v in [self.p1, self.p2, self.p3])
    
    def visualize(self, ax):
        shape = patches.Polygon(self.vertices, closed=True, linewidth=5, edgecolor='black', facecolor='blue', alpha=0.5)
        ax.add_patch(shape)

        for vertex in self.vertices:
            ax.scatter(vertex[0], vertex[1], color='red', label="Point")
            ax.text(vertex[0] + 0.1, vertex[1] + 0.1, f"({vertex[0]}, {vertex[1]})", fontsize=12, color='black')
