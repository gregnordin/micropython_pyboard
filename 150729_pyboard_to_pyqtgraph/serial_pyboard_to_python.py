#HV Control &
#Read and Plot from the PMT

#This code is to record the data that is received into the Teensy's ADC. 
#Includes the HV control and replotting the results at the end.

#See CSV Dataplot notebook to plot old experiment data.

from __future__ import division
from __future__ import print_function
from pyqtgraph import QtGui, QtCore #Provides usage of PyQt4's libraries which aids in UI design
import pyqtgraph as pg              #Initiation of plotting code
import serial                       #Communication with the serial port is done using the pySerial 2.7 package
from datetime import datetime       #Allows us to look at current date and time
#import dataprocessing               #code for plotting the data from the CSV

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything (a window)
w = QtGui.QWidget()
w.resize(1000,600)
w.setWindowTitle('Voltage Plots')

startBtnClicked = False
quitBtnClicked = False
firstupdate = 0

## This function contains the behavior we want to see when the start button is clicked
def startButtonClicked():
    global startBtnClicked
    global startBtn
    if (startBtnClicked == False):
        teensySerialData.flushInput() #empty serial buffer for input from the teensy
        startBtnClicked = True
        startBtn.setText('Stop')
            
    elif (startBtnClicked == True):
        startBtnClicked = False
        startBtn.setText('Start')

## Below at the end of the update function we check the value of quitBtnClicked
def quitButtonClicked():
    global quitBtnClicked
    quitBtnClicked = True

## Buttons to control the High Voltage
def HVoffButtonClicked():
    teensySerialData.write('0')
    print("HV Off")

def HVonButtonClicked():
    teensySerialData.write('1')	
    print("HV On")

def insertionButtonClicked():
    teensySerialData.write('3')
    print("Insertion")

def separationButtonClicked():
    teensySerialData.write('2')
    print("Separation")
    
#Start Recording in Widget
## Create widgets to be placed inside

startBtn = QtGui.QPushButton('Start')
startBtn.setToolTip('Click to begin graphing') #This message appears while hovering mouse over button

quitBtn = QtGui.QPushButton('Quit')
quitBtn.setToolTip('Click to quit program')

HVonBtn = QtGui.QPushButton("HV on")
HVonBtn.setToolTip('Click to turn the high voltage on')

HVoffBtn = QtGui.QPushButton("HV off")
HVoffBtn.setToolTip('Click to turn the high voltage off')

insBtn = QtGui.QPushButton("Insertion")
insBtn.setToolTip('Click to start insertion (#3)')

sepBtn = QtGui.QPushButton("Separation")
sepBtn.setToolTip('Click to start separation (#2)')

## Functions in parantheses are to be called when buttons are clicked
startBtn.clicked.connect(startButtonClicked)
quitBtn.clicked.connect(quitButtonClicked)
HVonBtn.clicked.connect(HVonButtonClicked)
HVoffBtn.clicked.connect(HVoffButtonClicked)
insBtn.clicked.connect(insertionButtonClicked)
sepBtn.clicked.connect(separationButtonClicked)

## xSamples is the maximum amount of samples we want graphed at a time
xSamples = 300

## Create plot widget for peak detector plot
pmtPlotWidget = pg.PlotWidget()
pmtPlotWidget.setYRange(0, 4096)
pmtPlotWidget.setXRange(0, xSamples)
pmtPlotWidget.setLabel('top', text = "PMT") #Title to appear at top of widget

## Create a grid layout to manage the widgets size and position
## The grid layout allows us to place a widget in a given column and row
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
## The first number in parantheses is the row, the second is the column
layout.addWidget(quitBtn, 0, 0)
layout.addWidget(startBtn, 2, 0)
layout.addWidget(HVonBtn, 0, 2)
layout.addWidget(insBtn, 2, 2)
layout.addWidget(sepBtn, 3, 2)
layout.addWidget(HVoffBtn, 4, 2)

layout.addWidget(pmtPlotWidget, 1, 1)

## Display the widget as a new window
w.show()

## Initialize all global variables

## Whenever we plot a range of samples, xLeftIndex is the x value on the
## PlotWidget where we start plotting the samples, xRightIndex is where we stop
## These values will reset when they reach the value of xSamples
xRightIndex = 0
xLeftIndex = 0

## These arrays will hold the unplotted voltage values from the pmt
## and the peak detector until we are able to update the plot
pmtData = []

## Used to determine how often we plot a range of values
graphCount = 0

## Time values in microseconds read from the teensy are stored in these variables
## Before timeElapsed is updated, we store its old value in timeElapsedPrev
timeElapsed = 0
timeElapsedPrev = 0

## Determines if we are running through the update loop for the first time
firstRun = True

## Create new file, with the name being today's date and current time and write headings to file in CSV format
i = datetime.now()
fileName = str(i.year) + str(i.month) + str(i.day) + "_" + str(i.hour) + str(i.minute) + str(i.second) + ".csv"

## File is saved to Documents/IPython Notebooks/RecordedData
#f = open('RecordedData\\' + fileName, 'a')
#f.write("#Data from " + str(i.year) + "-" + str(i.month) + "-" + str(i.day) + " at " + str(i.hour) + ":" + str(i.minute) + ":" + str(i.second) + '\n')
#f.write("Timestamp,PMT\n")

## Initialize the container for our voltage values read in from the teensy
## IMPORTANT NOTE: The com port value needs to be updated if the com value
## changes. It's the same number that appears on the bottom right corner of the
## window containing the TeensyDataWrite.ino code

teensySerialData = serial.Serial("/dev/tty.usbmodem1452", 115200)

def update():
    ## Set global precedence to previously defined values
    global xSamples
    global xRightIndex
    global xLeftIndex
    global pmtData
    global graphCount
    global timeElapsed
    global timeElapsedPrev
    global firstRun
    global firstupdate
    
    if firstupdate == 0:
        teensySerialData.flushInput()
        firstupdate += 1
    ## The number of bytes currently waiting to be read in.
    ## We want to read these values as soon as possible, because
    ## we will lose them if the buffer fills up
    bufferSize = teensySerialData.inWaiting()
    runCount = bufferSize//8 # since we write 8 bytes at a time, we similarly want to read them 8 at a time
    #print(bufferSize, runCount)
    while (runCount > 0):
        if (startBtnClicked == True):
        
            #Read in time (int) and PMT output (float with up to 5 decimal places)
            
            temp = []
            temp.append(teensySerialData.readline().strip().split(',') )
            print(bufferSize, runCount, temp[-1][0], temp[-1][1])
            
            timeElapsedPrev = timeElapsed
            timeElapsed = int (temp[0][0])
            
            if (firstRun == True):
                ## Only run once to ensure buffer is completely flushed
                firstRun = False
                teensySerialData.flushInput()
                break
                
            # We'll add all our values to this string until we're ready to exit the loop, at which point it will be written to a file
            stringToWrite = str(timeElapsed) + ","
            
            ## This difference calucalted in the if statement is the amount of time in microseconds since the last value 
            ## we read in and wrote to a file. If this value is significantly greater than 100, we know we have missed some 
            ## values, probably as a result of the buffer filling up and scrapping old values to make room for new values.
            ## The number we print out will be the approximate number of values we failed to read in.
            ## This is useful to determine if your code is running too slow
            #if (timeElapsed - timeElapsedPrev > 8000):
                #print(str((timeElapsed-timeElapsedPrev)/7400))
                
            numData = float (temp[0][1])
            
            pmtData.append(numData)
            stringToWrite = stringToWrite + str(numData) + '\n'
            #f.write(stringToWrite)
            graphCount = graphCount + 1
            xRightIndex = xRightIndex + 1
        runCount = runCount - 1
        
    ## We will start plotting when the start button is clicked
    if startBtnClicked == True:
        if (graphCount >= 1): #We will plot new values once we have this many values to plot
            if (xLeftIndex == 0):
                # Remove all PlotDataItems from the PlotWidgets. 
                # This will effectively reset the graphs (approximately every 30000 samples)
                #pmtPlotWidget.clear()
                pmtPlotWidget.clear()
                
            ## pmtCurve are of the PlotDataItem type and are added to the PlotWidget.
            ## Documentation for these types can be found on pyqtgraph's website

            pmtCurve = pmtPlotWidget.plot()
            xRange = range(xLeftIndex,xRightIndex)
            pmtCurve.setData(xRange, pmtData)
            
            ## Now that we've plotting the values, we no longer need these arrays to store them
            pmtData = []
            xLeftIndex = xRightIndex
            graphCount = 0
            if(xRightIndex >= xSamples):
                xRightIndex = 0
                xLeftIndex = 0
                pmtData = []
                
    if(quitBtnClicked == True):
        ## Close the file and close the window. Performing this action here ensures values we want to write to the file won't be cut off
        #f.close()
        w.close()
        teensySerialData.close()
        #dataprocessing.CSVDataPlot(fileName)
			
        
## Run update function in response to a timer    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start the Qt event loop
app.exec_()