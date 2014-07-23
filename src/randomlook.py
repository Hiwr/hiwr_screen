#!/usr/bin/env python

#############################################################################
#                                                                           #
#                                                                           #
# Copyright 2014 Worldline                                                  #
#                                                                           #
# Licensed under the Apache License, Version 2.0 (the "License");           #
# you may not use this file except in compliance with the LICENSE           #
# You may obtain a copy of the License at                                   #
#                                                                           #
#     http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                           #
# Unless required by applicable law or agreed to in writing, software       #
# distributed under the License is distributed on an "AS IS" BASIS,         #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
# See the License for the specific language governing permissions and       #
# limitations under the License.                                            #
#                                                                           #
#############################################################################

import rospy
from hiwr_msg.msg import EyesLook
from random import *;

def talker():
    pub = rospy.Publisher('EyesLook', EyesLook)
    rospy.init_node('talker', anonymous=True)
    r = rospy.Rate(2) # 10hz
    while not rospy.is_shutdown():
        str = EyesLook();
        str.x = ( random()*100 -50) /2   ; 
        str.y = (random()*100 -50) / 2  ; 
        str.delay = 0.2;
#        rospy.loginfo(str)
        pub.publish(str)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
