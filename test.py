import math
import random

def generate_random_island(rows=20, cols=42):
    center_y, center_x = (rows - 1) / 2, (cols - 1) / 2
    
    # Create a list of radii for 360 degrees to define the "shoreline"
    # We start with a base size and let it 'drift' randomly
    num_points = 360
    angles = []
    current_r = 0.35 # Base radius
    
    for i in range(num_points):
        # Small random adjustments create smooth but unpredictable bumps
        current_r += random.uniform(-0.03, 0.03)
        # Keep the radius within a reasonable 'island' range
        current_r = max(0.2, min(0.45, current_r))
        angles.append(current_r)

    for y in range(rows):
        row_str = ""
        for x in range(cols):
            dy, dx = (y - center_y), (x - center_x)
            
            # Find which angle (0-359) this coordinate points toward
            angle_rad = math.atan2(dy, dx)
            angle_deg = int(math.degrees(angle_rad)) % 360
            
            # Get the random radius we generated for that specific direction
            dynamic_radius = angles[angle_deg]
            
            # Normalize distance based on aspect ratio and our random radius
            dist_y = dy / (rows * dynamic_radius)
            dist_x = dx / (cols * dynamic_radius)
            
            if (dist_x**2 + dist_y**2) < 1:
                row_str += "."
            else:
                row_str += "W"
        print(row_str)

generate_random_island()