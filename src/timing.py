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
from math import cos, sin, ceil, pi

def linear_number(origin_value, destination_value, ratio=0.5):
	val = origin_value * (1.0-ratio) + destination_value * ratio
	#print "origin ", origin_value, "destination", destination_value, "ratio ", ratio, "value ", val
	return val

def sinusoidal_number(origin_value, destination_value, ratio=0.5):
	return origin_value + ( 1 - cos(ratio * pi) ) /2 * (destination_value - origin_value)

def linear_tuple_number(origin_value, destination_value, ratio=0.5, length=2):
	return tuple([linear_number(origin_value, destination_value, ratio) for i in range (1, length)])