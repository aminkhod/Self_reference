#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


adj = pd.read_csv('Adjectives_masterfile (4).csv', sep=';')
adj


# In[3]:


# ans = pd.read_csv('Tabelle1-Table 1.csv', sep=';')
ans = pd.read_csv('Tabelle1-Table 1.csv')
    
ans


# In[4]:


# lenght = 0
# for i in range(len(ans)):
#         if len(ans.iloc[i,:])> lenght:
#             lenght = len(ans.iloc[i,:])
# lenght


# ## Longest Common Subsequence

# In[5]:


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
  
    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]
  
    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]
# end of function lcs
  
# Driver program to test the above function
X = "AGGTAB"
Y = "GXTXAYB"
print("Length of LCS is ", lcs(X, Y))


# In[6]:


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


# In[7]:


len(adj['Adjektiv'][45:])


# In[8]:


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


# In[9]:


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


# In[10]:


ans.iloc[:, :]


# In[11]:


quas = pd.read_excel('Unipark 822.xlsx')
quas


# In[12]:


encod = pd.read_csv('EncodingAggregated (1).csv')
encod


# In[13]:


recalAnswer_Ecncoding = ans.merge(encod, left_on='Nosub', right_on='subj_counter_global', how="inner")


# In[14]:


recalAnswer_Ecncoding_questionnaire = recalAnswer_Ecncoding.merge(quas, left_on='VPCode', right_on='VPCode', how="inner")


# In[15]:


# Datenset = pd.read_csv('Datenset0406 (3) CSV.csv', sep=';')
# VPCode = Datenset['VPCode']
# Datenset = Datenset.iloc[:,8:17]
# Datenset['VPCode'] = VPCode


# In[16]:


# recalAnswer_Ecncoding_questionnaire = recalAnswer_Ecncoding_questionnaire.merge(Datenset, left_on='VPCode',
#                                                                                 right_on='VPCode', how="inner")


# In[17]:


"""this method is only for help and evaluates the output depending on whether the data
 needs to be turned over or not"""
def evaluate_psychological(i, colums, name, dataset, teilen):
    if teilen :
        sum = 0
        for j in colums:
            if int(colums.__getitem__(j)) == 0:
               # has not to be inverted
               sum += int(dataset[j][i])

            elif int(colums.__getitem__(j)) == 1:
                # has to be inverted
                value = int(dataset[j][i])
                if value == 1:
                    sum += 6
                elif value == 2:
                    sum += 5
                elif value == 3:
                    sum += 4
                elif value == 4:
                    sum += 3
                elif value == 5:
                    sum += 2
                elif value == 6:
                    sum += 1

        sum = sum / colums.__len__()
        dataset[name][i] = sum.__round__(2)

       # dataset.insert(i, name, sum)
    else:
        sum = 0
        for j in colums:
            if int(colums.__getitem__(j)) == 0:
               # has not to be inverted
               sum += int(dataset[j][i])

            elif int(colums.__getitem__(j)) == 1:
                # has to be inverted
                value = int(dataset[j][i])
                if value == 1:
                    sum += 6
                elif value == 2:
                    sum += 5
                elif value == 3:
                    sum += 4
                elif value == 4:
                    sum += 3
                elif value == 5:
                    sum += 2
                elif value == 6:
                    sum += 1

        return sum


# In[18]:


############################################### Unipark data evaluation###################################
##########################################################################################################
##########################################################################################################

"""this method inserts values such as KW, PW mean value, ... into the Unipark data table a"""
print("start  insert_psychological_wellbeing")

dataset = recalAnswer_Ecncoding_questionnaire.copy()

count_rows = dataset.shape[0]

column_names = ['K_Mittelwert', 'PW_Mittelwert', 'SL_Mittelwert', 'A_Mittelwert', 'SA_Mittelwert',
                'PB_Mittelwert', 'PWB_Mittelwert']
for i in column_names:
    dataset[i] = 0.00

K = {  'v_27': 0,
        'v_32': 1,
        'v_37': 1,
        'v_42': 0,
        'v_45': 1,
        'v_54': 0,
        'v_61': 0,
        'v_74': 1,
        'v_78': 0
        }

Pw = {  'v_28': 1,
        'v_43': 1,
        'v_46': 0,
        'v_51': 1,
        'v_62': 0,
        'v_66': 1,
        'v_75': 1,
        'v_79': 1
        }

SL = {  'v_33': 1,
        'v_38': 1,
        'v_47': 1,
        'v_52': 1,
        'v_55': 1,
        'v_58': 0,
        'v_63': 0,
        'v_67': 0,
        'v_71': 1
        }

A = {  'v_31': 0,
        'v_36': 0,
        'v_41': 1,
        'v_44': 0,
        'v_50': 1,
        'v_60': 0,
        'v_65': 1,
        'v_69': 1,
        'v_77': 0
        }

SA = {  'v_29': 0,
        'v_34': 0,
        'v_39': 1,
        'v_48': 0,
        'v_53': 0,
        'v_56': 1,
        'v_68': 1,
        'v_70': 0,
        'v_73': 0,
        'v_76': 0
        }

Pb = {  'v_26': 0,
        'v_30': 1,
        'v_35': 1,
        'v_40': 0,
        'v_49': 1,
        'v_57': 1,
        'v_59': 0,
        'v_64': 1,
        'v_72': 0
        }

for i in range(0, count_rows):
    evaluate_psychological(i, K, 'K_Mittelwert', dataset, True)
    evaluate_psychological(i, Pw, 'PW_Mittelwert', dataset, True)
    evaluate_psychological(i, SL, 'SL_Mittelwert', dataset, True)
    evaluate_psychological(i, A, 'A_Mittelwert', dataset, True)
    evaluate_psychological(i, SA, 'SA_Mittelwert', dataset, True)
    evaluate_psychological(i, Pb, 'PB_Mittelwert', dataset, True)

    dataset['PWB_Mittelwert'][i] = (evaluate_psychological(i, K, 'K_Mittelwert', dataset, False) +                                    evaluate_psychological(i, K, 'PW_Mittelwert', dataset, False)                                   + evaluate_psychological(i, K, 'SL_Mittelwert', dataset, False) +                                    evaluate_psychological(i, K, 'A_Mittelwert', dataset, False)                                    + evaluate_psychological(i, K, 'SA_Mittelwert', dataset, False) +                                     evaluate_psychological(i, K, 'PB_Mittelwert', dataset, False)) / 54
dataset


# In[19]:


"""that method evaluates self_esteem"""

print("start  self_esteem")
count_rows = dataset.shape[0]
dataset['self_esteem'] = 0
se = {  'v_80': 0,
        'v_81': 1,
        'v_82': 0,
        'v_83': 0,
        'v_84': 1,
        'v_85': 1,
        'v_86': 0,
        'v_87': 1,
        'v_88': 1,
        'v_89': 0
        }
for i in range(count_rows):
    sum = 0
    for j in se:
        if int(se.__getitem__(j)) == 0:
            # has not to be inverted
            sum += int(dataset[j][i])

        elif int(se.__getitem__(j)) == 1:
            # has to be inverted
            value = int(dataset[j][i])
            if value == 1:
                sum += 4
            elif value == 2:
                sum += 3
            elif value == 3:
                sum += 2
            elif value == 4:
                sum += 1

    dataset['self_esteem'][i] = sum.__round__(2)


# In[20]:



"""that method evaluates psycologic_wellbeing"""

pd.set_option('mode.chained_assignment', None)
pd.set_option('mode.chained_assignment', None)

print("start  social_psycologic_wellbeing")
sum = 0
count_rows = dataset.shape[0]
dataset['social_psycologic_wellbeing'] = 0
se = ['v_90', 'v_91', 'v_92', 'v_93', 'v_94', 'v_95', 'v_96', 'v_97']
for i in range(count_rows):
    sum = 0
    for j in se:
        sum += int(dataset[j][i])

    dataset['social_psycologic_wellbeing'][i] = sum
dataset


# In[21]:


dataset.to_csv('recalAnswer_Ecncoding_questionnaire.csv', index=False, sep=';',
               float_format='%.3f', decimal='.', header=True)


# In[ ]:




