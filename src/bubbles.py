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
from efl.evas import SmartObject, EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.evas import Rectangle, Line, Text, Polygon, ClippedSmartObject, Box, \
    EVAS_TEXT_STYLE_PLAIN, EVAS_TEXT_STYLE_OUTLINE, EVAS_TEXT_STYLE_SOFT_OUTLINE, EVAS_TEXT_STYLE_GLOW, \
    EVAS_TEXT_STYLE_OUTLINE_SHADOW, EVAS_TEXT_STYLE_FAR_SHADOW, EVAS_TEXT_STYLE_OUTLINE_SOFT_SHADOW, \
    EVAS_TEXT_STYLE_SOFT_SHADOW, EVAS_TEXT_STYLE_FAR_SOFT_SHADOW

from efl import emotion
from efl.emotion import Emotion

from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.image import Image

from efl.ecore import Animator, Timer

from config import path, script_path, img_path, font_path

#-- colors
WHITE = (255, 255, 255, 255)
BLUE = (0, 0, 100, 255)
YELLOW = (210, 210, 0, 255)
GREEN = (0, 230, 0, 255)
RED = (230, 0, 0, 255)
#--

# QR Code awesome font char: 

class Bubble(SmartObject):
    def __init__(self, win):
        SmartObject.__init__(self, win.evas)
        self.name = "bubble"
        #, pos=(0,100)
        bubble_size = (2*106, 2*159)
        self.bubble = Image(win, size=bubble_size, file=os.path.join(img_path, "bulle.png"))
        self.bubble.clip = Rectangle(win.evas, size=bubble_size, color=(255,255,255,200) )
        self.member_add(self.bubble)
        self.member_add(self.bubble.clip)

        self.show()

    def show(self):
        self.bubble.clip.show()
        self.bubble.show()

    def hide(self):
        self.bubble.clip.hide()

    def add(self, content, ratio=1.0, offset_y=None):
        if not offset_y:
            offset_y=(180- 180/ratio)/2
        content.size=(180,180/ratio)
        content.show()
        content.pos=self.pos
        content.clip=self.bubble.clip
        self.content=content
        self.member_add(content)
        content.move_relative(15,15+offset_y)
