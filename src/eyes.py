#!/usr/bin/env python
# encoding: utf-8

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

import os
from random import randint
from math import cos, sin, ceil

from efl.evas import SmartObject, EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.evas import Rectangle, Line, Text, Polygon, EVAS_TEXT_STYLE_PLAIN, EVAS_TEXT_STYLE_OUTLINE, EVAS_TEXT_STYLE_SOFT_OUTLINE, EVAS_TEXT_STYLE_GLOW, EVAS_TEXT_STYLE_OUTLINE_SHADOW, EVAS_TEXT_STYLE_FAR_SHADOW, EVAS_TEXT_STYLE_OUTLINE_SOFT_SHADOW, EVAS_TEXT_STYLE_SOFT_SHADOW, EVAS_TEXT_STYLE_FAR_SOFT_SHADOW


from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.button import Button
from efl.elementary.image import Image
from efl.elementary.box import Box, ELM_BOX_LAYOUT_FLOW_HORIZONTAL

from efl.elementary.frame import Frame
from efl.elementary.icon import Icon
from efl.elementary.label import Label
from efl.elementary.list import List
from efl.elementary.bubble import Bubble, ELM_BUBBLE_POS_TOP_LEFT, \
    ELM_BUBBLE_POS_TOP_RIGHT, ELM_BUBBLE_POS_BOTTOM_LEFT, \
    ELM_BUBBLE_POS_BOTTOM_RIGHT

from efl.ecore import Animator
import roslib
import rospy


EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

path = roslib.packages.get_pkg_dir('eyes')
script_path = os.path.join(path, "src") #os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_path, "hyve-eyes-png")
font_path = os.path.join(script_path, "fonts","fontawesome-webfont.ttf")

print font_path

screenSize = (screenX, screenY) = (800, 480)
global_offset = 0,-60

eyeballs_size = (eyeballs_size_x, eyeballs_size_y) = (420, 112)
eyeballs_pos = ((screenX - eyeballs_size_x)/2 + global_offset[0], (screenY-eyeballs_size_y)/2 + global_offset[1])
#--tests eyeball move animability
eyeballs_latest_pos_index = 0
#--

#-- ros
follow = ''
animate = ''
#--

def draw(win, bg, eyeballs, eyes, blink):
    
    #print "draw"

    #--tests eyeball move animability
    global eyeballs_latest_pos_index
    eyeballs.move(eyeballs_pos[0]+30*cos(eyeballs_latest_pos_index), eyeballs_pos[1]+30*sin(eyeballs_latest_pos_index))
    eyeballs_latest_pos_index+=0.1
    #--
    eyes.clip.color = (0,0,(100+eyeballs_latest_pos_index*10)%255,255)

    #if randint(0,100) > 1 :
        #print "eyes"
    #    blink.hide()
    #    eyes.show()
    #else :
        #print "blink"
    #    eyes.hide()
    #    blink.show()

    #win.resize(screenX, screenY)
    #win.show()
def listener():
    rospy.init_node('listener', anonymous=True)
    follow = rospy.Subscriber("EyesLook", EyesLook, callback, None ,1 )
    animate = rospy.Subscriber("animate", Animation, canimate, None, 1)
    touch = rospy.Subscriber("touch", TouchEvent , touchback, None, 1)
    rospy.spin()

def main_loop():
    win = StandardWindow("WLX42 Eyes", "Eyes of the robot", autodel=True)
    win.callback_delete_request_add(lambda o: elementary.exit())

    bg = Rectangle(win.evas, size = screenSize, color=(0,0,100,255), pos=(0,0))
    #bg.clip = Rectangle(win.evas, size = screenSize, color=(0,0,100,255), pos=(0,100) )
    bg.show()

    underlay = Rectangle(win.evas, pos=global_offset, size = screenSize, color=(255,255,255,255))
    underlay.show()

    eyes = Image(win, size = screenSize, pos=global_offset, file=os.path.join(img_path, "oeil-1.png"))
    #overlay.clip = Image(win, size = screenSize, pos=(0,0), file=os.path.join(img_path, "mb.png"))
    #overlay.clip.show()
    eyes.clip = Rectangle(win.evas, size = screenSize, color=(0,0,100,255), pos=(0,0) )
    eyes.clip.show()
    eyes.show()

    mustache = Image(win, size=screenSize, pos=global_offset, file=os.path.join(img_path, "moustaches.png"))
    mustache.clip = Rectangle(win.evas, size = screenSize, color=(0,0,100,255), pos=(0,0) )
    mustache.clip.show()
    mustache.stack_above(eyes)
    mustache.show()

    bubble_pos = (0,100)
    bubble_size = (2*106, 2*159)

    bubble = Image(win, size = bubble_size, pos=bubble_pos, file=os.path.join(img_path, "bulle.png"))

    bubble.clip = Rectangle(win.evas, size = bubble_size, color=(255,255,255,200), pos=bubble_pos )
    bubble.clip.show()
    bubble.stack_above(eyes)
    bubble.show()

    bubble_text_pos=(bubble_pos[0]+10, bubble_pos[1]+10)
    bubble_text = Text(win.evas, text='', color=(255,255,255,255), pos=bubble_text_pos, size=(180,180))
    bubble_text.font_source = font_path
    bubble_text.font = "FontAwesome", 150
    bubble_text.style = EVAS_TEXT_STYLE_SOFT_SHADOW
    bubble_text.shadow_color = (64,64,64,127)
    bubble_text.stack_above(bubble)
    bubble_text.show()

#    bx = Box(win)
#    win.resize_object_add(bx)
#    bx.size_hint_weight = EXPAND_BOTH
#    bx.show()
#    lb.show()

#    lb = Label(win, text="Blah, Blah, Blah")
#    lb2 = Label(win, text="Tut, Tut, Tut!")
#    bb = Bubble(win, text = "Message 1", content = lb,
#        pos = ELM_BUBBLE_POS_TOP_LEFT, size_hint_weight = EXPAND_BOTH,
#        size_hint_align = FILL_BOTH)
#    bb.part_text_set("info", "Corner: top_left")
#    bb.part_content_set("icon", ic)
#    bx.pack_end(bb)
#    bb.show()

    eyeballs = Image(win, size = eyeballs_size, pos=eyeballs_pos, file=os.path.join(img_path, "retine_sim.png"))
    

    blink = Image(win, size = screenSize, pos = global_offset, file=os.path.join(img_path, "oeil-11.png"))
    blink.clip = eyes.clip;

    dead = Image(win, size = screenSize, pos = global_offset, file=os.path.join(img_path, "oeil-10.png"))

    #eyes
    eyeballs.stack_below(eyes)
    eyeballs.show()

    def on_tick(*args, **kargs):
        draw(win, bg, eyeballs, eyes, blink)
        return True

    Animator(on_tick)

    draw(win, bg, eyeballs, eyes, blink)

    win.resize(screenX, screenY)
    win.show()

if __name__ == "__main__":
    elementary.init()
    main_loop()

    elementary.run()
    elementary.shutdown()
