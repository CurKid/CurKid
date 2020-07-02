import pandas as pd
import numpy as np
import random

# Create initial population elements
## Default of placing 8 queens in a 8 X 8 board
queensCount = 8   ## number of queens and chess Matrix
nCount = 1000  ## n Population count


## Creating elements for Population
def createElements():
    pop = pd.DataFrame(initArr.loc[random.randint(0,queensCount - 1)] for _ in range(queensCount)).reset_index(drop = True) 
    return pop

	
## Generate Population of n 
def genPopulation():
    for i in range(nCount):
        nPop.append(createElements()) 
    return(nPop)

# Function to score based on the numbers at column level
def scoreColumn(nPop,score):
    for n in range(nCount):
        tmpScore = 0
        for q in range(queensCount):            
            tmpScore = tmpScore + (nPop[n][q].sum() ** 3)
        score.loc[n][1] = tmpScore


# Function to score based on the numbers at diagonal - left to right

# Function to cal score for l to R diag from low to high pos 
def scoreLtoRDiagUp(nPop,score):
    for n in range(nCount):
        for q in range(queensCount-1, -1, -1):            
            tmpScore = 0
            for r in range(0 , queensCount-q):
                tmpScore = tmpScore + nPop[n][r][q]
                q += 1
            score.loc[n][2] = score.loc[n][2] + (tmpScore ** 3)

# Function to cal score for l to R diag from high to low pos 
def scoreLtoRDiagDown(nPop,score):
    for n in range(nCount):
        for q in range(1, queensCount):            
            tmpScore = 0
            for r in range(0 , queensCount-q):
                tmpScore = tmpScore + nPop[n][q][r]
                q += 1
            score.loc[n][2] = score.loc[n][2] + (tmpScore ** 3)               

            
def scoreLtoRDiag(nPop,score):
    scoreLtoRDiagUp(nPop,score)
    scoreLtoRDiagDown(nPop,score)
    


# Function to score based on the numbers at diagonal - right to left

# Function to cal score for R to L diag from low to high pos 
def scoreRtoLDiagUp(nPop,score):
    for n in range(nCount):
        for q in range(queensCount-1, -1, -1):            
            tmpScore = 0
            for r in range(queensCount-1,q-1, -1):
                tmpScore = tmpScore + nPop[n][q][r]
                q += 1
            score.loc[n][3] = score.loc[n][3] + (tmpScore ** 3)

            
## Function to cal score for R to L diag from high to low pos 
def scoreRtoLDiagDown(nPop,score):
    for n in range(nCount):
        for q in range(0, queensCount-1):            
            tmpScore = 0
            for r in range(0 ,q+1):
                tmpScore = tmpScore + nPop[n][q][r]
                q -= 1
            score.loc[n][3] = score.loc[n][3] + (tmpScore ** 3)               

            
def scoreRtoLDiag(nPop,score):
    scoreRtoLDiagUp(nPop,score)
    scoreRtoLDiagDown(nPop,score)
    

## update total score per population
def updateTotal(score):
    for n in range(nCount):
        score.loc[n][4] = score.loc[n][1:4].sum()

## function to identify if we have a winner
def checkWinners(score):
    chk1 = score [score[1]==queensCount ]
    if len(chk1) > 0:
        chk2 = chk1 [chk1[2] == queensCount ]
        if len(chk2) > 0:
            chk3 = chk2 [chk2[3] == queensCount ]
            if len(chk3) > 0:
                chk4 = list(chk3.index)
                chk5 = list(score[0][chk4])
                winners = chk5
                print(" count of winners -- " + str(len(winners)))
                print(winners)
                return winners


## Filter for parents
def filterParents(score):
    idx = score.sort_values(by = [4]).head(round(nCount / 2)).index.tolist()
    parents = [nPop[i] for i in idx]
    return parents


## Create Crossover
## trying Single-point crossover
def createOffsprings(parents):
    a = round(queensCount / 2)
    b = queensCount - a
    p = 0
    while p <= (len(parents) - 1):
        c1 = pd.concat([parents[p][:a], parents[p+1][a:]])
        c2 = pd.concat([parents[p+1][:a], parents[p][a:]])
        child.append(c1)
        child.append(c2)
        p += 2
    return child


## function to combine Parents and Offsprings
def createNewPop(nextPop,parents, child):
    for p in parents:
        nextPop.append(p)
    for c in child:
        nextPop.append(c)
    
    return nextPop
    

## Evaluate and rate each of n population

def evaluate(nPop,score):
    
    # Call Function to score based on the numbers at column level
    scoreColumn(nPop,score)

    #Call Function to score based on the numbers at diagonal - left to right
    scoreLtoRDiag(nPop,score)

    #Call Function to score based on the numbers at diagonal - right to left
    scoreRtoLDiag(nPop,score)

    ## Call function to update totals in Score df
    updateTotal(score)        

    return score


### Create a dataframe of size q X q 
initArr = []
initArr = pd.DataFrame(np.identity(queensCount, dtype = int))

### Generate a population of n elements
global nPop
nPop = []
nextPop = []
nPop = genPopulation()
#print(nPop)
result = "None"
execIter = 1
parents = []
child = []
global winners
winners = []
# initializing a nparray to store the scores for population
# stored for every population as [df index, column score , ltor diag , r to l diag, total]
global score
score = pd.DataFrame(np.zeros((nCount,5), dtype = int))
score[0] = range(nCount)

while result == "None":
    print("Executing iteration : " + str(execIter))
    # If no winner so far, continue
    score = pd.DataFrame(np.zeros((nCount,5), dtype = int))
    score[0] = range(nCount)

    # evaluate the population
    score = evaluate(nPop,score)
    print ("Evaluation completed  "  + str(execIter))
    
    # Check to see if we have a winner
    wins = []
    wins = checkWinners(score)
    if wins != None:
        result = "Great"
        winnerCount = len(wins)
        print(" Number of winners are : " + str(len(wins)) )
        print("The winners are : ********** ")
        winners = [nPop[i] for i in wins]
        print(winners)
        print(" Expected result below ****")
        w = wins[0]
        ans = []
        for i in nPop[w]:
            for j in range(len(nPop[w][i])):
                if nPop[w][i][j] == 1:
                    ans.append(j)
        print(ans)
        break
    print ("Winner check completed  "  + str(execIter))


    # identify elements that can be considered as parents
    parents = filterParents(score)

    # Create child aka Offsprings 
    child = []
    child = createOffsprings(parents)
    
    # Create new set of Population    
    nextPop = []
    nextPop = createNewPop(nextPop,parents, child)
    nPop = nextPop
    print("length of nextPop is : " + str(len(nPop)) + " -- " + str(len(nextPop)))

    print("Next Iteration Populated   "  + str(execIter))

    execIter += 1
    	
