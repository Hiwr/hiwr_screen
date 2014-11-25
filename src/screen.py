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
import re
import signal

from random import randint, random
from math import cos, sin, ceil
from collections import deque
from Queue import Queue
import sys
import numpy as np

import roslib
import rospy
from hiwr_msg.msg import EyesLook
from hiwr_msg.msg import Animation
from hiwr_msg.msg import TouchEvent
import std_msgs

from efl.evas import SmartObject, EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.evas import Rect, Rectangle, Line, Text, Polygon, ClippedSmartObject, Box, Map, \
    EVAS_TEXT_STYLE_PLAIN, EVAS_TEXT_STYLE_OUTLINE, EVAS_TEXT_STYLE_SOFT_OUTLINE, EVAS_TEXT_STYLE_GLOW, \
    EVAS_TEXT_STYLE_OUTLINE_SHADOW, EVAS_TEXT_STYLE_FAR_SHADOW, EVAS_TEXT_STYLE_OUTLINE_SOFT_SHADOW, \
    EVAS_TEXT_STYLE_SOFT_SHADOW, EVAS_TEXT_STYLE_FAR_SOFT_SHADOW
from efl.evas import Image as EvasImage

from efl import emotion
from efl.emotion import Emotion

from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.image import Image

from efl.ecore import Animator, Timer


from config import path, script_path, img_path, font_path
from color import rotate_hue, lighten, darken, from_to
from animation import animation_queue, animation_arrays
from timing import linear_number, sinusoidal_number, linear_tuple_number
from bubbles import Bubble
from transformable import Transformable

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

screen_size = (screenX, screenY) = (800, 480)
global_offset = 0, -60

eyeballs_size = (eyeballs_size_x, eyeballs_size_y) = (420, 112)
eyeballs_pos = ((screenX - eyeballs_size_x) / 2 +
                global_offset[0], (screenY - eyeballs_size_y) / 2 + global_offset[1])
#((screenX - eyeballs_size_x)/2, (screenY - eyeballs_size_y)/2)
#((screenX - eyeballs_size_x)/2 + global_offset[0], (screenY-eyeballs_size_y)/2 + global_offset[1])
#--tests eyeball move animability
eyeballs_latest_pos_index = 0
#--

#-- ros
follow = ''
animate = ''
#--

#-- colors
WHITE = (255, 255, 255, 255)
BLUE = (0, 0, 100, 255)
YELLOW = (210, 210, 0, 255)
GREEN = (0, 230, 0, 255)
RED = (230, 0, 0, 255)
#--
TOP_LEFT = (0, 0)

# e=0
# f=0

todo_queue = Queue(1)

#-- on Move Eye callback

def draw(win, face):
    global todo_queue
    if rospy.is_shutdown():
        elementary.exit()
        #sys.exit(0)
    if(not todo_queue.empty()):
        task = todo_queue.get_nowait()
        task()
        todo_queue.task_done()
    # print "draw"

    #--tests eyeball move animability
    #global eyeballs_latest_pos_index, e, f
    #face.eyes.eyeballs.move(eyeballs_pos[0]+30*cos(eyeballs_latest_pos_index), eyeballs_pos[1]+30*sin(eyeballs_latest_pos_index))
    #face.eyes.eyeballs.move(
    #    30 * cos(eyeballs_latest_pos_index), 30 * sin(eyeballs_latest_pos_index))
    #eyeballs_latest_pos_index += 0.1

    #--
    #if(eyeballs_latest_pos_index * 10 % ((2 * 256) - 1) < 256):
    #    apply(face.color_set, rotate_hue(face.color_get(), 0.005))
    #else:
    #apply(face.color_set, rotate_hue(face.color_get(), 0.005))
    # face.color_set(*lighten(face.color_get(0)))

    #if randint(0, 300) < 2:
        #face.anim_blink()
        # face.anim_tired(face.anim_tired)
        # face.anim_tired(lambda:face.anim_sleep(lambda:face.anim_sleep(lambda:face.anim_sleep(face.standard))))
        # print "eyes"
    #    blink.hide()
    #    eyes.show()
        # e=(e+1)%11
        # face.change_eyes(e)
        # print "change eyes!", e
        # f=(f+1)%3
        # face.change_mustache(e)
        # print "change mustache!", f
    # else :
        # print "blink"
    #    eyes.hide()
    #    blink.show()
        

class EyeBalls(SmartObject): #Transformable

    def __init__(self, win, eyes):
        SmartObject.__init__(self, win.evas)
        self.name = "eyeballs"

        self.eyeballs = Image(
            win, pos=eyeballs_pos, size=eyeballs_size, file=os.path.join(img_path, "retine_sim.png"))


        self.member_add(self.eyeballs)
        #Transformable.__init__(self, self.eyeballs)

        self.show()

    def show(self):
        self.eyeballs.show()

    def hide(self):
        self.eyeballs.hide()


class Eyes(Transformable):

    def __init__(self, win):
        global screen_size, global_offset

        SmartObject.__init__(self, win.evas)
        self.name = "eyes"

        eye_size = screen_size
        self.origin = eye_pos = global_offset

        # white underlay behind eyes
        self.underlay = Rectangle(win.evas, pos=TOP_LEFT, size=eye_size, color=WHITE)
        self.underlay.layer = 0
        self.member_add(self.underlay)

        # eyeballs
        self.eyeballs = EyeBalls(win, self)
        #self.eyeballs.layer = 2
        self.member_add(self.eyeballs)
        #self.eyeballs.stack_above(self.underlay)

        # first load images to retrieve eye size
        self.images = [Image(win, pos=TOP_LEFT, size=eye_size, file=os.path.join(img_path, 'oeil-' + str(i) + '.png'))
                       for i in range(1, 12)]
        # print "eyes image list", self.images
        self.eyes = self.images[0]
        for i in range(0, 11):
            self.member_add(self.images[i])
            self.images[i].layer = 3
            self.images[i].stack_above(self.underlay)
            self.images[i].stack_above(self.eyeballs)

        Transformable.__init__(self, self.eyes)

        self.clip_set(Rectangle(win.evas, pos=TOP_LEFT, size=eye_size, color=BLUE))

        self.show()
        # print "eyes underlay", self.underlay
        # print "eyes current image", self.eyes
        # print "eyes clip", self.clip

    def show(self):
        self.underlay.show()
        self.eyes.show()
        self.clipper.show()
        self.eyeballs.show()

    def hide(self):
        self.clipper.hide()
        self.eyeballs.hide()

    def clip_set(self, clipper):
        self.clipper = clipper
        # self.underlay.clip=clipper
        for i in range(0, 11):
            self.images[i].clip = clipper
        # self.eyes.clip=clipper

    def move_origin(self):
        self.move(*self.origin)

    def color_set(self, r, g, b, a):
        color = (r, g, b, a)
        self.clipper.color = color

    def color_get(self):
        return self.clipper.color

    def change(self, id):
        # print "changing eyes to", id
        self.eyes.hide()
        # print "old eyes hidden", self.eyes
        self.eyes = self.images[id]
        self.transformable_set(self.eyes)
        # print "new eyes still hidden", self.eyes
        self.eyes.show()
        # print "new eyes still displayed", self.eyes


class Mustache(Transformable):

    def __init__(self, win, pos=(0, 0)):

        SmartObject.__init__(self, win.evas)
        self.name = "mustache"

        self.mustache_size = (400, 134)
        # size=mustache_size,
        self.images = [Image(win, pos=TOP_LEFT, size=self.mustache_size, file=os.path.join(img_path, 'moustache-' + str(i) + '.png'))
                       for i in range(1, 3)]
        #print "mustache image list", self.images

        self.mustache = self.images[0]
        #Rectangle(win.evas, pos=TOP_LEFT, size=mustache_size, color=RED)#self.images[0]
        #self.member_add(self.mustache)
        for i in range(0, 2):
            self.member_add(self.images[i])
            self.images[i].layer = 4

        self.move(*pos)

        Transformable.__init__(self, self.mustache)

        # does not support yet rotate + scale with diffrent centers
        #self.rotate(15.0)
        #self.scale(0.5)
        self.show()

    def move(self, x,y):
        self.pos=(x,y)
        SmartObject.move(self, x, y)

    def change(self, id):
        self.mustache.hide()
        self.mustache = self.images[id]
        self.transformable_set(self.mustache)
        self.mustache.show()

    def show(self):
        self.mustache.show()

    def hide(self):
        self.mustache.hide()


class Face(SmartObject):

    def __init__(self, win):
        global screen_size, global_offset
        self.win = win

        SmartObject.__init__(self, win.evas)

        self.bg = Rectangle(
            win.evas, pos=TOP_LEFT, size=screen_size, color=BLUE)
        self.bg.layer = 0
        self.member_add(self.bg)

        self.eyes = Eyes(win)
        self.eyes.layer = 1
        self.eyes.move(global_offset[0], global_offset[1])
        self.eyes.stack_above(self.bg)
        self.member_add(self.eyes)

        self.mustache = Mustache(win, ( global_offset[0] + 200, global_offset[1] + 380 ) )
        #print "mustache.move to",  (global_offset[0] + 200, global_offset[1] + 380)
        #self.mustache.move( global_offset[0] + 200, global_offset[1] + 380 )
        self.mustache.layer = 5
        self.mustache.stack_above(self.eyes)
        self.member_add(self.mustache)

        self.color_set(*BLUE)
        self.standard()
        self.eyes.eyeballs.move(0,0)

        self.show()
        self.anim_standard()

        self.bubbles={}
        #self.anim_sleep()
        #print "bg", self.bg
        #print "eyes", self.eyes

    def show(self):
        self.bg.show()
        self.eyes.show()
        self.mustache.show()

    def hide(self):
        self.bg.hide()
        self.eyes.hide()
        self.mustache.hide()

    def color_set(self, r, g, b, a):
        color = (r, g, b, a)
        self.bg.color = color
        self.eyes.color_set(r, g, b, a)

    def color_get(self):
        return self.bg.color

    def change_eyes(self, id):
        self.eyes.change(id % 11)

    def change_mustache(self, id):
        self.mustache.change(id % 2)

    def noop(self):
        return True

    def add_bubble(self, name, content=None, ratio=1.0, pos=(20,40)):
        bubble=Bubble(self.win)
        bubble.name=name
        bubble.pos=pos
        if content:
            bubble.add(content)

        bubble.show()
        self.bubbles[name]=bubble
        return bubble

    def show_qr_bubble(self):
        if not self.bubbles.get("qr"):
            bubble_text = Text(self.win.evas, text='?', color=WHITE)
            bubble_text.font_source = font_path
            bubble_text.font = "FontAwesome", 130
            bubble_text.style = EVAS_TEXT_STYLE_SOFT_SHADOW
            bubble_text.shadow_color = (64,64,64,127)


            self.add_bubble("qr", bubble_text)
            self.bubbles["qr"].content.move_relative(0,-20)
        else:
            self.bubbles.get("qr").show()

    def show_tv_bubble(self):
        if not self.bubbles.get("tv"):
            bubble_image = Image(self.win, pos=(30,20), size=(160,80), file=os.path.join(img_path, "tv.png"))

            self.add_bubble("tv", bubble_image)
        else:
            self.bubbles.get("tv").show()

    def show_bubble(self, key):
        if self.bubbles.get(key):
            self.bubbles[key].show()

    def hide_bubble(self, key):
        if self.bubbles.get(key):
            self.bubbles[key].hide()

    def hide_all_bubbles(self):
        for key in self.bubbles:
            print "hiding bubble", key
            self.bubbles[key].hide()
            #del self.bubbles[key]

    # Face States
    def standard(self, awaken=True):
        self.awaken = awaken
        self.eyes.change(0)
        self.eyes.move_origin()
        self.color_set(*BLUE)
        return True

    def dead(self, awaken=False):
        self.awaken = awaken
        self.eyes.change(11)
        self.eyes.move_origin()
        self.color_set(*RED)
        return True

    def tired(self, awaken=True):
        self.awaken = awaken
        self.eyes.change(6)
        #self.color_set(*dark_blue)
        self.eyes.move_origin()
        return True

    def sleep(self, awaken=False):
        self.awaken = awaken
        self.eyes.change(10)
        self.eyes.move_origin()
        return True

    def intrigued(self, awaken=True):
        self.awaken = awaken
        self.eyes.change(7)
        self.eyes.move_origin()
        return True

    def astonished(self, awaken=True):
        self.awaken = awaken
        self.eyes.change(8)
        self.eyes.move_origin()
        return True

    def grumpy(self, awaken=True):
        self.awaken = awaken
        self.eyes.change(8)
        self.eyes.move_origin()
        return True

    # Face Animations (default for animating at ~ 30fps)
    def anim_standard(self, blink_max_delay=250.0/30.0, blink_min_delay=50.0/30.0, cb=lambda: None):
        self.animation="standard"
        self.eyes.change(0)

        def set_color(rgba):
            (r, g, b, a) = rgba
            self.color_set(r,g,b,a)
            return True

        animation_arrays( from_to(self.color, BLUE, 10, set_color))

        def on_timer():
            if self.animation == "standard":
                self.anim_blink()
                #self.anim_flash()
                interval = blink_min_delay + (random()* (blink_max_delay-blink_min_delay))
                Timer(interval, on_timer)
            return False

        on_timer()


    def anim_tired(self, cb=lambda: None):
        self.animation="tired"
        def cycle(cb):
            def check():
                if self.animation=="tired":
                    self.anim_tired()
                    return True
                else:
                    cb()
                    return False

            return check


        def on_timer_set_awaken():
            if self.animation == "tired":
                self.anim_blink()
                self.anim_flash(lighten(BLUE, 0.1), 20, lambda: self.anim_colorize(darken(BLUE, 0.02), 20 ) )
                
                #self.anim_flash()
                interval = 1 + (random()* 2)
                Timer(interval, on_timer_set_tired)
            return False

        def on_timer_set_tired():
            if self.animation == "tired":
                self.tired()
                self.anim_colorize(darken(BLUE, 0.05), 180)
                #self.anim_flash()
                interval = 1 + (random()* 4)
                Timer(interval, on_timer_set_asleep)
            return False

        def on_timer_set_asleep():
            if self.animation == "tired":
                self.sleep()

                self.anim_colorize(darken(BLUE, 0.1), 180)
                interval = 1 + (random()* 2)
                Timer(interval, on_timer_set_awaken)
            return False

        on_timer_set_tired()
        #animation_queue(self.standard, self.noop, self.noop
        #    , self.tired, self.noop, self.noop, self.noop, self.noop
        #    , self.standard, self.noop, self.noop, self.tired  # , self.noop, self.noop, self.noop, self.noop
        #    , cycle(cb))


    def anim_blink(self, cb=lambda: None):
        #self.animation="standard"
        animation_queue(
            self.tired, self.noop, self.noop, self.noop, self.noop,
            self.sleep, self.noop, self.noop, self.noop, self.noop, self.standard, cb)

    def anim_sleep(self, cb=lambda: None):
        self.animation="sleep"

        def step(x,y,color):
            def move():
                if self.animation=="sleep":
                    self.eyes.move_relative(x,y)
                    self.color_set(*color)
                    return True
                else:
                    self.eyes.move_origin()
                    
            return move

        def cycle(cb):
            def check():
                if self.animation=="sleep":
                    self.anim_sleep()
                    return True
                else:
                    self.eyes.move_origin()
                    cb()
                    return False
            return check

        animation_queue(
            self.sleep
            , step(0, -2, darken(BLUE,0.002*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, -5, darken(BLUE,0.007*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, -10, darken(BLUE,0.017*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, -10, darken(BLUE,0.027*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, -5, darken(BLUE,0.032*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, -2, darken(BLUE,0.034*5)), self.noop, self.noop, self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, 2, darken(BLUE,0.032*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, 5, darken(BLUE,0.027*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, 10, darken(BLUE,0.017*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, 10, darken(BLUE,0.007*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, 5, darken(BLUE,0.002*5)), self.noop, self.noop, self.noop, self.noop, self.noop
            , step(0, 2, BLUE), self.noop, self.noop, self.noop, self.noop, self.noop, self.noop, self.noop
            #, self.anim_flash
            , cycle(cb))

    def anim_colorize(self, color=YELLOW, quantity_of_ticks=10, cb=lambda: None):
        print "colorize original color", self.color, "destination color", color
        def set_color(rgba):
            (r, g, b, a) = rgba
            self.color_set(r,g,b,a)
            return True
        animation_arrays( from_to(self.color, color, quantity_of_ticks, set_color)
                        , [cb])

    def anim_flash(self, color=YELLOW, quantity_of_ticks=10, cb=lambda: None):
        print "flash original color", self.color, "destination color", color
        def set_color(rgba):
            (r, g, b, a) = rgba
            self.color_set(r,g,b,a)
            return True
        animation_arrays( from_to(self.color, color, quantity_of_ticks, set_color)
                        , from_to(color, self.color, quantity_of_ticks, set_color)
                        , [cb])

    def anim_eyeballs(self, coords, quantity_of_ticks=3, cb=lambda: None):
        print "original eyeball pos", self.eyes.eyes.pos
        dest_pos=(coords.x, coords.y)
        print "destination eyeball pos", dest_pos
        animation_arrays( timing.linear_tuple_number( self.eyes.eyeballs.eyeballs.pos, dest_pos , quantity_of_ticks), [cb])

    def anim_eyes_zoom(self, animation="eyeballs_zoom", quantity_of_ticks=20, cb=lambda: None):
        max_zoom=1.5
        min_zoom=1.0

        delta = 4.0/(quantity_of_ticks)
        #print 'delta', delta
        def scaler(start, stop, ratio):
            #print "scaler", start, stop, ratio
            def scale():
                if self.animation == animation:
                    self.eyes.smooth = False
                    self.eyes.map.smooth = False
                    self.eyes.scale( sinusoidal_number (start, stop, ratio) )
                    return True
                else:
                    self.eyes.scale( 1.0 )
                    self.eyes.smooth = True
                    self.eyes.map.smooth = True
                    cb()
                    return False
            return scale

        def cycle(cb):
            def check():
                #print "should display again if current animation is alarma:", self.animation
                if self.animation == animation:
                    self.anim_eyes_zoom(animation, quantity_of_ticks, cb)
                    return True
                else:
                    cb()
                    return False
            return check

        animation_arrays(
            [  scaler(1.0, max_zoom, ratio)           for ratio in np.arange(  0.0,  1.0 +delta/2, delta )]
            , [scaler(max_zoom, min_zoom, ratio)      for ratio in np.arange(  0.0,  1.0 +delta/2, delta/2 )]
            , [scaler(min_zoom, 1.0, ratio)           for ratio in np.arange(  0.0,  1.0 +delta/2, delta )]
            , [cycle(cb)] )

    def anim_mustache_dance(self, animation="mustache", quantity_of_ticks=30, cb=lambda: None):
        dest_angle=22.0
        delta = 4.0/(quantity_of_ticks)
        #print 'delta', delta
        def rotator(start, stop, ratio):
            #print "rotator", start, stop, ratio
            def rotate():
                if self.animation == animation:
                    self.mustache.smooth = False
                    self.mustache.rotate( sinusoidal_number (start, stop, ratio) )
                    return True
                else:
                    self.mustache.rotate( 0 )
                    self.mustache.smooth = True
                    cb()
                    return False
            return rotate

        def cycle(cb):
            def check():
                #print "should display again if current animation is alarma:", self.animation
                if self.animation == animation:
                    self.anim_mustache_dance(animation, quantity_of_ticks, cb)
                    return True
                else:
                    self.mustache.rotate( 0 )
                    self.mustache.smooth = True
                    cb()
                    return False
            return check

        animation_arrays(
            [  rotator(0, dest_angle, ratio)           for ratio in np.arange(  0.0,  1.0 +delta/2, delta )]
            , [rotator(-dest_angle, dest_angle, ratio) for ratio in np.arange(  1.0, -1.0 +delta/2, -delta/2 )]
            , [rotator(0, dest_angle, ratio)           for ratio in np.arange( -1.0,  0.0 +delta/2, delta )]
            , [cycle(cb)] )


    def anim_alarm(self, cb=lambda: None):
        #print "alarm !"
        self.animation="alarm"
        ref_color = lighten(BLUE, 0.1)

        def cycle(cb):
            def check():
                #print "should display again if current animation is alarma:", self.animation
                if self.animation == "alarm":
                    self.anim_alarm()
                    return True
                else:
                    cb()
                    return False
            return check

        def color_rotate(variation):
            mixed=rotate_hue(ref_color, variation)
            
            def colorize():
                if self.animation == "alarm":
                    self.color_set(*mixed)
                    return True
                elif self.animation == "mustache":
                    self.standard()
                    return True
                else:
                    self.standard()
                    cb()
                    return False
            return colorize


        hues = [ color_rotate(variation) for variation in np.arange(0, 1.001, 0.05) ]
        animation_arrays( hues, [cycle(cb)])


# ROS event handlers
def on_move_eye(pos, face):
    #position = pos
    #print "ROS Eye move:", pos
    #face.eyes.eyeballs.move(pos.x, pos.y)
    face.eyes.eyeballs.move(pos.x, pos.y)

def on_scenario_state(state, face):
    global todo_queue

    #=> Independently of scenario, QR code should flash in yellow, and node animation should be launched too
    print "--> New scenario State received", state
    m = re.search(".*?([0-9]+).*?", str(state))
    state = m.group(1)
    print "--> State :", state

    if(state not in ["1","2","3","4","5","6","7"]): # default + "0"
        # Hyve is tracking face. (EyesLook message should manage that by itself)
        # When a visitor badges its qrcode pass
        #=> standard face is required
        #=> if state 0, timer to aske for qr in 15s
        print "Switching to standard face & standard animation with QR bubble displayed"
        def state0():
            print "doing todo for state 0"
            face.standard()
            face.anim_standard()
            face.hide_all_bubbles()
            face.show_qr_bubble()
            #face.anim_mustache_dance() #disable mustache if rotate
        return todo_queue.put(state0, 1)

    elif (state == "1"):
        print "Standard face, noding, flashing and saying thank you"
        def state1():
            print "doing todo for state 1"
            face.standard()
            face.anim_standard()
            face.hide_all_bubbles()
            face.anim_flash(GREEN)

        return todo_queue.put(state1, 1)


    elif (state == "2"):
        # Hyve is watching the TV
        #=> display a thinking bubble where hiwr shows a TV
        print "Switching watching TV animation"
        def state2():
            print "doing todo for state 2"
            face.standard()
            face.anim_standard()
            #create bubble
            face.hide_all_bubbles()
            face.show_tv_bubble()

        return todo_queue.put(state2, 1)

    elif (state == "3"):
        # Hyve is tired
        #=> tired animation every few seconds
        #=> bubble to ask for night cap in order to sleep
        print "Switching random tired animation"
        def state3():
            print "doing todo for state 3"
            face.tired()
            face.anim_tired()
            face.hide_all_bubbles()

        return todo_queue.put(state3, 1)

    elif (state == "4"):
        # Hyve is sleeping
        #=> sleep animation

        print "Switching to sleep animation"
        def state4():
            print "doing todo for state 4"
            face.sleep()
            face.anim_sleep()
            face.hide_all_bubbles()

        return todo_queue.put(state4, 1)

    elif (state == "5"):
        # Hyve wakes up
        #=> alarm animation, waiting for the visitor to remove the night cap
        print "Switching to Alarm animation"
        def state5():
            print "doing todo for state 5"
            #face.anim_standard()
            face.anim_alarm()
            face.intrigued()
            face.hide_all_bubbles()
            #face.eyes.eyeballs.scale(1.0)
            #face.eyes.eyeballs.scale(0.9)
            #face.eyes.eyeballs.scale(1.0)
            face.anim_eyes_zoom("alarm")
            face.anim_mustache_dance("alarm")
            

        return todo_queue.put(state5, 1)

    elif (state == "6"):
        # Hyve wakes up
        #=> alarm animation, waiting for the visitor to remove the night cap
        print "Switching to standard face & standard animation"
        def state6():
            print "doing todo for state 0"
            face.standard()
            face.anim_standard()
            face.hide_all_bubbles()

        return todo_queue.put(state6, 1)

    elif(state== "7"):
        #Grumpy mode
        def state7():
            face.animation = "grumpy"
            #face.standard()
            #face.anim_alarm()
            
            face.grumpy()
            face.hide_all_bubbles()
            face.anim_mustache_dance("grumpy")

        return todo_queue.put(state7,1)
    
def listener(face):
    print "Setting up ROS listening"
    rospy.init_node('listener', anonymous=True)
    print "ROS listens for EyesLook messages on /EyesLook"
    follow = rospy.Subscriber(
        "EyesLook", EyesLook, lambda pos: on_move_eye(pos, face), None, 1)
    print "ROS listens for String messages on /Scenario/state"
    follow = rospy.Subscriber(
        "Scenario/state", std_msgs.msg.String, lambda state: on_scenario_state(state, face), None, 1)

    #animate = rospy.Subscriber("animate", Animation, canimate, None, 1)
    #touch = rospy.Subscriber("touch", TouchEvent, touchback, None, 1)
    #rospy.spin()


def start():
    win = StandardWindow("Robot Eyes", "Eyes of the robot", autodel=True)
    win.callback_delete_request_add(lambda o: elementary.exit())

    face = Face(win)
    
    draw(win, face)
    def on_tick(*args, **kargs):
        draw(win, face)
        return True

    Animator(on_tick)

    win.resize(screenX, screenY)
    win.show()

    listener(face)


if __name__ == "__main__":
    elementary.init()
    start()
    if(os.geteuid() is 0):
        print "current user is root, renicing the process"
        os.nice(-12)
    elementary.run()

    #elementary.shutdown()
