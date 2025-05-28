import csv
import bpy
import math
from mathutils import Vector, Euler

# ------------------------
# CONFIGURABLE PARAMETERS
# ------------------------
car_z_offset = 0.46           # Car height from ground
car_scale = 0.5               # Scale factor for car model
heading_smoothing = True     # Enable smoothing
smoothing_strength = 0.25    # Smoothing factor between 0 (no change) and 1 (full new theta)

# ------------------------
# CLEAN SCENE
# ------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ------------------------
# LOAD DATA
# ------------------------
def load_csv(filepath, has_theta=False):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header
        if has_theta:
            return [[float(row[0]), float(row[1]), float(row[2])] for row in reader]
        else:
            return [[float(row[0]), float(row[1])] for row in reader]

true_positions = load_csv(r'your_filepath/true_path.csv')
noisy_positions = load_csv(r'your_filepath/noisy_measurements.csv')
mpc_positions = load_csv(r'your_filepath/mpc_estimated_path.csv', has_theta=True)

# ------------------------
# IMPORT CAR MODEL
# ------------------------
bpy.ops.wm.obj_import(filepath=r'your_filepath/car.obj')
car = bpy.context.selected_objects[0]



# Center car geometry around origin and apply scale
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
car.scale = (car_scale, car_scale, car_scale)

# ------------------------
# CREATE REAR AXLE EMPTY
# ------------------------
# Start position
start_x, start_y, start_theta = mpc_positions[0]
rear_empty = bpy.data.objects.new("RearEmpty", None)
rear_empty.empty_display_type = 'PLAIN_AXES'
rear_empty.location = (start_x, start_y, car_z_offset)
rear_empty.rotation_euler = Euler((0, 0, start_theta), 'XYZ')
bpy.context.collection.objects.link(rear_empty)

# ------------------------
# PARENT CAR TO REAR EMPTY
# ------------------------
car.parent = rear_empty
car.location = Vector((0.9, 0, 0))  # Forward offset in local space (adjust based on model length)

# ------------------------
# ANIMATE REAR EMPTY
# ------------------------
last_theta = start_theta
for i, (x, y, theta) in enumerate(mpc_positions):
    if heading_smoothing:
        theta = (1 - smoothing_strength) * last_theta + smoothing_strength * theta
    last_theta = theta

    rear_empty.location = (x, y, car_z_offset)
    rear_empty.rotation_euler = Euler((0, 0, theta), 'XYZ')
    rear_empty.keyframe_insert(data_path="location", frame=i+1)
    rear_empty.keyframe_insert(data_path="rotation_euler", frame=i+1)

# ------------------------
# TRUE PATH CURVE
# ------------------------
true_curve = bpy.data.curves.new(name="TruePath", type='CURVE')
true_curve.dimensions = '3D'
polyline = true_curve.splines.new('POLY')
polyline.points.add(count=len(true_positions)-1)
for i, pos in enumerate(true_positions):
    polyline.points[i].co = (pos[0], pos[1], 0, 1)

true_obj = bpy.data.objects.new("TruePath", true_curve)
bpy.context.collection.objects.link(true_obj)
true_curve.bevel_depth = 0.1

# Green material for path
green_mat = bpy.data.materials.new(name="GreenMaterial")
green_mat.use_nodes = True
green_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0, 1, 0, 1)
true_obj.data.materials.append(green_mat)

# ------------------------
# GPS POINTS (NOISY MEASUREMENTS)
# ------------------------
red_mat = bpy.data.materials.new(name="RedMaterial")
red_mat.use_nodes = True
red_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (1, 0, 0, 1)

for pos in noisy_positions:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(pos[0], pos[1], 0))
    sphere = bpy.context.active_object
    sphere.data.materials.append(red_mat)

# ------------------------
# SUN LIGHT
# ------------------------
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object
sun.data.energy = 2

# ------------------------
# ROAD PLANE
# ------------------------
bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, 0))
road = bpy.context.object
road.scale = (2, 10, 1)
road.rotation_euler = (0, 0, math.radians(90))
road_mat = bpy.data.materials.new(name="RoadMaterial")
road_mat.diffuse_color = (0.1, 0.1, 0.1, 1)
road.data.materials.append(road_mat)

# ------------------------
# CAMERA SETUP
# ------------------------
bpy.ops.object.camera_add(location=(10, 4, 2))  # Move camera in front of the car
camera = bpy.context.object
camera.rotation_euler = (math.radians(80), 0, math.radians(90))  # Adjust rotation to face car

bpy.context.scene.camera = camera

# Track car
for constraint in camera.constraints:
    camera.constraints.remove(constraint)

track = camera.constraints.new(type='TRACK_TO')
track.target = car
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# Animate camera movement (in front of car on X-axis)
for i, (x, y) in enumerate(true_positions):
    camera.location.x = x + 10  # Move the camera to the front of the car
    camera.keyframe_insert(data_path="location", frame=i+1)

print("✅ Scene setup and animation complete.")
