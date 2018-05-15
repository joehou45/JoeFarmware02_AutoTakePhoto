# Problem:

You can display pictures taken by built-in camera in the Farm Designer. This theoretically gives you a possibility to
take a picture of your entire garden. Unfortunately it did not work for me because:
- it requires to build a tedious sequence of moving and taking picture steps
- repeated Relative Moves do not work for me https://forum.farmbot.org/t/absolute-vs-relative-move/3530/7
- Like many other people I have problems with the built-in camera (black screens and UART device removed errors)


# Solution:

This Farmware helps to take a picture without all these troubles. You only need is to specify the enclosing box and desired
step sizes. If during the process your camera fails - you'll be able to restart your bot and resume from where it broke.
No need to create long sequences anymore.

IMORTANT: It is impossible to call one farmware from another. So you need to create a sequence "Take a photo" that calls
farmware that takes a photo.

Defaut values work good in case if you have (0,0,0) in the right top corner of your raised bed with the head at top most
position. Update default parameters for your setup.


#Installation
Use the the folloiwing manifest to register this Farmware https://raw.githubusercontent.com/etcipnja/Selfie/master/Selfie/manifest.json

Thank you,
Eugene
