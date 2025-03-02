## Differential Drive Robot

Step 1: Clone the repository
```
cd dev_ws/src
git clone git@github.com:oc-robotics/differential_drive_robot.git
```
Step 2: Build the package (make sure you are running the following commands within NoVNC)
```
colcon build --symlink-install
```
Step 3: Source the setup
```
source install/setup.bash
```
Step 4: Run the Gazebo simulation
```
ros2 launch differential_drive_robot launch_sim.launch.py
```
