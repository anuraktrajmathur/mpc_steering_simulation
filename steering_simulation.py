import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation

# Vehicle Parameters
L = 2.5  # Wheelbase of the vehicle
lookahead_distance = 1.5  # Fixed lookahead distance
max_steering_rate = 0.5  # Max rate of change of steering angle

# Generate True Path
t = np.linspace(0, 60, 600)  # Extend to 60 seconds
true_x = t
true_y = np.sin(t)

# Generate Noisy Measurements
noise_std = 0.3
measured_x = true_x + np.random.normal(0, noise_std, size=len(true_x))
measured_y = true_y + np.random.normal(0, noise_std, size=len(true_y))

# Kinematic Bicycle Model
def kinematic_model(state, delta, dt=0.1):
    x, y, v, theta = state
    beta = np.arctan(0.5 * np.tan(delta))  # Bicycle model slip angle
    x_new = x + v * np.cos(theta + beta) * dt
    y_new = y + v * np.sin(theta + beta) * dt
    theta_new = theta + (v / L) * np.sin(beta) * dt
    return np.array([x_new, y_new, v, theta_new])

# Low-pass filter for smoother steering
def smooth_steering(prev_delta, new_delta, max_rate=max_steering_rate):
    return prev_delta + np.clip(new_delta - prev_delta, -max_rate, max_rate)

# Improved Heuristic Steering Control
def heuristic_control(x, y, state, prev_delta):
    vehicle_x, vehicle_y, v, theta = state
    
    dx, dy = x - vehicle_x, y - vehicle_y
    target_angle = np.arctan2(dy, dx)
    raw_delta = np.arctan(2 * L * np.sin(target_angle - theta) / lookahead_distance)
    
    return smooth_steering(prev_delta, raw_delta)

# Simulate the MPC-like Control
state = np.array([0, 0, 1.2, 0])  # Velocity set to 1.2 m/s
estimated_states = []
steering_angles = []
prev_delta = 0  # Initialize previous steering angle

for x_ref, y_ref in zip(true_x, true_y):
    delta = heuristic_control(x_ref, y_ref, state, prev_delta)
    state = kinematic_model(state, delta)
    estimated_states.append(state)
    steering_angles.append(delta)
    prev_delta = delta  # Update previous steering angle

estimated_states = np.array(estimated_states)

# Export data to CSV
true_path_df = pd.DataFrame({'X': true_x, 'Y': true_y})
noisy_measurements_df = pd.DataFrame({'X': measured_x, 'Y': measured_y})
estimated_path_df = pd.DataFrame({'X': estimated_states[:, 0], 'Y': estimated_states[:, 1], 'Theta': estimated_states[:, 3]})
estimated_path_df.to_csv('mpc_estimated_path.csv', index=False)

true_path_df.to_csv('true_path.csv', index=False)
noisy_measurements_df.to_csv('noisy_measurements.csv', index=False)
estimated_path_df.to_csv('mpc_estimated_path.csv', index=False)

# Plot the Results with Animation
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(true_x, true_y, 'g--', label='True Path')
ax.scatter(measured_x, measured_y, color='r', s=10, label='Noisy GPS Measurements')
line, = ax.plot([], [], 'b-', label='MPC Estimated Path')
ax.legend()
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Path Estimation using MPC Control')
ax.grid()

# Animation function
def update(frame):
    line.set_data(estimated_states[:frame, 0], estimated_states[:frame, 1])
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(estimated_states), interval=50, blit=True)
plt.show()

# Plot Steering Angles
plt.figure(figsize=(10, 5))
plt.plot(t[:len(steering_angles)], steering_angles, 'b-', label='Steering Angle')
plt.xlabel('Time')
plt.ylabel('Steering Angle (rad)')
plt.title('Steering Angle over Time')
plt.legend()
plt.grid()
plt.show()
