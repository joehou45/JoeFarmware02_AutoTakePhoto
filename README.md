# Problem:

You can display pictures taken by built-in camera in the Farm Designer. This theoretically gives you a possibility to
take a picture of your entire garden. Unfortunately it did not work for me because:
- it requires to build a tedious sequence of moving and taking picture steps
- repeated Relative Moves do not work for me https://forum.farmbot.org/t/absolute-vs-relative-move/3530/7
- Like many other people I have problems with the built-in camera (black screens and UART device removed errors)


# Solution:

This Farmware helps to take a picture without all these troubles. You only need to specify the enclosing box and desired
step sizes. If during the process your camera fails - you'll be able to restart your bot and resume from where it broke.
No need to create long sequences anymore.

IMORTANT: It is impossible to call one farmware from another. So you need to create a sequence "Take a photo" that calls
farmware that takes a photo.

Camera starts taking pictures from the corner with min coordiantes and advances with suggested steps on X and than on Y
coordinates till it reaches the corner with max coordinates.

It is probably not a good idea to supply (0,0) - (max_x, max_y) because otherwise you will see a lot of copies of your
gantry that moves along with the camera. Your goal is to specify the smallest rectangle inside your raised bed that still
gives you the full coverage of the bed. This depends of the camera you are using, its position on Z axis and bed orientation.

# What can be improved

If your plant is tall I think it is impossible to get a good picture of it stiched from several shots. It might be a
good idea at the end of the sequence to take a single shot of each plant that has a decent spread.

# Installation

Use the the folloiwing manifest to register this Farmware https://raw.githubusercontent.com/etcipnja/Selfie/master/Selfie/manifest.json

Thank you,
Eugene
