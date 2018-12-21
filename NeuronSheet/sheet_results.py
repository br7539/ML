# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 13:12:25 2018

@author: dossantosb
"""

import neuronsheet as ns

# =============================================================================
# Annotator Progress
# =============================================================================

#df_multiple = ns.clean_sheet('Active_Neuron_Worksheet.xlsx', ['2018-04-03','2018-04-13'])
#
#annotator = 'Bruno'
#
## loops over dictionary of sheets
#for sheet_i, df in df_multiple.items():
#        
#    print(sheet_i, '\n',annotator)
#    ns.graph_annotator_progress(df, annotator)
    
    
    
# =============================================================================
# Neuron progress (across samples)
# =============================================================================
    
#df_multiple = ns.clean_sheet('Finished_Worksheet.xlsx', ['2018-08-01','2018-07-02','2018-06-14','2018-05-23','2018-04-13',\
#'2018-04-03','2018-03-09','2018-01-30','2017-12-19','2017-11-17','2017-10-31','2017-09-25','2017-09-19',\
#'2017-09-11','2017-08-28','2017-08-10','2017-06-28','2017-06-10','2017-05-04','2017-04-19','2017-02-22',\
#'2017-01-15','2016-10-31','2016-10-25','2016-07-18','2016-04-04','2015-07-11','2015-06-19',\
#'2014-06-24'])
#
## loops over dictionary of sheets
#for sheet_i, df in df_multiple.items():
#        
#    status = ns.neuron_status(df)
#    print(sheet_i, status)


# =============================================================================
# Compare segment
# =============================================================================
    
df_multiple = ns.clean_sheet('Finished_Worksheet.xlsx', ['2018-06-14'])

# loops over dictionary of sheets
for sheet_i, df in df_multiple.items():
        
    manual, assist_manual = ns.segmentV_speed_single(df)
    print(sheet_i, manual)
    print(sheet_i, assist_manual)