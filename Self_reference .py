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


recalAnswer_Ecncoding_questionnaire.to_csv('Data integration.csv', index=False)


# In[ ]:




