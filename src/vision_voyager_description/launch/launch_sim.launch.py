import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    pkg_name = 'vision_voyager_description'
    
    xacro_file = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'vision_voyager.urdf.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    pkg_description = get_package_share_directory('vision_voyager_description')
    world_file = os.path.join(pkg_description, 'worlds', 'world_with_objects.world')


    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True
        }]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': [f'-r ', world_file]}.items(),
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description', 
            '-name', 'vision_voyager', 
            '-x', '0.0',  
            '-y', '0.0',   
            '-z', '0.1'  
        ],
        output='screen'
    )


    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
        '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
        '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
        '/ultrasonic/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
        '/line_follower/left@sensor_msgs/msg/Image[gz.msgs.Image',
        '/line_follower/center@sensor_msgs/msg/Image[gz.msgs.Image',
        '/line_follower/right@sensor_msgs/msg/Image[gz.msgs.Image',
        '/model/vision_voyager/joint/pan_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
        '/model/vision_voyager/joint/tilt_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
        '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
    ],
    output='screen'
    )


    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
        bridge
    ])