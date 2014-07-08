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
import colorsys
import numpy as np
from timing import linear_number


def mix(rgba_orig, rgba_dest, ratio=0.5, interpoller=linear_number):
    (r_o, g_o, b_o, a_o) = rgba_orig
    (r_d, g_d, b_d, a_d) = rgba_dest
    return (  interpoller(r_o, r_d, ratio)
            , interpoller(g_o, g_d, ratio)
            , interpoller(b_o, b_d, ratio)
            , interpoller(a_o, a_d, ratio))

def from_to(rgba_orig, rgba_dest, quantity_of_ticks, func, interpoller=linear_number):
    a=[]
    ticks_frequency = 1.0/quantity_of_ticks
    for ratio in np.arange(0, 1.0+(ticks_frequency/2), ticks_frequency): #add ticks_frequency/2 to 1.0 limit in order to be sure to keep 1.0 as a value
        #print "current ratio", ratio
        def generate_to_call(r):
            def to_call():
                #print "current r", r
                return func(mix(rgba_orig, rgba_dest, r, interpoller))
            return to_call

        a.append(generate_to_call(ratio))
    return a

# Utilities
def rotate_hue(rgba, amount=0.005):
    (r, g, b, a) = rgba
    # print "rgba", rgba
    (r, g, b) = float(r) / 255.0, float(g) / 255.0, float(b) / 255.0
    # print "rgb", (r,g,b)
    hls = colorsys.rgb_to_hls(r, g, b)
    # print "hls", hls

    (h, l, s) = hls
    h = max(h + amount % 1.0, 0.005)

    # print "new hls", (h,l,s)
    (r, g, b) = colorsys.hls_to_rgb(h, l, s)
    # print "new rgb", (r,g,b)
    (r, g, b) = int(r * 255), int(g * 255), int(b * 255)
    rgba = (r, g, b, a)

    # print "new rgba", rgba
    return rgba

# beware, there is a little trick in order to keep the hue : value cannot
# go under 1


def lighten(rgba, amount=0.005):
    (r, g, b, a) = rgba
    # print "rgba", rgba
    (r, g, b) = float(r) / 255.0, float(g) / 255.0, float(b) / 255.0
    # print "rgb", (r,g,b)
    hls = colorsys.rgb_to_hls(r, g, b)
    # print "hls", hls

    (h, l, s) = hls
    l = max(min(l + amount, 0.995), 0.005)

    # print "new hls", (h,l,s)
    (r, g, b) = colorsys.hls_to_rgb(h, l, s)
    # print "new rgb", (r,g,b)
    (r, g, b) = int(r * 255), int(g * 255), int(b * 255)
    rgba = (r, g, b, a)

    # print "new rgba", rgba
    return rgba


def darken(rgba, amount=0.005):
    return lighten(rgba, -amount)
