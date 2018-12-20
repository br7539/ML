# -*- coding: utf-8 -*-
"""
Neuron Sheet Analysis

This script parses and provides analysis for the neuron worksheet.
"""

import matplotlib as plt
import numpy as np
import pandas as pd


# =============================================================================
# Import and Clean File
# =============================================================================

def clean_sheet(file, sheets):
    "This functions cleans and returns dictionary of sheets"
    
    # import file
    df_multiple = pd.read_excel(file, sheets)
    
    # loops over dictionary of sheets
    for sheet_i, df in df_multiple.items():
    
        # Fill missing row values
        for index, row in df.iterrows():
            if isinstance(row['Neuron Name'],str):
                neuron = row['Neuron Name']
            else:
                df.loc[index,'Neuron Name']= neuron
            if isinstance(row['Soma Compartment'], str):
                soma = row['Soma Compartment']
            else:
                df.loc[index,'Soma Compartment']= soma
                soma = None
            if isinstance(row['Neuron Status'],str):
                status = row['Neuron Status']
            else:
                df.loc[index,'Neuron Status']= status
            if isinstance(row['Dendrites'],str):
                dendrites = row['Dendrites']
            else:
                df.loc[index,'Dendrites']= dendrites
            if isinstance(row['In Database'],str):
                database = row['In Database']
            else:
                df.loc[index,'In Database']= database
            if isinstance(row['Database ID'],str):
                _id = row['Database ID']
            else:
                df.loc[index,'Database ID']= _id
                _id = None
    # dictionary of dataframes (key = sheet)       
    return df_multiple

# =============================================================================
# Functions for whole samples
# =============================================================================

def segmentV_speed(df):
    "Average speed per segment version on completed neurons (w/ duplicates)"
    
    manual, assist_manual, frags, assist_frags = [], [], [], []
    # Iterate over dataframe
    for index, row in df.iterrows():  
        # check neuron status and if it has speed annotated
        if row['Neuron Status'] == 'Completed' and \
        not np.isnan(row['Speed (mm/hr)']):
            # add speed to variables
            if row['Segment Ver.'] == 'Manual':
                manual.append(row['Speed (mm/hr)'])
            if row['Segment Ver.'] == 'Assisted Manual':
                assist_manual.append(row['Speed (mm/hr)'])
            if row['Segment Ver.'] == 'De-Novo Merge':
                frags.append(row['Speed (mm/hr)'])
            if row['Segment Ver.'] == 'Assisted Merge':
                assist_frags.append(row['Speed (mm/hr)'])
      
    # Calculate average speed over segment versions
    manual_speed = np.average(manual)
    assist_manual_speed = np.average(assist_manual)
    frags_speed = np.average(frags)
    assist_frags = np.average(assist_frags)
    # list of segment speeds
    return manual_speed, assist_manual_speed, frags_speed, assist_frags 
        

def segmentV_speed_single(df):
    "Average speed per segment version on completed neurons with annotated speeds"
    
    manual, assist_manual, frags, assist_frags = [], [], [], []   
    # Iterate over dataframe
    for index, row in df.iterrows():        
        
        # if same neuron (sequential) 
        if df.iloc[index]['Neuron Name'] == df.iloc[index+1]['Neuron Name']:
            
            # do if individual neuron is completed and speed is annotated
            if df.iloc[index]['Neuron Status'] == 'Completed' and \
            not np.isnan(df.iloc[index]['Speed (mm/hr)']):

                # neuron 1
                if df.iloc[index]['Segment Ver.'] == "Manual":
                    manual.append(df.iloc[index]['Speed (mm/hr)'])
                if df.iloc[index]['Segment Ver.'] == 'Assisted Manual':
                    assist_manual.append(df.iloc[index]['Speed (mm/hr)'])
                if df.iloc[index]['Segment Ver.'] == 'De-Novo Merge':
                    frags.append(df.iloc[index]['Speed (mm/hr)']) 
                if df.iloc[index]['Segment Ver.'] == 'Assisted Merge':
                    assist_frags.append(df.iloc[index]['Speed (mm/hr)']) 
                               
                # neuron 2                                    
                if df.iloc[index+1]['Segment Ver.'] == 'Manual':
                    manual.append(df.iloc[index+1]['Speed (mm/hr)'])
                if df.iloc[index+1]['Segment Ver.'] == 'Assisted Manual':
                    assist_manual.append(df.iloc[index+1]['Speed (mm/hr)'])
                if df.iloc[index+1]['Segment Ver.'] == 'De-Novo Merge':
                    frags.append(df.iloc[index+1]['Speed (mm/hr)'])
                if df.iloc[index+1]['Segment Ver.'] == 'Assisted Merge':
                    assist_frags.append(df.iloc[index+1]['Speed (mm/hr)'])
                    
    # Calculate average speed over segment versions
#    manual_speed = np.average(manual)
#    assist_manual_speed = np.average(assist_manual)
#    frags_speed = np.average(frags)
#    assist_frags_speed = np.average(assist_frags)
    # list of segment speeds
    return  manual, assist_manual
#[manual_speed, assist_manual_speed, frags_speed, assist_frags_speed],

def length_total(df):
    "Length of completed neurons (w/ duplicates)"
    
    length = []
    # Iterate over dataframe
    for index, row in df.iterrows():        
        # do if neuron is completed and length is annotated    
        if row['Annotator Progress'] == 'Completed' and \
        not np.isnan(row['Length (mm)']):  
            # add length to list
            length.append(row['Length (mm)'])
    # calculation
    total_len, length_avg, neuron_n = sum(length), np.average(length), len(length)
    # list of total length, length average, and neuron number
    return total_len, length_avg, neuron_n


def neuron_status(df):
    'Counts number of incomplete/untraceable Neuron Status'
    
    incomplete, untraceable = 0, 0
    # Iterate over dataframe
    for index, row in df.iterrows():  
        
        # if same neuron (sequential) 
        if df.iloc[index-1]['Neuron Name'] == df.iloc[index]['Neuron Name']:
        
            # check neuron status and if it has speed annotated
            if row['Neuron Status'] == 'Incomplete':
                incomplete +=1
            if row['Neuron Status'] == 'Untraceable':
                untraceable +=1

    return incomplete, untraceable


# def get_neuron_coord(df, feature0, feature1, feature2, feature3):
#     'Creates a list of neuron features'
#
#     coord, features_list = [], []
#
#     # Iterate over dataframe
#     for index, row in df.iterrows():
#         # check neuron status
#         if row['Segment Ver.'] == 'Manual' and row['Annotator Progress'] == feature0:
#             coord.append(row['Neuron Location (µm)'])
#             features_list.append(row['Annotator Progress'])
#         if row['Segment Ver.'] == 'Manual' and row['Annotator Progress'] == feature1 or \
#         row['Annotator Progress'] == feature2 or row['Annotator Progress'] == feature3:
#             feature_list.append(row['Neuron Location (µm)'])
#             features_list.append(row['Annotator Progress'])
#
#     return coord, features_list

# =============================================================================
# Functions for individuals
# =============================================================================
def annotator_progress(df, annotator):
    "Annotator tracing progress (length, speed, #neurons, segmentation ver.)"

    length, speed, neuron_n = [], [], 0
    manual, assist_manual, frags, assist_frags = 0, 0, 0, 0
    # Iterate over dataframe
    for index, row in df.iterrows():        
        # length    
        if row['Annotator Progress'] == 'Completed':
                length = []
    # Iterate over dataframe
    for index, row in df.iterrows():        
        # do if annotator and neuron is completed and length is annotated    
        if row['Annotator Progress'] == 'Completed' and \
        row['Annotator'] == annotator: 
            # total neuron number
            neuron_n +=1
            # add length to list
            if not np.isnan(row['Length (mm)']):  
                length.append(row['Length (mm)'])
            # add speed           
            if not np.isnan(row['Speed (mm/hr)']):
                speed.append(row['Speed (mm/hr)'])
            # segmentation ver.
            if row['Segment Ver.'] == 'Manual':
                manual +=1
            if row['Segment Ver.'] == 'Assisted Manual':
                assist_manual +=1
            if row['Segment Ver.'] == 'De-Novo Merge':
                frags +=1
            if row['Segment Ver.'] == 'Assisted Merge':
                assist_frags +=1
    # list of segmentation versions
    ### Try using and returning sorted tuples for use in pie graph ###
    segmentation_v = [manual, assist_manual, frags, assist_frags]
    # calculations
    speed_avg = np.average(speed)
    length_total = sum(length)   
    # length, speed, neuron_n, segmentation_v (list)        
    return speed, length, neuron_n, segmentation_v, speed_avg, length_total



def graph_annotator_progress(df, annotator):
    "Graphs boxplot of speed, piechart of segmentation, and MISC"
    
    # call annotator progress function and get desired output
    speed, length, neuron_n, segmentation_v,t,length_total = annotator_progress(df, annotator)
    # graph
    plt.subplot(1,2,1)
    plt.title('Speed')
    plt.boxplot(speed, meanline=True, showmeans=True)
    plt.subplot(1,2,2)
    plt.title('Segmentation')
    plt.pie(segmentation_v, labels= ['manual','assist_manual','frags','assist_frags'])
    plt.figtext(0,0,f"Total neurons = {neuron_n}\n"f"Total length= {length_total}")
    plt.show()
    plt.close()
    
    return


# =============================================================================
# Results
# =============================================================================

#df_multiple = clean_sheet('Active_Neuron_Worksheet.xlsx', ['2018-04-03','2018-04-13'])
#
#annotator = 'Bruno'
#
## loops over dictionary of sheets
#for sheet_i, df in df_multiple.items():
#        
#    print(sheet_i, '\n',annotator)
#    graph_annotator_progress(df, annotator)
    
 

        
