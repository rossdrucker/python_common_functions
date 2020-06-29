# -*- coding: utf-8 -*-
"""
Useful Python functions I use repeatedly

@author: Ross Drucker
"""
import os
import time
import numpy as np
import math
import sys
import datetime

sys.path.insert(0, function_library)
import UnitConversions as convert

# =========================================================================== #
#                       Validate a yes/no or T/F input                        #
# =========================================================================== #
def yes_no_input(prompt = 'Yes or no?: '):
    yn_response = input(prompt)

    if yn_response.upper() in ['Y', 'YES', 'TRUE']:
        return True
    elif yn_response.upper() in ['N', 'NO', 'FALSE']:
        return False
    elif yn_response.upper() in ['Q', 'QUIT']:
        sys.exit()
    else:
        print('Invalid response. Please try again.')
        yes_no_input(prompt)

# =========================================================================== #
#                       Check to see if a file exists                         #
# =========================================================================== #
def check_for_file(directory = os.getcwd(), filename = '', loud = False):
    files = os.listdir(directory)
    if filename in files:
        if loud:
            print(f'{filename} found.')
        return True
    else:
        if loud:
            print(f'{filename} not found.')
        return False

# =========================================================================== #
#               Check to see when the last time a file was modified           #
# =========================================================================== #
def get_last_modification_time(directory = os.getcwd(), filename = ''):
    ts = os.path.getmtime(os.path.join(directory, filename))

    return datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y')

# =========================================================================== #
#                   Save the current directory for later                      #
# =========================================================================== #
def temp_save_directory():
    cd = os.getcwd().replace('\\', '/')

    return cd

# =========================================================================== #
#                       Determine if a year is a leap year                    #
# =========================================================================== #
def determine_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0 and year % 400 != 0:
            return False
        else:
            return True
    else:
        return False

# =========================================================================== #
#                       Create a valid integer input                          #
# =========================================================================== #
def int_input(prompt = 'Number: '):
    num = input(prompt)

    if num.upper() in ['Q', 'QUIT']:
        sys.exit()
    else:
        try:
            num = int(num)
            return num
        except:
            print('Invalid response. Please try again.')
            int_input(prompt)

# =========================================================================== #
#                       Create a valid integer input                          #
# =========================================================================== #
def float_input(prompt = 'Number: '):
    num = input(prompt)

    if num.upper() in ['Q', 'QUIT']:
        sys.exit()
    else:
        try:
            num = float(num)
            return num
        except:
            print('Invalid response. Please try again.')
            int_input(prompt)

# =========================================================================== #
#                 Calculate spherical distance between two points             #
# =========================================================================== #
def get_distance(df, lat2, lon2):
    lat1 = df['Latitude']
    lon1 = df['Longitude']

    # Set constant for Earth's radius
    R = 6371

    # Convert the latitudes and longitudes to radians from degrees
    lat1 = convert.degrees_to_radians(lat1)
    lat2 = convert.degrees_to_radians(lat2)
    lon1 = convert.degrees_to_radians(lon1)
    lon2 = convert.degrees_to_radians(lon2)

    # Make math easier
    sp1 = math.sin(lat1)
    sp2 = math.sin(lat2)
    cp1 = math.cos(lat1)
    cp2 = math.cos(lat2)
    cl12 = math.cos(lon1 - lon2)

    comp = (sp1 * sp2) + (cp1 * cp2 * cl12)

    dist_km = R * math.acos(comp)


    return dist_km

# =========================================================================== #
#               Calculate the percentage difference between two numbers       #
# =========================================================================== #
def get_pct_difference(x1, x2):
    try:
        pct_diff = (x1 - x2) / x2

    except ZeroDivisionError:
        pct_diff = 0

    return pct_diff

# =========================================================================== #
#               Alternative to the round method, useful for printing          #
# =========================================================================== #
def truncate(n, decimals = 0):
    if type(n) not in [int, float]:
        return 0

    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier