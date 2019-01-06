# -*- coding: utf-8 -*-
"""
Neuron Sheet Analysis

This script parses and provides analysis for the neuron worksheet.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Import and Clean File
# =============================================================================

def clean_sheet(file, sheets):
    "This functions cleans and returns dictionary of sheets (requires correct excell dimentions)"
   
    # import file
    df_multiple = pd.read_excel(file, sheets)
    
    # loops over dictionary of sheets
    for sheet_i, df in df_multiple.items():
    
        # Fill missing row values
        for index, row in df.iterrows():
            # if same neuron
            if isinstance(df.iloc[index-1]['Neuron Name'],str) and \
            not isinstance(df.iloc[index]['Neuron Name'],str) and \
            df.iloc[index-1]['Neuron Name'] != df.iloc[index]['Neuron Name']:
                df.loc[index,'Neuron Name']= df.iloc[index-1]['Neuron Name']
                # add soma compartment
                if isinstance(df.iloc[index-1]['Soma Compartment'],str) and \
                not isinstance(df.iloc[index]['Soma Compartment'],str):
                    df.loc[index,'Soma Compartment']= df.iloc[index-1]['Soma Compartment']
                # add coordinate
                if isinstance(df.iloc[index-1]['Neuron Location (µm)'],str) and \
                not isinstance(df.iloc[index]['Neuron Location (µm)'],str):
                    df.loc[index,'Neuron Location (µm)']= df.iloc[index-1]['Neuron Location (µm)']                    
                # add neuron status
                if isinstance(df.iloc[index-1]['Neuron Status'],str) and \
                not isinstance(df.iloc[index]['Neuron Status'],str):
                    df.loc[index,'Neuron Status']= df.iloc[index-1]['Neuron Status']        
                # add dendrites
                if isinstance(df.iloc[index-1]['Dendrites'],str) and \
                not isinstance(df.iloc[index]['Dendrites'],str):
                    df.loc[index,'Dendrites']= df.iloc[index-1]['Dendrites']
                # add database status
                if isinstance(df.iloc[index-1]['In Database'],str) and \
                not isinstance(df.iloc[index]['In Database'],str):
                    df.loc[index,'In Database']= df.iloc[index-1]['In Database']
                # add database id
                if isinstance(df.iloc[index-1]['Database ID'],str) and \
                not isinstance(df.iloc[index]['Database ID'],str):
                    df.loc[index,'Database ID']= df.iloc[index-1]['Database ID']

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
        if df.iloc[index]['Neuron Name'] == df.iloc[index-1]['Neuron Name']:           
            # do if both tracings are completed and speed is annotated
            if df.iloc[index]['Neuron Status'] == 'Completed' and df.iloc[index-1]['Neuron Status'] == 'Completed' and\
            not np.isnan(df.iloc[index]['Speed (mm/hr)']) and not np.isnan(df.iloc[index-1]['Speed (mm/hr)']):
        
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
                if df.iloc[index-1]['Segment Ver.'] == 'Manual':
                    manual.append(df.iloc[index-1]['Speed (mm/hr)'])
                if df.iloc[index-1]['Segment Ver.'] == 'Assisted Manual':
                    assist_manual.append(df.iloc[index-1]['Speed (mm/hr)'])
                if df.iloc[index-1]['Segment Ver.'] == 'De-Novo Merge':
                    frags.append(df.iloc[index-1]['Speed (mm/hr)'])
                if df.iloc[index-1]['Segment Ver.'] == 'Assisted Merge':
                    assist_frags.append(df.iloc[index-1]['Speed (mm/hr)'])
                    
                    
    #Calculate average speed over segment versions
    manual_speed = np.average(manual)
    assist_manual_speed = np.average(assist_manual)
    frags_speed = np.average(frags)
    assist_frags_speed = np.average(assist_frags)
    
    # [segment speeds], [segment lists]
    return [manual_speed, assist_manual_speed, frags_speed, assist_frags_speed]\
    ,[manual, assist_manual, frags, assist_frags] 
        


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
