import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace
import xacro

def generate_launch_description():
    pkg_name = 'vision_voyager_description'
    pkg_share = get_package_share_directory(pkg_name)
    
    
    xacro_file_1 = os.path.join(pkg_share, 'urdf', 'vision_voyager_1.urdf.xacro')
    xacro_file_2 = os.path.join(pkg_share, 'urdf', 'vision_voyager_2.urdf.xacro')
    xacro_file_3 = os.path.join(pkg_share, 'urdf', 'vision_voyager_3.urdf.xacro')
    xacro_file_4 = os.path.join(pkg_share, 'urdf', 'vision_voyager_4.urdf.xacro')
    
    robot_description_raw_1 = xacro.process_file(xacro_file_1).toxml()
    robot_description_raw_2 = xacro.process_file(xacro_file_2).toxml()
    robot_description_raw_3 = xacro.process_file(xacro_file_3).toxml()
    robot_description_raw_4 = xacro.process_file(xacro_file_4).toxml()
    
    world_file = os.path.join(pkg_share, 'worlds', 'world_with_objects.world')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )

    # ROBOT 1
    robot1_nodes = GroupAction(
        actions=[
            PushRosNamespace('robot1'),
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                output='screen',
                parameters=[{
                    'robot_description': robot_description_raw_1,
                    'use_sim_time': True,
                    'frame_prefix': 'robot1/'
                }]
            ),
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-topic', 'robot_description', 
                    '-name', 'robot1',
                    '-x', '0.0', '-y', '0.0', '-z', '0.1'
                ],
                output='screen'
            ),
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                arguments=[
                    '/model/robot1/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                    '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                    '/model/robot1/ultrasonic/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                    '/model/robot1/line_follower/left@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot1/line_follower/center@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot1/line_follower/right@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot1/joint/pan_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot1/joint/tilt_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot1/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
                ],
                output='screen',
                remappings=[
                    ('/model/robot1/cmd_vel', '/robot1/cmd_vel'),
                    ('/model/robot1/ultrasonic/scan', '/robot1/ultrasonic/scan'),
                    ('/model/robot1/line_follower/left', '/robot1/line_follower/left'),
                    ('/model/robot1/line_follower/center', '/robot1/line_follower/center'),
                    ('/model/robot1/line_follower/right', '/robot1/line_follower/right'),
                    ('/model/robot1/joint/pan_joint/cmd_pos', '/robot1/joint/pan_joint/cmd_pos'),
                    ('/model/robot1/joint/tilt_joint/cmd_pos', '/robot1/joint/tilt_joint/cmd_pos'),
                    ('/model/robot1/camera/image_raw', '/robot1/camera/image_raw'),
                ]
            )
        ]
    )

    # ROBOT 2
    robot2_nodes = GroupAction(
        actions=[
            PushRosNamespace('robot2'),
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                output='screen',
                parameters=[{
                    'robot_description': robot_description_raw_2,
                    'use_sim_time': True,
                    'frame_prefix': 'robot2/'
                }]
            ),
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-topic', 'robot_description', 
                    '-name', 'robot2',
                    '-x', '-1.0', '-y', '-3.12', '-z', '0.1'
                ],
                output='screen'
            ),
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                arguments=[
                    '/model/robot2/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                    '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                    '/model/robot2/ultrasonic/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                    '/model/robot2/line_follower/left@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot2/line_follower/center@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot2/line_follower/right@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot2/joint/pan_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot2/joint/tilt_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot2/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
                ],
                output='screen',
                remappings=[
                    ('/model/robot2/cmd_vel', '/robot2/cmd_vel'),
                    ('/model/robot2/ultrasonic/scan', '/robot2/ultrasonic/scan'),
                    ('/model/robot2/line_follower/left', '/robot2/line_follower/left'),
                    ('/model/robot2/line_follower/center', '/robot2/line_follower/center'),
                    ('/model/robot2/line_follower/right', '/robot2/line_follower/right'),
                    ('/model/robot2/joint/pan_joint/cmd_pos', '/robot2/joint/pan_joint/cmd_pos'),
                    ('/model/robot2/joint/tilt_joint/cmd_pos', '/robot2/joint/tilt_joint/cmd_pos'),
                    ('/model/robot2/camera/image_raw', '/robot2/camera/image_raw'),
                ]
            )
        ]
    )

    # ROBOT 3 
    robot3_nodes = GroupAction(
        actions=[
            PushRosNamespace('robot3'),
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                output='screen',
                parameters=[{
                    'robot_description': robot_description_raw_3,
                    'use_sim_time': True,
                    'frame_prefix': 'robot3/'
                }]
            ),
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-topic', 'robot_description', 
                    '-name', 'robot3',
                    '-x', '-0.79', '-y', '0.87', '-z', '0.1',
                    '-Y', '-1.48'  # (Yaw) in rad
                ],
                output='screen'
            ),
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                arguments=[
                    '/model/robot3/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                    '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                    '/model/robot3/ultrasonic/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                    '/model/robot3/line_follower/left@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot3/line_follower/center@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot3/line_follower/right@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot3/joint/pan_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot3/joint/tilt_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot3/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
                ],
                output='screen',
                remappings=[
                    ('/model/robot3/cmd_vel', '/robot3/cmd_vel'),
                    ('/model/robot3/ultrasonic/scan', '/robot3/ultrasonic/scan'),
                    ('/model/robot3/line_follower/left', '/robot3/line_follower/left'),
                    ('/model/robot3/line_follower/center', '/robot3/line_follower/center'),
                    ('/model/robot3/line_follower/right', '/robot3/line_follower/right'),
                    ('/model/robot3/joint/pan_joint/cmd_pos', '/robot3/joint/pan_joint/cmd_pos'),
                    ('/model/robot3/joint/tilt_joint/cmd_pos', '/robot3/joint/tilt_joint/cmd_pos'),
                    ('/model/robot3/camera/image_raw', '/robot3/camera/image_raw'),
                ]
            )
        ]
    )

    # ROBOT 4
    robot4_nodes = GroupAction(
        actions=[
            PushRosNamespace('robot4'),
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                output='screen',
                parameters=[{
                    'robot_description': robot_description_raw_4,
                    'use_sim_time': True,
                    'frame_prefix': 'robot4/'
                }]
            ),
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-topic', 'robot_description', 
                    '-name', 'robot4',
                    '-x', '-1.35', '-y', '-1.29', '-z', '0.1',
                    '-Y', '-2.05'  
                ],
                output='screen'
            ),
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                arguments=[
                    '/model/robot4/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                    '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                    '/model/robot4/ultrasonic/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                    '/model/robot4/line_follower/left@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot4/line_follower/center@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot4/line_follower/right@sensor_msgs/msg/Image[gz.msgs.Image',
                    '/model/robot4/joint/pan_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot4/joint/tilt_joint/cmd_pos@std_msgs/msg/Float64]gz.msgs.Double',
                    '/model/robot4/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'
                ],
                output='screen',
                remappings=[
                    ('/model/robot4/cmd_vel', '/robot4/cmd_vel'),
                    ('/model/robot4/ultrasonic/scan', '/robot4/ultrasonic/scan'),
                    ('/model/robot4/line_follower/left', '/robot4/line_follower/left'),
                    ('/model/robot4/line_follower/center', '/robot4/line_follower/center'),
                    ('/model/robot4/line_follower/right', '/robot4/line_follower/right'),
                    ('/model/robot4/joint/pan_joint/cmd_pos', '/robot4/joint/pan_joint/cmd_pos'),
                    ('/model/robot4/joint/tilt_joint/cmd_pos', '/robot4/joint/tilt_joint/cmd_pos'),
                    ('/model/robot4/camera/image_raw', '/robot4/camera/image_raw'),
                ]
            )
        ]
    )

    return LaunchDescription([
        set_gazebo_engine,
        gazebo,
        robot1_nodes,
        TimerAction(
            period=5.0,
            actions=[robot2_nodes]
        ),
        TimerAction(
            period=10.0,
            actions=[robot3_nodes]
        ),
        TimerAction(
            period=15.0,
            actions=[robot4_nodes]
        )
    ])