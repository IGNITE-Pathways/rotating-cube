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
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
shadow_color = (50, 50, 50)
opaque_color = (200, 200, 200)

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

def project_shadow(point, light_position):
    # Shadow plane at z = -2
    t = (point.z - light_position.z) / (light_position.z - -2)
    shadow_x = light_position.x + t * (point.x - light_position.x)
    shadow_y = light_position.y + t * (point.y - light_position.y)
    return Point3D(shadow_x, shadow_y, -2)

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

# Define the faces (sides) of the cube
faces = [
    (0, 1, 2, 3),  # back face
    (4, 5, 6, 7),  # front face
    (0, 1, 5, 4),  # top face
    (2, 3, 7, 6),  # bottom face
    (0, 3, 7, 4),  # left face
    (1, 2, 6, 5)   # right face
]

# Define the axis points
axis_points = {
    'x': Point3D(2, 0, 0),
    'y': Point3D(0, 2, 0),
    'z': Point3D(0, 0, 2)
}

# Parameters for projection
fov = 256
viewer_distance = 4

# Light position
light_position = Point3D(5, -5, -10)

def draw_cube():
    projected_points = [project_point(v, width, height, fov, viewer_distance) for v in vertices]
    shadow_points = [project_point(project_shadow(v, light_position), width, height, fov, viewer_distance) for v in vertices]

    # Draw shadows
    for edge in edges:
        pygame.draw.line(screen, shadow_color, shadow_points[edge[0]], shadow_points[edge[1]], 1)

    # Draw faces
    for face in faces:
        point_list = [projected_points[i] for i in face]
        pygame.draw.polygon(screen, opaque_color if face == faces[1] else white, point_list)

    # Draw edges
    for edge in edges:
        pygame.draw.line(screen, black, projected_points[edge[0]], projected_points[edge[1]], 1)

def draw_axes():
    origin = Point3D(0, 0, 0)
    projected_origin = project_point(origin, width, height, fov, viewer_distance)
    
    projected_x = project_point(axis_points['x'], width, height, fov, viewer_distance)
    projected_y = project_point(axis_points['y'], width, height, fov, viewer_distance)
    projected_z = project_point(axis_points['z'], width, height, fov, viewer_distance)
    
    pygame.draw.line(screen, red, projected_origin, projected_x, 2)
    pygame.draw.line(screen, green, projected_origin, projected_y, 2)
    pygame.draw.line(screen, blue, projected_origin, projected_z, 2)
    
    font = pygame.font.Font(None, 36)
    screen.blit(font.render('X', True, red), (projected_x[0], projected_x[1]))
    screen.blit(font.render('Y', True, green), (projected_y[0], projected_y[1]))
    screen.blit(font.render('Z', True, blue), (projected_z[0], projected_z[1]))

def rotate_point(point, angle_x, angle_y, angle_z):
    # Rotate around the X-axis
    cos_angle = math.cos(angle_x)
    sin_angle = math.sin(angle_x)
    y = point.y * cos_angle - point.z * sin_angle
    z = point.y * sin_angle + point.z * cos_angle
    point.y, point.z = y, z
    
    # Rotate around the Y-axis
    cos_angle = math.cos(angle_y)
    sin_angle = math.sin(angle_y)
    x = point.x * cos_angle + point.z * sin_angle
    z = -point.x * sin_angle + point.z * cos_angle
    point.x, point.z = x, z
    
    # Rotate around the Z-axis
    cos_angle = math.cos(angle_z)
    sin_angle = math.sin(angle_z)
    x = point.x * cos_angle - point.y * sin_angle
    y = point.x * sin_angle + point.y * cos_angle
    point.x, point.y = x, y

# Main game loop
running = True
angle_x, angle_y, angle_z = 0, 0, 0
rotation_speed = 0.001
mouse_sensitivity = 0.001
mouse_x, mouse_y = pygame.mouse.get_pos()
mouse_down = False
rotating = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
                rotating = True
                mouse_x, mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
                rotating = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle_y -= rotation_speed
    if keys[pygame.K_RIGHT]:
        angle_y += rotation_speed
    if keys[pygame.K_UP]:
        angle_x -= rotation_speed
    if keys[pygame.K_DOWN]:
        angle_x += rotation_speed
    if keys[pygame.K_q]:
        angle_z -= rotation_speed
    if keys[pygame.K_e]:
        angle_z += rotation_speed
    if keys[pygame.K_w]:
        rotation_speed += 0.001
    if keys[pygame.K_s]:
        rotation_speed -= 0.001
        rotation_speed = max(rotation_speed, 0.001)

    screen.fill(black)

    # Rotate the cube
    if rotating:
        for vertex in vertices:
            rotate_point(vertex, angle_x, angle_y, angle_z)

        for axis in axis_points.values():
            rotate_point(axis, angle_x, angle_y, angle_z)

    draw_cube()
    draw_axes()

    # Mouse rotation
    if mouse_down:
        new_mouse_x, new_mouse_y = pygame.mouse.get_pos()
        dx, dy = new_mouse_x - mouse_x, new_mouse_y - mouse_y
        angle_x += dy * mouse_sensitivity
        angle_y += dx * mouse_sensitivity
        mouse_x, mouse_y = new_mouse_x, new_mouse_y

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
