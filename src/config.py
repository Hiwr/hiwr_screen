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
import roslib

path = roslib.packages.get_pkg_dir('hyve_screen')
#os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(path, "src")
img_path = os.path.join(script_path, "hyve-eyes-png")
# does not work yet... had to install it in ~/.fonts
font_path = os.path.join(script_path, "fonts", "fontawesome-webfont.ttf")
#video_path = os.path.join(script_path, "video", "bigbuckbunny-trailer.m4v")
video_path = os.path.join(script_path, "video", "BigBuckBunny_320x180.mp4")

