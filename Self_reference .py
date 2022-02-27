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
    
    
    
    if x['Group'] == 1 or x['Group'] == 2 or x['Group'] == 3:
        for j in clean:
            if j in list(adj['Adjektiv'][:45]) or j in list(adj['AdjerlaubteZeichen'][:45]):
                rightAns += 1
            else:
                falseAns += 1

    elif x['Group'] == 4 or x['Group'] == 5 or x['Group'] == 6:
        for j in clean:
            if j in list(adj['Adjektiv'][45:]) or j in list(adj['AdjerlaubteZeichen'][45:]):
                rightAns += 1
            else:
                falseAns += 1
    if i ==11:
        print(len(clean), rightAns, falseAns)
        print(clean)
    numRightAns.append(rightAns)
    numFalseAns.append(falseAns)
    
ans['number of correct answer'] = numRightAns
ans['number of False answer'] = numFalseAns


# In[6]:


# recall rate computing
ans['Doppelt'] = ans['Doppelt'].fillna(0)
correctRecallRate = []
for i in range(len(numRightAns)):
    try:
        correctRecallRate.append(numRightAns[i] / (numFalseAns[i] + numRightAns[i]))
    except:
        correctRecallRate.append(np.nan)
        
ans['correct Recall rate']  = correctRecallRate

# False recall rate
ans['False recall rate'] = 1 - ans['correct Recall rate']
ans['correct Recall rate'] = ans['correct Recall rate'].fillna(0)
ans['False recall rate'] = ans['False recall rate'].fillna(0)
ans.iloc[:,10:]


# In[7]:


# COMPUTING recall and FPR based on tense and group 
# numRightAns = []
numPresentRecal = []
numPastRecal = []
numOtherRecal = []

for i, x in ans.iterrows():
    presentRightAns = 0
    pastRightAns = 0
    otherRightAns = 0

##group of 1 & 4

    if x['Group'] == 1 or x['Group'] == 4:
        if x['Group'] == 1:
            for j in range(12, 57):
                if x.iloc[j] in list(adj['Adjektiv'][:15]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][:15]):
                    presentRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][15:30]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][15:30]):
                    pastRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][30:45]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][30:45]):
                    otherRightAns += 1
        elif x['Group'] == 4:
            for j in range(12, 57):
                if x.iloc[j] in list(adj['Adjektiv'][45:60]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][45:60]):
                    presentRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][60:75]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][60:75]):
                    pastRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][75:]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][75:]):
                    otherRightAns += 1
                    
#group of 3 & 6

    elif x['Group'] == 3 or x['Group'] == 6:
        if x['Group'] == 3:
            for j in range(12, 57):
                if x.iloc[j] in list(adj['Adjektiv'][:15]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][:15]):
                    pastRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][15:30]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][15:30]):
                    otherRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][30:45]) or x.iloc[j] in                 list(adj['AdjerlaubteZeichen'][30:45]):
                    presentRightAns += 1
        elif x['Group'] == 6:
            for j in range(12, 57):
                if x.iloc[j] in list(adj['Adjektiv'][45:60]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][45:60]):
                    pastRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][60:75]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][60:75]):
                    otherRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][75:]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][75:]):
                    presentRightAns += 1


#group of 2 & 5

    elif x['Group'] == 2 or x['Group'] == 5:
        if x['Group'] == 2:
            for j in range(12, 57):
                if x.iloc[j] in list(adj['Adjektiv'][:15]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][:15]):
                    otherRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][15:30]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][15:30]):
                    presentRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][30:45]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][30:45]):
                    pastRightAns += 1
        elif x['Group'] == 5:
            for j in range(12, 57):
                if x.iloc[j] in list(adj['Adjektiv'][45:60]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][45:60]):
                    otherRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][60:75]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][60:75]):
                    presentRightAns += 1
                elif x.iloc[j] in list(adj['Adjektiv'][75:]) or x.iloc[j] in                list(adj['AdjerlaubteZeichen'][75:]):
                    pastRightAns += 1

    numPresentRecal.append(presentRightAns)
    numPastRecal.append(pastRightAns)
    numOtherRecal.append(otherRightAns)

# ans['num Present Recall'], ans['num Past Recall'], ans['num Other Recall'] = numPresentRecal,\
# numPastRecal, numOtherRecal
ans['Present Recall rate'], ans['Past Recall rate'], ans['Other Recall rate'] = [z/15 for z in numPresentRecal], [z/15 for z in numPastRecal], [z/15 for z in numOtherRecal]

ans['Present FPR'], ans['Past FPR'], ans['Other FPR'] = 1 - ans['Present Recall rate'], 1 - ans['Past Recall rate'], 1 - ans['Other Recall rate']


# In[16]:


# COMPUTING recall and FPR based on sentiment

numPosRecal = []
numNegRecal = []
numNeutralRecal = []

for i, x in ans.iterrows():
    posRightAns = 0
    negRightAns = 0
    NeutralRightAns = 0
    buf = x.iloc[12:57]
    cleanAdjList = []
    
    for zz in buf:
        if type(zz) != type(np.nan):
            if zz.strip() != '' and zz not in clean:
                cleanAdjList.append(zz)
                
    if x['Group'] == 1 or x['Group'] == 2 or x['Group'] == 3:
        for aj in cleanAdjList:
            if aj in list(adj['Adjektiv'][:45]) or aj in list(adj['AdjerlaubteZeichen'][:45]):
                try:
                    if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                        negRightAns += 1
                    elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                        posRightAns += 1
                    elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                        NeutralRightAns += 1
                except:
                    1+1 

    elif x['Group'] == 4 or x['Group'] == 5 or x['Group'] == 6:
        for aj in cleanAdjList:
            if aj in list(adj['Adjektiv'][45:]) or aj in list(adj['AdjerlaubteZeichen'][45:]):
                try:
                    if adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == -1:
                        negRightAns += 1
                    elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 1:
                        posRightAns += 1
                    elif adj.loc[adj[adj['Adjektiv'] == aj].index[0], 'Valenz'] == 0:
                        NeutralRightAns += 1
                except:
                    1+1  
    numPosRecal.append(posRightAns)
    numNegRecal.append(negRightAns)
    numNeutralRecal.append(NeutralRightAns)


ans['Positive Recall'], ans['Neg Recall'], ans['Neutral Recalkl'] = numPosRecal, numNegRecal, numNeutralRecal


# In[17]:


ans.iloc[:, 57:]


# In[19]:


ans.to_csv('Data Analysis.csv', index=False)


# In[ ]:




