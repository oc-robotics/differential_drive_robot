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
Step 5: Driving the Robot (open a new tab of current terminal and run the following command line)
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Step 6: Opening the obstacle world
```
gz sim /ocr/dev_ws/src/differential_drive_robot/worlds/obstacle_world.sdf
```

    If unable to find or download the file, run this command:
    ```
    export GZ_SIM_RESOURCE_PATH=/ocr/dev_ws/src/differential_drive_robot/worlds
    ```

