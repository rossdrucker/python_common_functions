# -*- coding: utf-8 -*-
"""
@author: Ross Drucker
"""

import holidays
import datetime
import pandas as pd


def create_holiday_frame():
    '''
    Create a dataframe with all holiday run ups and hangovers

    A run up is two days prior to a holiday and a hangover is 2 days after
    a given holiday
    '''

    def no_holiday(obs):
        '''
        This US holidays package returns a null if there is no holiday, and we
        want to flip that null into a string so we can remove it later when we
        encode the columns
        '''
        if obs == None:
            return_value = 'No_Holiday'
        else:
            return_value = obs

        return return_value

    # Load the united states holidays
    us_holidays = holidays.UnitedStates()
    holiday_frame = pd.DataFrame()

    # Iterate over every day starting on January 1st 2016 and check
    start_date = datetime.datetime(year = 2016, day = 1, month = 1)
    for i in range(0,(365 * 10)):
        holiday_frame.loc[i,'event_date'] = start_date + datetime.timedelta(i)
        holiday_frame.loc[i,'Holiday'] = us_holidays.get(holiday_frame.loc[i,
                         'event_date'])


    # Get a list of unique holidays and the non nulls
    unique_holidays = holiday_frame['Holiday'].unique().tolist()
    unique_holidays = [holiday for holiday in unique_holidays if holiday !=\
                       None]

    # But in the holiday hangovers for the two days after
    for i in range(0,len(holiday_frame)):
        if holiday_frame.loc[i,'Holiday'] in unique_holidays:
            for bar in range(1,2):
                holiday_frame.loc[i + bar,'Holiday'] = 'Holiday_Hangover'

            # Put in the holiday hangovers for the two days before
    for i in range(0,len(holiday_frame)):
        if holiday_frame.loc[i,'Holiday'] in unique_holidays:
            for bar in range(1,2):
                if i - bar < 0:
                    pass
                else:
                    holiday_frame.loc[i - bar,'Holiday'] = 'Holiday_RunUp'

    # New years can create some negative indexes don't need them that far back
    holiday_frame['event_date'] = holiday_frame['event_date'].\
    apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'))
    holiday_frame.index = holiday_frame['event_date']
    holiday_frame['Holiday'] = holiday_frame['Holiday'].apply(lambda x: \
                 no_holiday(x))

    return holiday_frame