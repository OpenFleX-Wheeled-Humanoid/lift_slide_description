#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    model_path = PathJoinSubstitution(
        [FindPackageShare('lift_slide_description'), 'urdf', 'lift_slide_module.urdf.xacro']
    )
    rviz_path = PathJoinSubstitution(
        [FindPackageShare('lift_slide_description'), 'rviz', 'display.rviz']
    )

    use_joint_state_gui_arg = DeclareLaunchArgument(
        'use_joint_state_gui',
        default_value='true',
        description='是否启动 joint_state_publisher_gui'
    )
    start_rviz_arg = DeclareLaunchArgument(
        'start_rviz',
        default_value='true',
        description='是否启动 RViz'
    )
    min_height_arg = DeclareLaunchArgument(
        'min_height',
        default_value='-0.650',
        description='升降最小位移（米）'
    )
    max_height_arg = DeclareLaunchArgument(
        'max_height',
        default_value='0.300',
        description='升降最大位移（米）'
    )

    robot_description_content = ParameterValue(
        Command(
            [
                'xacro ',
                model_path,
                ' min_height:=',
                LaunchConfiguration('min_height'),
                ' max_height:=',
                LaunchConfiguration('max_height'),
                ' ros2_control:=false',
            ]
        ),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='lift_slide_robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}],
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='lift_slide_joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_joint_state_gui')),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='lift_slide_rviz',
        output='screen',
        arguments=['-d', rviz_path],
        condition=IfCondition(LaunchConfiguration('start_rviz')),
    )

    return LaunchDescription(
        [
            use_joint_state_gui_arg,
            start_rviz_arg,
            min_height_arg,
            max_height_arg,
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
