import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # Numele pachetului
    package_name='vision_voyager_description'

    # Procesăm fișierul XACRO pentru a obține URDF
    pkg_path = os.path.join(get_package_share_directory(package_name))
    xacro_file = os.path.join(pkg_path,'urdf','vision_voyager.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    # Node: Robot State Publisher (publică structura robotului)
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': True}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Gazebo (pornire server și client)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # Node: Spawn Entity (pune robotul în Gazebo)
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'vision_voyager'],
                        output='screen')

    # Lansăm totul
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
    ])
