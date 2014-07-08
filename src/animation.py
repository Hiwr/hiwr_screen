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
from efl.ecore import Animator
from collections import deque
from timing import linear_number

# defines an animation with steps, called on each frame
def animation_queue(first_callback, *callbacks):
        #print "first cb", first_callback
        callbacks = deque(callbacks)
        #print "other cbs", callbacks
        first_callback()

        def on_tick(*args, **kargs):
            if(len(callbacks)):
                #print "run", callbacks[0]
                return (callbacks.popleft())()

        Animator(on_tick)

# defines an animation from multiple arrays of callbacks to call during an animation (eases flash effects, etc.)
def animation_arrays(*arrays):
    array=[]

    for a in arrays:
        #print "add this array to animation stack", a
        array.extend(a)

    return animation_queue(*array)



