# -*- coding: utf-8 -*-
"""
@author: Ross Drucker
"""
import math

def degrees_to_radians(deg):
    return deg * math.pi / 180

def radians_to_degrees(rad):
    return rad * 180 / math.pi

def km_to_miles(dist):
    return dist * 100000 / 160934.4

def oz_to_lb(oz):
    return oz * .0625