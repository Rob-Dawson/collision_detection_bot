import os
import xacro
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

#region Paths

    ## Global Path
    PKG_PATH = FindPackageShare("collision_detection_bot").find("collision_detection_bot")

    ##  Path to XACRO
    try:
        XACRO_PATH = os.path.join(PKG_PATH, "description", "robot.urdf.xacro")
    except FileNotFoundError:
        LogInfo("Cannot find robot file")
    robot_description = xacro.process_file(XACRO_PATH).toxml()

#endregion

#region Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
#endregion

#region Include Launch Descriptions

    declare_use_sim_time = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="false",
        description="Use Simulation (Gazebo) clock if true",
    )

#endregion

#region Nodes

    params = {
        "robot_description": robot_description,
        "use_sim_time": use_sim_time,
    }
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params],
    )

#endregion

#region Add Launch Descriptions

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time)
    ld.add_action(node_robot_state_publisher)    

#endregion

    return ld
