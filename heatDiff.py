#Code By: Nicholas Tidwell
#FSUID: nbt16b
#02/08/2020
import matplotlib.pyplot as plt
import numpy as np
import time

#get input
initialTemp = int(input("Enter starting temp: "))
startTime = time.time()

#Create array of zeroes
currentTempGrid = np.zeros((initialTemp + 2,initialTemp + 2), dtype=np.float)
colors = np.array(['darkblue', 'blue', 'aqua', 'lawngreen', 'yellow', 'orange', 'red', 'darkred'])

#initial first row to initial temp
currentTempGrid[:,0] = initialTemp

#make copy of grid
prevTempGrid = np.copy(currentTempGrid)

#Use given equation
def heatMapNextValue():
    for i in range(1,currentTempGrid.shape[0]-1):
        for j in range(1,currentTempGrid.shape[1]-1):
            currentTempGrid[i][j] = (prevTempGrid[i-1][j] + prevTempGrid[i+1][j] + prevTempGrid[i][j-1] + prevTempGrid[i][j+1])/4

def getColor(heatVal):
    colorRangesStep = initialTemp / 8

    multiplier = 1
    while heatVal > colorRangesStep * multiplier:
        multiplier = multiplier + 1
    return colors[multiplier-1]

heatMapNextValue()
maxSteps = 0
while(not(np.array_equal(currentTempGrid, prevTempGrid)) and maxSteps != 3000):
    prevTempGrid = np.copy(currentTempGrid)
    heatMapNextValue()
    maxSteps = maxSteps + 1


for i in range(1,currentTempGrid.shape[0]-1):
    for j in range(1,currentTempGrid.shape[1]-1):
        plt.scatter(j,i, c=getColor(currentTempGrid[i][j]))

endTime = time.time()
print(endTime-startTime)
plt.show()


