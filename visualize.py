from figures import Rectangle, Triangle, Circle, Point
import matplotlib.pyplot as plt
import matplotlib.patches as patches

A = Point(5,0)
B = Point(0,0)
C = Point(0,12)
D = Point(0.6,0.6)
E  = Point(12,12) 
tri = Triangle(A,B,C)
rec = Rectangle(B,10,10)
cir = Circle(E,5)

# Create a plot
fig, ax = plt.subplots()

# Create the rectangle and add it to the plot
rec.visualize(ax)

cir.visualize(ax)
tri.visualize(ax)

ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Rectangle with Vertex Coordinates in 2D Space")

# Show the plot
plt.gca().set_aspect('equal', adjustable='box')  # Keep the aspect ratio equal
plt.grid(True)
plt.show()