hiwr\_screen
===============================================

Display eyes and different faces on the screen.

Contributing
----------------------

Contributions via pull request are welcome and may be included under the
same license as below.

Copyright
----------------------

hiwr\_screen, except where otherwise noted, is released under the
[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
See the LICENSE file located in the root directory.

Build
----------------------
build instructions

Execution
----------------------

To start hiwr\_screen, do the following (assuming, you
have a working ROS core running):

   Launch using roslaunch:

   > rosrun hiwr\_screen tired\_screen

Node
----------------------

### Subscribed Topics

- `/EyesLook`
    * Put eyes to the position specified

- `/Scenario/state`
    * Face state to display on the screen