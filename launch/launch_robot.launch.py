import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

from launch_ros.actions import Node

def generate_launch_description():
    package_name='differential_drive_robot'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros_control': 'true'}.items()
    )

    default_world = os.path.join(
        get_package_share_directory(package_name),
        'worlds',
        'obstacle_world.sdf'
    )

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
    )

    # # Include the Gazebo launch file, provided by the ros_gz_sim package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
    #                 launch_arguments={'gz_args': ['-r -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    #         )

    # # Run the spawner node from the ros_gz_sim package
    # spawn_entity = Node(package='ros_gz_sim', executable='create',
    #                     arguments=['-topic', 'robot_description',
    #                                '-name', 'my_bot',
    #                                '-z', '0.1'],
    #                     output='screen')

    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_params = os.path.join(
        get_package_share_directory('differential_drive_robot'), # <-- Replace with your package name
        'config',
        'my_controllers.yaml'
        )
    
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        # arguments=["diff_cont"],
        parameters=[{'robot_description': robot_description},
                controller_params],
    )
    
    delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=controller_manager,
                on_start=[joint_broad_spawner],
            )
        )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=controller_manager,
                on_start=[diff_drive_spawner],
            )
        )


    # # Bridge for cmd_vel and other topics
    # bridge_params = os.path.join(get_package_share_directory(package_name), 'config', 'gz_bridge.yaml')
    # ros_gz_bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=[
    #         '--ros-args',
    #         '-p',
    #         f'config_file:={bridge_params}',
    #     ]
    # )

    # ros_gz_image_bridge = Node(
    #     package="ros_gz_image",
    #     executable="image_bridge",
    #     arguments=["/camera/image_raw"]
    # )

    # Launch them all!
    return LaunchDescription([
        rsp,
        world_arg,
        # gazebo,
        # spawn_entity,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        # ros_gz_bridge,
        # ros_gz_image_bridge
    ])