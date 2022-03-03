#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


adj = pd.read_csv('Adjectives_masterfile (4).csv', sep=';')
adj


# In[3]:


ans = pd.read_csv('Tabelle1-Table 1.csv', sep=';')
ans


# In[4]:


# lenght = 0
# for i in range(len(ans)):
#         if len(ans.iloc[i,:])> lenght:
#             lenght = len(ans.iloc[i,:])
# lenght


# In[5]:


# COMPUTING right answer for each participants 
numRightAns = []
numFalseAns = []

for i, x in ans.iterrows():
    rightAns = 0
    falseAns = 0
    
    buf = x.iloc[12:57]
    clean = []
    
    for zz in buf:
        if type(zz) != type(np.nan):
            if zz.strip() != '' and zz not in clean:
                clean.append(zz)
    
#     if i == 19:
#         print(len(clean))
#         print(clean)
    
    if x['Group'] == 1 or x['Group'] == 2 or x['Group'] == 3:
        for j in clean:
            if j in list(adj['Adjektiv'][:45]) or j in list(adj['AdjerlaubteZeichen'][:45]):
                rightAns += 1
            else:
#                 print(j)
                falseAns += 1

    elif x['Group'] == 4 or x['Group'] == 5 or x['Group'] == 6:
        for j in clean:
            if j in list(adj['Adjektiv'][45:]) or j in list(adj['AdjerlaubteZeichen'][45:]):
                rightAns += 1
            else:
                falseAns += 1
#     if i ==19:
#         print(len(clean), rightAns, falseAns)
#         print(clean)
    numRightAns.append(rightAns)
    numFalseAns.append(falseAns)
    
ans['number of correct recall'] = numRightAns
ans['number of False recall'] = numFalseAns


# In[6]:


len(adj['Adjektiv'][45:])


# In[7]:


# recall rate computing
ans['Doppelt'] = ans['Doppelt'].fillna(0)
# correctRecallRate = []
# for i in range(len(numRightAns)):
#     try:
#         correctRecallRate.append(numRightAns[i] / (numFalseAns[i] + numRightAns[i]))
#     except:
#         correctRecallRate.append(np.nan)
        
# ans['correct Recall rate']  = correctRecallRate
# ans['correct Recall']  = numRightAns

# # False recall rate
# ans['False recall'] = 1 - ans['correct Recall rate']
# ans['correct Recall rate'] = ans['correct Recall rate'].fillna(0)
# ans['False recall rate'] = ans['False recall rate'].fillna(0)
ans.iloc[:,57:]


# In[8]:


# COMPUTING recall and FPR based on tense and group 
# numRightAns = []
numPresentRecal = []
numPastRecal = []
numOtherRecal = []

numPosPresentRecal = []
numPosPastRecal = []
numPosOtherRecal = []

numNegPresentRecal = []
numNegPastRecal = []
numNegOtherRecal = []

numNeutralPresentRecal = []
numNeutralPastRecal = []
numNeutralOtherRecal = []


for i, x in ans.iterrows():
    
    posPresentRightAns = 0
    posPastRightAns = 0
    posOtherRightAns = 0
    
    negPresentRightAns = 0
    negPastRightAns = 0
    negOtherRightAns = 0
    
    neutralPresentRightAns = 0
    neutralPastRightAns = 0
    neutralOtherRightAns = 0
    
    presentRightAns = 0
    pastRightAns = 0
    otherRightAns = 0

    buf = x.iloc[12:57]
    cleanAdjList = []
    
    for zz in buf:
        if type(zz) != type(np.nan):
            if zz.strip() != '' and zz not in cleanAdjList:
                cleanAdjList.append(zz)
##group of 1 & 4

    if x['Group'] == 1 or x['Group'] == 4:
        if x['Group'] == 1:
            for aj in cleanAdjList:
                if aj in list(adj['Adjektiv'][:15]) or aj in                list(adj['AdjerlaubteZeichen'][:15]):
                    presentRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1
                    
                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1

                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1
                            
                            
                elif aj in list(adj['Adjektiv'][15:30]) or aj in                list(adj['AdjerlaubteZeichen'][15:30]):
                    pastRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][30:45]) or aj in                list(adj['AdjerlaubteZeichen'][30:45]):
                    otherRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
        elif x['Group'] == 4:
            for aj in cleanAdjList:
                if aj in list(adj['Adjektiv'][45:60]) or aj in                list(adj['AdjerlaubteZeichen'][45:60]):
                    presentRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1
                    
                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1

                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][60:75]) or aj in                list(adj['AdjerlaubteZeichen'][60:75]):
                    pastRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][75:]) or aj in                list(adj['AdjerlaubteZeichen'][75:]):
                    otherRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    
#group of 3 & 6

    elif x['Group'] == 3 or x['Group'] == 6:
        if x['Group'] == 3:
            for aj in cleanAdjList:
                if aj in list(adj['Adjektiv'][:15]) or aj in                list(adj['AdjerlaubteZeichen'][:15]):
                    pastRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][15:30]) or aj in                list(adj['AdjerlaubteZeichen'][15:30]):
                    otherRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][30:45]) or aj in                 list(adj['AdjerlaubteZeichen'][30:45]):
                    presentRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1
                    
                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1

                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1
                            
        elif x['Group'] == 6:
            for aj in cleanAdjList:
                if aj in list(adj['Adjektiv'][45:60]) or aj in                list(adj['AdjerlaubteZeichen'][45:60]):
                    pastRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][60:75]) or aj in                list(adj['AdjerlaubteZeichen'][60:75]):
                    otherRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][75:]) or aj in                list(adj['AdjerlaubteZeichen'][75:]):
                    presentRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1
                    
                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1

                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1


#group of 2 & 5

    elif x['Group'] == 2 or x['Group'] == 5:
        if x['Group'] == 2:
            for aj in cleanAdjList:
                if aj in list(adj['Adjektiv'][:15]) or aj in                list(adj['AdjerlaubteZeichen'][:15]):
                    otherRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][15:30]) or aj in                list(adj['AdjerlaubteZeichen'][15:30]):
                    presentRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1
                    
                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1

                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][30:45]) or aj in                list(adj['AdjerlaubteZeichen'][30:45]):
                    pastRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
        elif x['Group'] == 5:
            for aj in cleanAdjList:
                if aj in list(adj['Adjektiv'][45:60]) or aj in                list(adj['AdjerlaubteZeichen'][45:60]):
                    otherRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negOtherRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralOtherRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][60:75]) or aj in                list(adj['AdjerlaubteZeichen'][60:75]):
                    presentRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1
                    
                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1

                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPresentRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPresentRightAns += 1
                            
                elif aj in list(adj['Adjektiv'][75:]) or aj in                list(adj['AdjerlaubteZeichen'][75:]):
                    pastRightAns += 1
                    try:
                        if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1
                            
                    except:
                        if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
                            posPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
                            negPastRightAns += 1

                        elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
                            neutralPastRightAns += 1

    numPresentRecal.append(presentRightAns)
    numPastRecal.append(pastRightAns)
    numOtherRecal.append(otherRightAns)

    numPosPresentRecal.append(posPresentRightAns)
    numPosPastRecal.append(posPastRightAns)
    numPosOtherRecal.append(posOtherRightAns)

    numNegPresentRecal.append(negPresentRightAns)
    numNegPastRecal.append(negPastRightAns)
    numNegOtherRecal.append(negOtherRightAns)

    numNeutralPresentRecal.append(neutralPresentRightAns)
    numNeutralPastRecal.append(neutralPastRightAns)
    numNeutralOtherRecal.append(neutralOtherRightAns)
    

# ans['num Present Recall'], ans['num Past Recall'], ans['num Other Recall'] = numPresentRecal,\
# numPastRecal, numOtherRecal
ans['Present Recall'], ans['Past Recall'], ans['Other Recall'] = numPresentRecal, numPastRecal, numOtherRecal




ans['Positive Present Recall'], ans['Positive Past Recall'],ans['Positive Other Recall'] = numPosPresentRecal,numPosPastRecal, numPosOtherRecal

ans['Neg Present Recall'], ans['Neg Past Recall'], ans['Neg Other Recall'] = numNegPresentRecal, numNegPastRecal,numNegOtherRecal

ans['Neutral Present Recall'], ans['Neutral Past Recall'], ans['Neutral Other Recall'] = numNeutralPresentRecal,numNeutralPastRecal, numNeutralOtherRecal


# ans['Present FPR'], ans['Past FPR'], ans['Other FPR'] = \
# 1 - ans['Present Recall rate'], 1 - ans['Past Recall rate'], 1 - ans['Other Recall rate']


# In[9]:


# # COMPUTING recall and FPR based on sentiment

# numPosRecal = []
# numNegRecal = []
# numNeutralRecal = []

# for i, x in ans.iterrows():
#     posRightAns = 0
#     negRightAns = 0
#     NeutralRightAns = 0
    
#     buf = x.iloc[12:57]
#     cleanAdjList = []
    
#     for zz in buf:
#         if type(zz) != type(np.nan):
#             if zz.strip() != '' and zz not in cleanAdjList:
#                 cleanAdjList.append(zz)

# #     cleanAdjList = list(set(cleanAdjList))
    
#     if x['Group'] == 1 or x['Group'] == 2 or x['Group'] == 3:
#         for aj in cleanAdjList:
#             if aj in list(adj['Adjektiv'][:45]) or aj in list(adj['AdjerlaubteZeichen'][:45]):
#                 try:
#                     if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
#                         negRightAns += 1
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
#                         posRightAns += 1
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
#                         NeutralRightAns += 1
#                 except:
#                     if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
#                         negRightAns += 1
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
#                         posRightAns += 1
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
#                         NeutralRightAns += 1
# #                     print(len(cleanAdjList), ans['correct Recall'][i], aj, i)
                    
    
#     elif x['Group'] == 4 or x['Group'] == 5 or x['Group'] == 6:
#         for aj in cleanAdjList:
#             if aj in list(adj['Adjektiv'][45:]) or aj in list(adj['AdjerlaubteZeichen'][45:]):
#                 try:
#                     if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
#                         negRightAns += 1
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
#                         posRightAns += 1
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
#                         NeutralRightAns += 1
#                 except:
#                     if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
#                         negRightAns += 1
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
#                         posRightAns += 1
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
#                         NeutralRightAns += 1
# #                     print(len(cleanAdjList), ans['correct Recall'][i], aj, i)
        
#     numPosRecal.append(posRightAns)
#     numNegRecal.append(negRightAns)
#     numNeutralRecal.append(NeutralRightAns)


# ans['Positive Recall'], ans['Neg Recall'], ans['Neutral Recall'] = \
# numPosRecal, numNegRecal, numNeutralRecal

# ans.iloc[:, 55:]


# In[10]:


# # COMPUTING recall and FPR based on sentiment

# numPosPresentRecal = []
# numPosPastRecal = []
# numPosOtherRecal = []

# numNegPresentRecal = []
# numNegPastRecal = []
# numNegOtherRecal = []

# numNeutralPresentRecal = []
# numNeutralPastRecal = []
# numNeutralOtherRecal = []


# for i, x in ans.iterrows():
#     posPresentRightAns = 0
#     posPastRightAns = 0
#     posOtherRightAns = 0
    
#     negPresentRightAns = 0
#     negPastRightAns = 0
#     negOtherRightAns = 0
    
#     neutralPresentRightAns = 0
#     neutralPastRightAns = 0
#     neutralOtherRightAns = 0
    
    
#     buf = x.iloc[12:57]
#     cleanAdjList = []
    
#     for zz in buf:
#         if type(zz) != type(np.nan):
#             if zz.strip() != '' and zz not in cleanAdjList:
#                 cleanAdjList.append(zz)
    
#     if x['Group'] == 1 or x['Group'] == 2 or x['Group'] == 3:
#         for aj in cleanAdjList:
#             if aj in list(adj['Adjektiv'][:45]) or aj in list(adj['AdjerlaubteZeichen'][:45]):
#                 try:
#                     if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
#                         if aj in list(adj['Adjektiv'][5:10]):
#                             posPresentRightAns += 1
#                         elif aj in list(adj['Adjektiv'][20:25]):
#                             posPastRightAns += 1
#                         elif aj in list(adj['Adjektiv'][35:40]):
#                             posOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
#                         if aj in list(adj['Adjektiv'][:5]):
#                             negPresentRightAns += 1
#                         elif aj in list(adj['Adjektiv'][15:20]):
#                             negPastRightAns += 1
#                         elif aj in list(adj['Adjektiv'][30:35]):
#                             negOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
#                         if aj in list(adj['Adjektiv'][10:15]):
#                             neutralPresentRightAns += 1
#                         elif aj in list(adj['Adjektiv'][25:30]):
#                             neutralPastRightAns += 1
#                         elif aj in list(adj['Adjektiv'][40:45]):
#                             neutralOtherRightAns += 1
#                 except:
#                     if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
#                         if aj in list(adj['AdjerlaubteZeichen'][5:10]):
#                             posPresentRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][20:25]):
#                             posPastRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][35:40]):
#                             posOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
#                         if aj in list(adj['AdjerlaubteZeichen'][:5]):
#                             negPresentRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][15:20]):
#                             negPastRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][30:35]):
#                             negOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
#                         if aj in list(adj['AdjerlaubteZeichen'][10:15]):
#                             neutralPresentRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][25:30]):
#                             neutralPastRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][40:45]):
#                             neutralOtherRightAns += 1

#     elif x['Group'] == 4 or x['Group'] == 5 or x['Group'] == 6:
#         for aj in cleanAdjList:
#             if aj in list(adj['Adjektiv'][45:]) or aj in list(adj['AdjerlaubteZeichen'][45:]):
#                 try:
#                     if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
#                         if aj in list(adj['Adjektiv'][50:55]):
#                             posPresentRightAns += 1
#                         elif aj in list(adj['Adjektiv'][65:70]):
#                             posPastRightAns += 1
#                         elif aj in list(adj['Adjektiv'][80:85]):
#                             posOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
#                         if aj in list(adj['Adjektiv'][45:50]):
#                             negPresentRightAns += 1
#                         elif aj in list(adj['Adjektiv'][60:65]):
#                             negPastRightAns += 1
#                         elif aj in list(adj['Adjektiv'][75:80]):
#                             negOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
#                         if aj in list(adj['Adjektiv'][55:60]):
#                             neutralPresentRightAns += 1
#                         elif aj in list(adj['Adjektiv'][70:75]):
#                             neutralPastRightAns += 1
#                         elif aj in list(adj['Adjektiv'][85:90]):
#                             neutralOtherRightAns += 1
#                 except:
#                     if adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 1:
#                         if aj in list(adj['AdjerlaubteZeichen'][50:55]):
#                             posPresentRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][65:70]):
#                             posPastRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][80:85]):
#                             posOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == -1:
#                         if aj in list(adj['AdjerlaubteZeichen'][45:50]):
#                             negPresentRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][60:65]):
#                             negPastRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][75:80]):
#                             negOtherRightAns += 1
                    
#                     elif adj.loc[adj[adj['AdjerlaubteZeichen'] == aj].index[0], 'Valenz'] == 0:
#                         if aj in list(adj['AdjerlaubteZeichen'][55:60]):
#                             neutralPresentRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][70:75]):
#                             neutralPastRightAns += 1
#                         elif aj in list(adj['AdjerlaubteZeichen'][85:90]):
#                             neutralOtherRightAns += 1
                    
#     numPosPresentRecal.append(posPresentRightAns)
#     numPosPastRecal.append(posPastRightAns)
#     numPosOtherRecal.append(posOtherRightAns)

#     numNegPresentRecal.append(negPresentRightAns)
#     numNegPastRecal.append(negPastRightAns)
#     numNegOtherRecal.append(negOtherRightAns)

#     numNeutralPresentRecal.append(neutralPresentRightAns)
#     numNeutralPastRecal.append(neutralPastRightAns)
#     numNeutralOtherRecal.append(neutralOtherRightAns)


# ans['Positive Present Recall'], ans['Positive Past Recall'],ans['Positive Other Recall'] = numPosPresentRecal,\
# numPosPastRecal, numPosOtherRecal

# ans['Neg Present Recall'], ans['Neg Past Recall'], ans['Neg Other Recall'] = numNegPresentRecal, numNegPastRecal,\
# numNegOtherRecal

# ans['Neutral Present Recall'], ans['Neutral Past Recall'], ans['Neutral Other Recall'] = numNeutralPresentRecal,\
# numNeutralPastRecal, numNeutralOtherRecal


# In[11]:


ans.iloc[:, 57:]


# In[12]:


ans.to_csv('Data Analysis.csv', index=False)


# In[ ]:




