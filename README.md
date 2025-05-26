# 🧭 Vehicle Steering Simulation using Heuristic Control and Kinematic Bicycle Model

This project simulates a vehicle following a sine-wave trajectory using a simplified **kinematic bicycle model** and a **heuristic steering controller**, mimicking basic MPC behavior. The simulated path is visualized in **Matplotlib**, and the path data is exported for animation in **Blender** using a car CAD model.

---

## 📌 Project Highlights

- 🚗 Simulates vehicle motion using a kinematic bicycle model
- 🧠 Heuristic steering control with smoothed inputs
- 📉 Adds noisy GPS measurements to simulate real-world sensor inaccuracies
- 📦 Exports path data to `.csv` for animation in Blender
- 📽️ Creates animated plots in Python to visualize path tracking
- 🛠️ Ideal for understanding control fundamentals in autonomous driving

---

## 📂 Files

| File                      | Description                                     |
|---------------------------|-------------------------------------------------|
| `steering_simulation.py`  | Main script for simulating and visualizing path |
| `true_path.csv`           | Ground truth sine wave trajectory               |
| `noisy_measurements.csv`  | Simulated noisy GPS measurements                |
| `mpc_estimated_path.csv`  | Estimated vehicle trajectory using control law  |
| `car.obj`                 | CAD model of a car                              |
| `car_animation.py`        | Python script for Blender animation             |
| `animation.mkv`           | Final animation video                           |


---

## 📈 Example Output

### Simulated Path Tracking  
![path_tracking](docs/path_tracking.png)

### Steering Angle Over Time  
![steering_plot](docs/steering_angle.png)


---

## 🧪 How It Works

### 1. **True Path Generation**
Generates a smooth sine-wave trajectory over 60 seconds.

### 2. **Noisy GPS Simulation**
Adds Gaussian noise to the true path to simulate real-world GPS data.

### 3. **Kinematic Bicycle Model**
Models the vehicle's movement based on velocity, steering input, and heading:
```python
x_new = x + v * cos(theta + beta) * dt
y_new = y + v * sin(theta + beta) * dt
theta_new = theta + (v / L) * sin(beta) * dt
```

### 4. **Heuristic Control**
Calculates the steering angle required for the vehicle to reach the next target point by:

- Computing the angle between the vehicle’s current heading and the vector towards the lookahead point.
- Applying a rate-limited smoothing function to the steering angle to avoid abrupt changes.

### 5. **Visualization**
- Plots the true path, noisy GPS measurements, and the estimated vehicle path using `matplotlib`.
- Creates an animation showing the vehicle following the path over time.

---

## ▶️ Getting Started

### ✅ Prerequisites
- Python 3.7+
- NumPy
- Matplotlib
- Pandas

Install dependencies with:
```bash
pip install numpy matplotlib pandas
```
### 🚀 Running the Simulation
Run the main script:
```bash
python steering_simulation.py
```
## 🎞️ Blender Visualization (Optional)

A **separate Blender script** handles the entire visualization workflow, including:

- Importing the `mpc_estimated_path.csv` trajectory data
- Loading the car CAD model
- Animating the vehicle along the path with realistic heading (theta) rotations
- Setting up the camera and scene for optimal visualization

### Usage

1. Open the Blender script in Blender’s scripting workspace.
2. Modify the file paths at the top of the script to point to:
   - The exported CSV file (`mpc_estimated_path.csv`)
   - Your car CAD model file
3. Run the script — everything else (data import, animation, camera setup) is handled automatically.

This makes it easy to visualize your vehicle path with minimal manual setup.

### 📚 Concepts Demonstrated
- Path following using heuristic steering control

- Vehicle dynamics modeled via kinematic bicycle equations

- Handling and filtering noisy sensor data

- Exporting trajectory data for 3D animation and visualization

### 🤝 Contributing
Contributions are welcome! Suggestions include:

- Implementing advanced control algorithms such as Pure Pursuit, Stanley Controller, or full Model Predictive Control (MPC).

- Incorporating real-time sensor data input and filtering techniques (e.g., Extended Kalman Filter).

- Enhancing visualization and animation quality.

### 📜 License
- This project is licensed under the MIT License.
- Feel free to use, adapt, and distribute the code.

### 🙋‍♂️ Author
Anurakt Raj Mathur
🔗 [LinkedIn](https://www.linkedin.com/in/anuraktrajmathur)
📬 anuraktrajmathur@gmail.com
