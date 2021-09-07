## PIP Requirements
## matplotlib
## serial
## tkinter

## Importing pip libraries
import matplotlib.pyplot as pyplot
import threading
import sys
from time import sleep, time
import serial
import tkinter as tk

## Data from serial is in format: WaterDepth : WaterTemp : AirTemp : tdsValue

## Length of data lists
dataSizeMax = 30

## Global variable used for daemon threads to tell main loop to close program
runMain = True
waterDepth = []
waterTemperature = []
airTemperature = []
tdsValue = []
timeData = []

class serialProcessor():
    def __init__(self):
        self.floatContents = []
        for i in range(0, 10): self.floatContents.append(str(i))
        self.floatContents.append(".")
        global waterDepth
        global waterTemperature
        global airTemperature
        global tdsValue
        global timeData

    def process(self, serialData, timeReceived):
        ## Convert from bytes to string
        serialData = str(serialData)
        ## Obtain numbers from the string
        self.extractedData = self.extractSerialNumbers(serialData)
        ## Ignore the data if we didn't get 4 numbers
        if ( len(self.extractedData) != 4 ):
            return
        waterDepth.append(self.extractedData[0])
        waterTemperature.append(self.extractedData[1])
        airTemperature.append(self.extractedData[2])
        tdsValue.append(self.extractedData[3])
        timeData.append(timeReceived)
        print("dataHandling :: Filled " + str(len(timeData)) + "/" + str(dataSizeMax) + " of allocated space")
        while (len(timeData) >= dataSizeMax):
            waterDepth.pop(0)
            waterTemperature.pop(0)
            airTemperature.pop(0)
            tdsValue.pop(0)
            timeData.pop(0)

    
    def extractSerialNumbers(self, serialData):
        ## Create a list to save found numbers
        returnNumbers = []
        startIndex = 0
        for index in range(0, len(serialData)):
            if ( not (serialData[index] in self.floatContents)):
                if (startIndex == index):
                    startIndex += 1
                else:
                    returnNumbers.append(float(serialData[startIndex:index]))
                    startIndex = index + 1
        return returnNumbers

def serialThread():

    ## Create serialProcessor object
    serialManager = serialProcessor()

    ## This loop continually tries to open a port to listen to the uC
    while (True):

        ## Try ttyACM0
        try:
            serialObj = serial.Serial("/dev/ttyACM0")
            print("serialThread :: Opened port /dev/ttyACM0")
            break
        except:
            print("serialThread :: Couldn't start on port /dev/ttyACM0")

        ## Try ttyACM1
        try:
            serialObj = serial.Serial("/dev/ttyACM1")
            print("serialThread :: Opened port /dev/ttyACM1")
            break
        except:
            print("serialThread :: Couldn't start on port /dev/ttyACM1")
        
        print("Couldn't open port. Waiting to retry")
        sleep(1)

    ## This loop reads data from serial and sends it to a serial processing object
    while (True):
        ## Read from serial, readline() waits until a full line has been printed
        serialInput = serialObj.readline()
        currentTime = time()
        print("serialThread :: Received data from serial -> " + str(serialInput))
        serialManager.process(serialInput, currentTime)

class graphManagerClass():
    def __init__(self, initialSetting):
        self.initialisedSetting = initialSetting
        global waterDepth
        global waterTemperature
        global airTemperature
        global tdsValue
        global timeData
        pyplot.figure("Condensed Farming Data Analysis")

    def isRunnning(self):
        return pyplot.fignum_exists(1)

    def graph(self, settingNumber):
        if (settingNumber != self.initialisedSetting):
            pyplot.clf()
            self.initialisedSetting = settingNumber
        self.updateGraph(settingNumber)

    def updateGraph(self, settingNumber):
        global dataHandler
        if (settingNumber == 0): ## All 4 graphs
            ## --- "Data 1" ---
            ## Select graph 1 in a 2 by 2 subplot
            pyplot.subplot(221)
            ## Clear anything already on that subplot
            pyplot.cla()
            ## Label axis and title the plot
            pyplot.title("Water Depth")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Depth (cm)")
            ## Plot data to the subplot
            pyplot.plot(timeData, waterDepth)
            # Repeat for the rest of the data
            ## --- "Data 2" --- 
            pyplot.subplot(222)
            pyplot.cla()
            pyplot.title("Water Temperature")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Temperature (Degrees C)")
            pyplot.title("Water Temperature")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Temperature (Degrees C)")
            pyplot.plot(timeData, waterTemperature)
            ##--- Data 3 ---
            pyplot.subplot(223)
            pyplot.cla()
            pyplot.title("Total Dissolved Solids")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("TDS (Parts Per Million)")
            pyplot.title("Air Temperature")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Temperature (Degrees C)")
            pyplot.plot(timeData, airTemperature)
            ## --- Data 4 ---
            pyplot.subplot(224)
            pyplot.cla()
            pyplot.title("Total Dissolved Solids")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("TDS (Parts Per Million)")
            pyplot.plot(timeData, tdsValue)
        elif (graphSetting == 1): ## Water Depth
            pyplot.subplot(111)
            pyplot.cla()
            pyplot.title("Water Depth")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Water Depth (cm)")
            pyplot.plot(timeData, waterDepth)
        elif (graphSetting == 2): ## Water Temperature
            pyplot.subplot(111)
            pyplot.cla()
            pyplot.title("Water Temperature")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Temperature (Degrees C)")
            pyplot.plot(timeData, waterTemperature)
        elif (graphSetting == 3): ## Air Temperature
            pyplot.subplot(111)
            pyplot.cla()
            pyplot.title("Air Temperature")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("Air Temperature (Degrees C)")
            pyplot.plot(timeData, airTemperature)
        elif (graphSetting == 4): ## tds Value
            pyplot.subplot(111)
            pyplot.cla()
            pyplot.title("Total Dissolved Soilds")
            pyplot.xlabel("Time (s)")
            pyplot.ylabel("TDS (Parts Per Million)")
            pyplot.plot(timeData, waterTemperature)
        elif (graphSetting == 5): ## Mixed
            pyplot.subplot(111)
            pyplot.cla()
            pyplot.title("All Data")
            pyplot.xlabel("Time (s)")
            pyplot.plot(timeData, waterDepth)
            pyplot.plot(timeData, waterTemperature)
            pyplot.plot(timeData, airTemperature)
            pyplot.plot(timeData, tdsValue)
            pyplot.legend(["Water Depth", "Water Temperature", "Air Temperature", "Air Temperature"])
        else:
            print("graphManager :: Invalid value for graphSetting")
        pyplot.pause(0.01)

class guiThread():
    def __init__(self):
        global graphSetting
        # self.checkRunningPeriod = 1000 # ms
        backgroundColor = "VioletRed1"
        ## Top Frame
        self.root = tk.Tk()
        self.root.title("Condensed Farming")
        self.mainFrame = tk.Frame(self.root, bg = backgroundColor)
        self.mainFrame.pack()
        self.topFrame = tk.Frame(self.mainFrame, bg = backgroundColor)
        self.topFrame.pack(side = tk.TOP)
        self.stopButtonImage = tk.PhotoImage(file = "JD.png")
        self.stopButtonImage = self.stopButtonImage.subsample(5, 5)
        self.stopButton = tk.Button(self.topFrame, image = self.stopButtonImage, command = self.stopAll)
        self.stopButton.pack(side = tk.LEFT)
        ## Bottom Frame
        self.bottomFrame = tk.Frame(self.mainFrame, bg = "gray80")
        self.bottomFrame.pack(side = tk.TOP, fill = tk.X)
        self.dataSizeScale = tk.Scale(self.bottomFrame, label = "Number of data points", command = self.setDataSize, from_ = 1, to = 1000, length = 300, orient = tk.HORIZONTAL, borderwidth = 0.01, highlightthickness = 0, bg = "gray80", troughcolor = "red2")
        global dataSizeMax
        self.dataSizeScale.set(dataSizeMax)
        self.dataSizeScale.pack()
        ## Radio Button stuff
        self.buttonSelected = tk.IntVar()
        radioButtonBGColor = backgroundColor
        tk.Radiobutton(self.topFrame, variable = self.buttonSelected, value = 0, text = "All graphs", command = self.setGraph0, bg = radioButtonBGColor, borderwidth = 0, highlightthickness = 0).pack(anchor = tk.W)
        tk.Radiobutton(self.topFrame, variable = self.buttonSelected, value = 1, text = "Water Depth", command = self.setGraph1, bg = radioButtonBGColor, borderwidth = 0, highlightthickness = 0).pack(anchor = tk.W)
        tk.Radiobutton(self.topFrame, variable = self.buttonSelected, value = 2, text = "Water Temperature", command = self.setGraph2, bg = radioButtonBGColor, borderwidth = 0, highlightthickness = 0).pack(anchor = tk.W)
        tk.Radiobutton(self.topFrame, variable = self.buttonSelected, value = 3, text = "Air Temperature", command = self.setGraph3, bg = radioButtonBGColor, borderwidth = 0, highlightthickness = 0).pack(anchor = tk.W)
        tk.Radiobutton(self.topFrame, variable = self.buttonSelected, value = 4, text = "TDS Value", command = self.setGraph4, bg = radioButtonBGColor, borderwidth = 0, highlightthickness = 0).pack(anchor = tk.W)
        tk.Radiobutton(self.topFrame, variable = self.buttonSelected, value = 5, text = "All On One Graph", command = self.setGraph5, bg = radioButtonBGColor, borderwidth = 0, highlightthickness = 0).pack(anchor = tk.W)

        # Check if the program is running every 1000 ms
        # self.root.after(self.checkRunningPeriod, self.checkRunning)
        
        self.root.resizable(width = False, height = False)
        self.root.mainloop()

    def setGraph0(self):
        global graphSetting
        graphSetting = 0

    def setGraph1(self):
        global graphSetting
        graphSetting = 1

    def setGraph2(self):
        global graphSetting
        graphSetting = 2

    def setGraph3(self):
        global graphSetting
        graphSetting = 3

    def setGraph4(self):
        global graphSetting
        graphSetting = 4

    def setGraph5(self):
        global graphSetting
        graphSetting = 5

    def setDataSize(self, scaleValue):
        global dataSizeMax
        dataSizeMax = int(scaleValue)

    def stopAll(self):
        # global runSerial
        global runMain
        # runPlotter = False
        self.root.destroy()
        # runSerial = False
        runMain = False
    # def checkRunning(self):
    #     if (runGui == False):
    #         print("guiThread :: runGui is False")
    #         self.root.destroy()
    #     else:
    #         self.root.after(self.checkRunningPeriod, self.checkRunning)

graphManager = graphManagerClass(0)

## Used to remember which layout the graphs should be in
graphSetting = 0

def main():
    ## Allow main loop to see function elsewhere in the python script
    global guiThread
    global serialThread
    global graphSetting

    ## Create daemon threads for tkinter gui and serial threading
    guiThread = threading.Thread(target = guiThread, daemon = True)
    guiThread.start()

    serialThread = threading.Thread(target = serialThread, daemon = True)
    serialThread.start()

    ## Wait a second for threads to start
    sleep(1)

    while (True):
        
        graphManager.graph(graphSetting) ## Graph with setting 0 (All 4 graphs)

        ## Check if main should be closed
        if (runMain == False):
            sys.exit()
        ## Check if serialThread is still alive, close program if it is not
        elif (serialThread.is_alive() == False):
            print("serialThread :: Caused program to fail")
            print("mainThread :: Closing main thread")
            sys.exit()
        ## Check if guiThread is still alive, close program if not
        elif (guiThread.is_alive() == False):
            print("mainThread :: guiThread closed, closing main thread")
            sys.exit()

if __name__ == "__main__":
    main()