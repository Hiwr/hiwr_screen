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

from random import randint, random
from math import cos, sin, ceil
from collections import deque
from Queue import Queue
import sys
import numpy as np

from efl.evas import SmartObject, EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.evas import Map

from efl.ecore import Animator, Timer


from config import path, script_path, img_path, font_path, video_path
from color import rotate_hue, lighten, darken, from_to
from animation import animation_queue, animation_arrays
from timing import linear_number, sinusoidal_number, linear_tuple_number
from bubbles import Bubble

class Transformable(SmartObject):

    def __init__(self, transformable):
        self.rotation=None
        self.scaling=None
        self.transformable_set(transformable)

    def transformable_set(self, transformable):
        self.transformable=transformable

    def rotate_and_scale(self, x_factor=0.5, y_factor=None, degree=15.0, rotate_center=None, scale_center=None):
        self.transformable.show()

        if not rotate_center:
            if not scale_center:
                rotate_center = scale_center = self.transformable.center
            else:
                rotate_center = scale_center

        if not y_factor:
            y_factor = x_factor

        pos = self.pos

        self.transformable.map_enabled = False

        m = Map(4)
        m.alpha=True
        m.util_points_populate_from_object(self.transformable)

        m.util_rotate(degree, rotate_center[0], rotate_center[1])
        m.util_zoom(x_factor, y_factor, scale_center[0], scale_center[1])
        
        self.transformable.map = m
        self.transformable.map_enabled = True
        m.delete()
        del m
        #print "self.pos", self.pos, "self.transformable.pos", self.transformable.pos
        self.transformable.move( *pos )

    def rotate(self, degree=15.0, center=None):
        #print "rotate transformable!", degree
        self.rotation = (degree, center)
        if not center:
            center=self.transformable.center

        if self.scaling:
            return self.rotate_and_scale(self.scaling[0], self.scaling[1], degree, center, self.scaling[2])
        else:
            return self.rotate_and_scale(1.0, 1.0, degree, center, center)

    def scale(self, x_factor=0.5, y_factor=None, center=None):
        if not center:
            center = self.transformable.center
        if not y_factor:
            y_factor = x_factor

        #print "scale transformable!", x_factor, y_factor, center

        self.scaling = (x_factor, y_factor, center)
        if self.rotation:
            return self.rotate_and_scale(x_factor, y_factor, self.rotation[0], self.rotation[1], center)
        else:
            return self.rotate_and_scale(x_factor, y_factor, 0, center, center)