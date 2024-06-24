import logging
import pickle
from datetime import datetime
from pathlib import Path
import pandas as pd
import os

isLoaded = False

def setupLogger(fileName = 'example.log'):
    global isLoaded
    Path('data').mkdir(parents=True, exist_ok=True)
    Path(os.path.join('data','obj')).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(format='%(asctime)s [%(levelname)-5.5s] %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', filename=fileName, level=logging.INFO)
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    isLoaded = True
    logging.info('Logger Loaded')

def logNotes(notes):
    global isLoaded
    if(not isLoaded):
        setupLogger()
    logging.info(notes)

def saveObj(simTag, objTag, obj, objFolder=os.path.join('data','obj'), makeNote=False):
    global isLoaded
    if(not isLoaded):
        setupLogger()

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    filePath =os.path.join(objFolder, simTag + '_' + objTag + '_' + dt_string + '.pkl')
    with open(filePath, 'wb') as file:
        pickle.dump(obj, file, protocol=3)

    if(makeNote):
        logNotes('OBJECT,' + simTag + ',' + objTag + ',' + filePath)
        
    return filePath

def saveSimulation(simTag, inputDict, outputDict, notes='No additional notes'):
    global isLoaded
    if(not isLoaded):
        setupLogger()

    logging.info('SIMULATION ' + simTag + ' INPUTS')
    for key in inputDict.keys():
        if (not isinstance(inputDict[key], str)):
            filePath = saveObj(simTag, key, inputDict[key])
            text = 'INPUT,' + simTag + ',' + key + '_file,' + filePath
        else:
            text = 'INPUT,' + simTag + ',' + key + ',' + inputDict[key]
        logging.info(text)
    logging.info('SIMULATION ' + simTag + ' OUTPUTS')
    for key in outputDict.keys():
        if (not isinstance(outputDict[key], str)):
            filePath = saveObj(simTag, key, outputDict[key])
            text = 'OUTPUT,' + simTag + ',' + key + '_file,' + filePath
        else:
            text = 'OUTPUT,' + simTag + ',' + key + ',' + outputDict[key]
        logging.info(text)
    logging.info('SIMULATION ' + simTag + ' NOTES')
    logging.info('NOTE,'+ simTag + ',' + notes)

def convertLog(logfile='example.log', logdir='.'):
    lines = []
    with open(os.path.join(logdir,logfile),'r') as f:
        lines = f.readlines()
    curSimTag = ''
    simData = {}
    for line in lines:
        lineSplit = line.split(',')
        try:
            simTag = lineSplit[1]
            objTag = lineSplit[2]
            obj = lineSplit[3].replace('\n','')
            date = lineSplit[0].split(' ')[0]
            time = lineSplit[0].split(' ')[1]
            inOut = lineSplit[0].split(']')[1].replace(' ','')
        except:
            print('non-object line : ' + line)
            continue
        if curSimTag != simTag:
            simData[simTag] = {'simTag':simTag}
            simData[simTag]['date'] = date
            simData[simTag]['time'] = time
            curSimTag = simTag
        simData[simTag][objTag] = obj
    objTagList = []
    for simTag in simData.keys():
        for objTag in simData[simTag].keys():
            if (objTag not in objTagList):
                objTagList.append(objTag)
    df = pd.DataFrame(columns=objTagList)
    for simTag in simData.keys():
        df = df.append(simData[simTag], ignore_index=True)
    fileName = logdir + '/' + logfile.split('.')[0] + '.csv'
    df.to_csv(fileName, sep=',')

def getObjectFromUniqueId(uniqueId, objFolder=os.path.join('data','obj')):
    fileList = os.listdir(objFolder)
    filePath = [i for i in fileList if uniqueId in i][0]
    with open(os.path.join(objFolder,filePath), "rb") as f:
        tempWeight = pickle.load(f)

    return tempWeight

def isSimTagUsed(simTag, objFolder=os.path.join('data','obj')):
    fileList = os.listdir(objFolder)
    fileList = [i for i in fileList if simTag in i]
    if(len(fileList)>0):
        return False
    return True
