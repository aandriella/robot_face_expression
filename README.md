# Repo used to generate TIAGo Facial expressions

#### Most of the code is taken from the great work of [Bilgehan NAL](https://github.com/bilgehannal/baxter_face_software)  on the Baxter robot #### 



#### Package:
- **face_builder** folder contains all the png images used to build the robot's face.
- **launch** folder contains the ros launch file
- **script** folder contains the code to build the face. Most of the code has been got from the work of Bilgehan NAL and just a few things have been edited or removed in order to get it working with the TIAGo.



How to run it:

``` 
 roslaunch robot_face_expression robot_face_expression.launch 
```

To visualise the different facial expressions you have to run the [robot_face_visualizer](https://github.com/aandriella/robot_face_visualizer) node as follows:

``` 
 rosrun robot_face_visualizer face_visualizer.py
```
