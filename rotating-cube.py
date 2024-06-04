import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Space with Pygame")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the clock
clock = pygame.time.Clock()

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def project_point(point, width, height, fov, viewer_distance):
    factor = fov / (viewer_distance + point.z)
    x = point.x * factor + width / 2
    y = -point.y * factor + height / 2
    return int(x), int(y)

# Define the cube's vertices
vertices = [
    Point3D(-1, 1, -1),
    Point3D(1, 1, -1),
    Point3D(1, -1, -1),
    Point3D(-1, -1, -1),
    Point3D(-1, 1, 1),
    Point3D(1, 1, 1),
    Point3D(1, -1, 1),
    Point3D(-1, -1, 1)
]

# Define the edges connecting the vertices
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # back face
    (4, 5), (5, 6), (6, 7), (7, 4),  # front face
    (0, 4), (1, 5), (2, 6), (3, 7)   # connecting edges
]

# Parameters for projection
fov = 256
viewer_distance = 4

def draw_cube():
    projected_points = [project_point(v, width, height, fov, viewer_distance) for v in vertices]

    for edge in edges:
        pygame.draw.line(screen, white, projected_points[edge[0]], projected_points[edge[1]], 1)

# Main game loop
running = True
angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    # Rotate the cube
    angle += 0.01
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    for vertex in vertices:
        x = vertex.x * cos_angle - vertex.z * sin_angle
        z = vertex.x * sin_angle + vertex.z * cos_angle
        vertex.x, vertex.z = x, z

    draw_cube()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
