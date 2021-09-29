AprilTag-imgs
=============

Images of all tags from all the pre-generated [AprilTag 3](https://github.com/AprilRobotics/apriltags) families. You can generate your own layouts or images of tags using our other repo, [AprilTag-generation](https://github.com/AprilRobotics/apriltag-generation).

If the format of the markers is very small (ex : by default, 9x9 pixels), you'll need to rescale them. To do so, you may use the following imagemagick command (Unix) : 

~~~
convert <small_marker>.png -scale <scale_chosen_in_percent>% <big_marker>.png
~~~
