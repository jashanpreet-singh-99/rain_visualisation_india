#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import indian_state_list as isl

d_state = isl.d_state

def read_data_csv(year):
    """ Function to Read Database acc to year and remove the unwanted index column
        Return none if the year is out of the range."""

    if 1900 < year <= 2017 :
        path = os.getcwd()
        d = pd.read_csv(path + '/year_record/record_' + str(year) + '.csv')
        d = d.iloc[:,1:]
    else :
        return None
    return d

def detect_presence_of_and(database) :
    """ Detect if state already in d_state if not then check for & in the Sub division
        Return Parent database -> database with new correction column"""

    def remove_state_phase_one(value) :
        if value.lower() in d_state.keys():
            return 0
        else :
            if '&' in value :
                return 1
            return 2
    database['correction'] = database.SUBDIVISION.apply(remove_state_phase_one)
    return database


def remove_the_and(database) :
    """ Remove the & and split the subdivion on the & and create new entrie with same values as previous
        Return the new & less Database"""
    def implementation_of_phase_one(value):
        val = value.split("&")
        return val[0]

    def implementation_of_phase_one_2(value):
        val = value.split("&")
        return val[1]

    # database with only value to correct
    database_correction = database[database.correction == 1].copy()
    # database copy of value to correct
    database_2 = database_correction.copy()
    # split on & and return val 1
    database_correction.SUBDIVISION = database_correction.SUBDIVISION.apply(implementation_of_phase_one)
    # split on & and return val 2
    database_2.SUBDIVISION = database_2.SUBDIVISION.apply(implementation_of_phase_one_2)
    # join both new databases inot database correction
    database_correction = database_correction.append(database_2).copy()
    # assign database value without &
    database = database[database.correction != 1].copy()
    # join in with the database_correction
    database = database.append(database_correction).copy()
    # reset the index
    database.reset_index(drop=True,inplace=True)

    return database

def remove_unwanted_words(database) :
    """ Check for given unwanted words in state name and remove if any present
        Return the corrected database which is free from all unwanted words
    """

    unwanted = ['west', 'east', 'north ', 'south', 'gangetic', 'region', 'coastal', 'sub himalayan', 'interior']

    def remove_word(value) :
        for c_word in unwanted:
            if c_word in value:
                value = value.replace(c_word,"")
        return value.strip()

    database.SUBDIVISION = database.SUBDIVISION.apply(remove_word)
    return database

def detect_presence_of_space(database) :
    """ Detect if corrected state names so far are in d_state -> set correction 0
        if not check for space in name if so set correction -> 1
        Else set correction -> 2
        Return Database with new correction labels
    """

    def remove_state_phase_two(value) :
        if value.lower() in d_state.keys():
            return 0
        else :
            if ' ' in value :
                return 1
            return 3

    database['correction'] = database.SUBDIVISION.apply(remove_state_phase_two)
    return database

def remove_the_space(database) :
    """ Create a list of all the labels, then split them, After that check if the splitted data id required
        if required record the names and original value
        create new database with values to add and joinit with old database
        Return corrected database"""
    # databse with value to correct
    database_correction = database[database.correction == 1].copy()
    # contain state names
    label_s = database_correction.SUBDIVISION
    split_able = {}
    # split the name and check if splted words are in d_state, if present then add to splitable with their original val
    for s in label_s:
        in_s = s.split(" ")
        for s_v in in_s:
            if s_v.strip().lower() in d_state.keys():
                if s in split_able.keys():
                    split_able[s] += [s_v]
                else :
                    split_able[s] = [s_v]
    # Empty database
    new_data = pd.DataFrame()
    # Add the splited state names into new database and set correction to 0
    for i in split_able.keys() :
        d = database_correction[database_correction.SUBDIVISION == i].copy()
        for v in split_able[i] :
            d.SUBDIVISION = v
            d.correction = 0
            new_data = new_data.append(d, ignore_index=True).copy()
    # get all values that are not to be corrected
    database = database[database.correction != 1].copy()
    # add the new_data database into the parent datbase
    database = database.append(new_data).copy()
    # reset the index
    database.reset_index(drop=True, inplace=True)
    return database

def group_state_and_get_means(database):
    """ Remove the duplicate state name with their mean value entry """
    database = database.groupby('SUBDIVISION', as_index=False).mean().copy()

    database.reset_index(drop=True, inplace=True)
    database = database.round(2)
    return database

def fix_error_prone_states(database) :
    """ Fix the incorrect name of west bengal
        Add the left over states from d_state by duplicating tripura
        joined the old and new datbase
        return datbase with known state with correction value 0 and remove the correction column"""

    # fix the bengal -> WestBengal
    database.loc[4,'SUBDIVISION'] = 'west bengal'
    database.loc[4,'correction'] = 0
    # create list of all labels and convert to lower case
    l = list(database.SUBDIVISION)
    l = [x.lower() for x in l]
    # Check for left over states
    left_over = []
    for item in d_state.keys():
        if item not in l:
            left_over.append(item)
    # new DataFrame
    new_data = pd.DataFrame()
    # Duplicate the Tripura state for the other states as their values was written together and set value = 0
    for val in left_over:
        d = database[database.SUBDIVISION == 'tripura'].copy()
        d.SUBDIVISION = val
        d.correction = 0
        new_data = new_data.append(d).copy()
    # Join the old and new Database
    database = database.append(new_data).copy()
    # get Only Those values that are required
    database = database[database.correction == 0]
    # reindex the State
    database.reset_index(drop=True, inplace=True)
    # Remove the correction Column
    database = database.iloc[:,:-1]
    return database

def save_filtered_data(database) :
    year = database.YEAR[5]
    path = os.getcwd()
    return database.to_csv(path + '/year_record_filtered/record_' + str(year) + '_filtered.csv')
