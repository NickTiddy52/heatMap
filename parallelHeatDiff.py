#Code By: Nicholas Tidwell
#FSUID: nbt16b
#02/08/2020
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import multiprocessing as mp
import time
colors = ['darkblue', 'blue', 'aqua', 'lawngreen', 'yellow', 'orange', 'red', 'darkred']


def main():
    # get input
    initialTemp = int(input("Enter starting temp: "))
    startTime = time.time()

    # Create array of zeroes
    currentTempGrid = np.zeros((initialTemp + 2, initialTemp + 2), dtype=np.float)
    # initial first row to initial temp
    currentTempGrid[:, 0] = initialTemp
    # make copy of grid
    prevTempGrid = np.copy(currentTempGrid)
    #Create Pool Of Proccess
    pool = mp.Pool(processes=mp.cpu_count())

    #Asynchronous Way of getting each new row
    results = [pool.apply_async(nextHeatVal, args=(x,prevTempGrid, currentTempGrid)) for x in range(0, currentTempGrid.shape[0]-2)]
    #Apply results to master Grid
    currentTempGrid = joinColumns(results, currentTempGrid)

    maxSteps = 0
    #Find Convergence
    while not (np.array_equal(currentTempGrid, prevTempGrid)) and maxSteps != 3000:
        prevTempGrid = np.copy(currentTempGrid)
        results = [pool.apply_async(nextHeatVal, args=(x, prevTempGrid, currentTempGrid)) for x in range(0, currentTempGrid.shape[0]-2)]
        currentTempGrid = joinColumns(results, currentTempGrid)
        maxSteps = maxSteps + 1

    #Plot Graph
    for i in range(1, currentTempGrid.shape[0] - 1):
        for j in range(1, currentTempGrid.shape[1] - 1):
            plt.scatter(j, i, c=getColor(currentTempGrid[i][j], initialTemp))

    endTime = time.time()
    print("Time to run: " + str(endTime - startTime))
    plt.show()


def joinColumns(results, grid):
    output = [p.get() for p in results]
    output = np.transpose(output)
    grid[:,1:-1] = output
    return grid

def getColor(heatVal, initialTemp):
    colorRangesStep = initialTemp / 8
    multiplier = 1
    while heatVal > colorRangesStep * multiplier:
        multiplier = multiplier + 1
    return colors[multiplier - 1]

def nextHeatVal(chunkStart, prevTempGrid, currentTempGrid):
    chunk = prevTempGrid[:, chunkStart:chunkStart + 3]
    for i in range(1, chunk.shape[0] - 1):
        currentTempGrid[i][1 + chunkStart] = (chunk[i - 1][1] + chunk[i + 1][1] + chunk[i][0] + chunk[i][2]) / 4
    return currentTempGrid[:, 1 + chunkStart]

if __name__ == '__main__':
    main()
