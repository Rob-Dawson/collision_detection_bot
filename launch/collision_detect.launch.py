import os
import os.path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, LogInfo

def generate_launch_description():

#region Path to Files
    try:
        PKG_PATH = FindPackageShare("collision_detection_bot").find("collision_detection_bot")
    except FileNotFoundError:
        LogInfo("Cannot find package")

    ##  Path to XACRO
    try:
        XACRO_PATH = os.path.join(PKG_PATH, "robot.urdf.xacro")
    except FileNotFoundError:
        LogInfo("Cannot find robot file")

    ## Path to Gazebo Classic
    GAZEBO_PATH = FindPackageShare("gazebo_ros").find("gazebo_ros")

    ## Path to Gazebo World
    try:
        GAZEBO_WORLD = os.path.join(PKG_PATH, "worlds", "empty.world")
    except:
        print("Cannot find world")

#endregion 

#region Include Launch Descriptions

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            PKG_PATH, "launch", "rsp.launch.py"
        )]),
        launch_arguments={'use_sim_time':'true'}.items()
    )


    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            GAZEBO_PATH, "launch", "gazebo.launch.py" 
        )]),
        launch_arguments={
            'verbose':"false",
            'world': GAZEBO_WORLD}.items()
    )
#endregion

#region Nodes

    spawn_entity = Node(
        package="gazebo_ros",
        executable='spawn_entity.py',
        arguments=['-topic', "robot_description", "-entity", "collision_detection_bot"],
        output="screen"
    )
#endregion


#region Add Launch Descriptions
    ld = LaunchDescription()
    ld.add_action(rsp)
    ld.add_action(gazebo)
    ld.add_action(spawn_entity)
#endregion

    return ld