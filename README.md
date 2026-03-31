# 49595-HW2

## Important dependency note
- `rospy` is a ROS package, not a PyPI package.
- So `uv add rospy` will fail (expected behavior).
- For these examples, install dependencies through Duckietown module files:
	- `dependencies-apt.txt`
	- `dependencies-py3.txt`
	- `dependencies-py3.dt.txt`
- Then build/run with `dts devel ...` inside each module folder.

## Perception: 
- Navigate to the `./ros-sensor-camera/` directory. This folder contains the boilerplate for subscribing to the Duckiebot's continuous video stream.

## Movement: 
- Navigate to the `./ros-actuator-wheels/` directory. This folder shows you how to publish speed commands to the left and right motors to make the robot move forward, backward, or turn.

## Quick start (Duckietown)
Follow Duckietown setup guidance here: [duckietown get-started](https://duckietown.com/get-started/)

### Camera sensor example
1. `cd ros-sensor-camera`
2. `dts devel build`
3. `dts devel run -X -R <ROBOT_NAME>`

This shows the live camera and logs simple sensor readings (image brightness and center pixel color).

### Wheels movement example
1. `cd ros-actuator-wheels`
2. `dts devel build`
3. `dts devel run -R <ROBOT_NAME>`

This runs a basic sequence: forward, stop, backward, stop.

## [SOFTWARE SET UP](https://duckietown.com/get-started/#:~:text=Software%20environment%20setup)

## Duckie Github Links
- [dt-core github](https://github.com/duckietown/dt-core)
- [duckie code-example github](https://github.com/duckietown/code-examples)