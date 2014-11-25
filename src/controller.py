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
from hiwrmsg.msg import Animation 
from hiwrmsg.msg import EyesLook 
from pygame import *

def talker():
    f = rospy.Publisher('EyesLook', EyesLook)
    a = rospy.Publisher('animate', Animation)
    rospy.init_node('talker')
    anim =Animation()
    look = EyesLook()
    while not rospy.is_shutdown(): 

        # teleportation au centre
        look.x=0
        look.y=0
        look.delay = 0
        f.publish(look)
        time.wait(1000)
        
        # Test de fluiditee
        look.x=70
        look.y=30
        look.delay = 10
        f.publish(look)
        look.x=-70
        look.y=-30
        look.delay = 10
        f.publish(look)
        time.wait(1000)
        #Test Blink
        time.wait(500)
        anim.animation = 'blink'
        anim.temps = 100
        a.publish(anim)
        time.wait(200)
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
