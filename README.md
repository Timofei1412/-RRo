
#  Rower (Team SHP-7-fe) 
[code](Code/rro.py)
## table of contents
  main info & credits
  all components
  necessary programs
    how to install git
    how to install python
    how to install openmv
  how to run

### A robot designed to solve the WRO FutureEngineers 2022 task (Version Mk. IV) 

### © Ksendzov Sergey Dmitrievich (https://www.github.com/AFK1 & https://www.github.com/sergwest)
### © Ksendzov Igor Dmitrievich (https://www.github.com/c4llv07e)
### © Fedorov Timofey Artemavich (https://www.github.com/Timofei1412)
### And our teacher - © Max Vasilchenko


## Introduction
  This robot is based on openmv. Openmv is a machine vision technology. This is used to find boundaries, cubes and lines on the field in WRO Future Engineers 2022. We use the camera to find colored cubes, colored lines, and field boundaries. We programmed in the Opencv idea program and modeling in Autocad Fusion 360, Freecad, Openscad. This robot performs its task in theory and in practice.

## Necessary information
This robot is unique and apart from some of the electronic components, it was developed completely from scratch. Therefore, although in some places it does not look properly assembled, but it fulfills its task (RRo Future Engineers) and does not need a dorobotka. Thanks for your attention

## Repository content
  teamPhoto/ - contain 2 team's photo
  src/ - contain robot's code
  robotPhoto/ - contain 6 robot's photo
  scheme/ - contain robot's scheme and 3d model
  
  If you do not open the photo or it is in insufficient quality, please go to the desired folder and find the photo.

## Photo of the robot:
![Front](views/front.png) 
![Back](views/back.png) 
![Right](views/right.png) 
![Left](views/left.png) 
![Top](views/top.png) 
![Bottom](views/bottom.png)

## About electrical and mechanical components:
### OpenMV
  OpenMV - smart and fast chip with camera. It is use some algorithms for machine vision (see colors, shapes and conditions).
### Pololu micro motor
  We used these motors because they are the most reliable and simple. Also, their fastening perfectly fits our design.
### Gearc ace 450
  This device is our battery. It is suitable for our tasks and has a high energy intensity. Of course, the lack of mounting makes it difficult to work with it, but this is a small problem compared to other batteries.
### Servo MG90
  The MG90S is a servo. Why did we use this particular servo motor? Because it fits perfectly in size, and also has a large mounting area.
### selfmade chip
  Everyone knows that if you want to do something well, do it yourself. Therefore, this board was self-assembled and it does its job well.

### General assembly
First of all, print the case. It will take you about two hours from the print style. After printing, carefully remove the case and make sure that you have removed the supports.
After that, print out the rest of the details or find a decent replacement for them. Insert the parts as shown in the photo, together with the motor and the servo motor.
Somewhere you will need a glue gun, and somewhere you will need a distraction. After all, you can install the remaining electronics and make sure that nothing blocks the camera's view.
At the end, you can connect the wires (don't forget to check the wiring) and start the robot

## Installing the necessary programs:
### Git.
####   Checking for Git
     To see if you already have Git installed, open up your terminal application.
     If you're on a Mac, look for a command prompt application called "Terminal".
     If you're on a Windows machine, open the windows command prompt or "Git Bash".
     Once you've opened your terminal application, type git version. The output will either tell you which version of Git is installed, or it will alert you that git is an unknown command. If it's an unknown command, read further and find out how to install Git.
####Install Git Using GitHub Desktop
     Installing GitHub Desktop will also install the latest version of Git if you don't already have it. With GitHub Desktop, you get a command line version of Git with a robust GUI. Regardless of if you have Git installed or not, GitHub Desktop offers a simple collaboration tool for Git.
     https://git-scm.com/download/

### Python.
https://www.tutorialspoint.com/how-to-install-python-in-windows
### Openmv.
https://www.openmv.io/pages/download


## Setup:
1) download code from github:
```git clone https://github.com/c4llv07e/-RRo.git```
2) Run openmv in created folder.
3) Connect robot to openmv.
4) Setup code.

## Starting the robot:
 - put the robot on the field, directed along the track.
 - click on the button. It will take two seconds until the robot processes the request.

## To turn off the robot:
  Switch the lever on the side to turn off the power. It will take about one second, so keep that in mind

## Our plans for the future.
  We are going to refine our robot. For example, we want to add recognition of other colored cubes and processing of different commands (riding backwards, accelerating straight and so on). Of course, we also want to speed up the work to the possible limit, since this is his main task. Of course, I would also like to increase stability to the maximum. We hope that we will have time to implement it.
