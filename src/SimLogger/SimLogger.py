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

def readDatFile(filePath, withHeader=False):
    data = []
    with open(filePath) as f:
        if(withHeader):
            header = f.readline()
        for i in range(0, int(f.readline())):
            temp2d = []
            for j in range(0, int(f.readline())):
                temp1d = []
                for k in range(0, int(f.readline())):
                    temp1d.append(float(f.readline()))
                temp2d.append(temp1d)
            data.append(temp2d)
    return data

def saveInitWeights(simTag, objFolder='./data/obj/', initWeightsFilePath='./initWeights.dat'):
    initWeights = readDatFile(initWeightsFilePath)
    saveObj(simTag, 'init_weights', initWeights, objFolder=objFolder, makeNote=False)

def saveWeightFiles(simTag, epochs, weightFileDir='./data/weights', clearFolder=False):
    for e in range(epochs):
        weightFile = weightFileDir+'/weights'+str(e)+'.dat'
        try:
            tempWeights = readDatFile(weightFile)
            saveObj(simTag, 'weights_'+str(e), tempWeights)
      
            if(clearFolder):
                os.remove(weightFile)
        except:
            print('Training finished early')
            break

def getWeightFromUniqueId(uniqueId, objFolder='./data/obj'):
    fileList = os.listdir(objFolder)
    filePath = [i for i in fileList if uniqueId in i][0]
    with open(objFolder+'/'+filePath, "rb") as f:
        tempWeight = pickle.load(f)

    return tempWeight

def pklToInitWeights(simTag, epoch, objFolder='./data/obj'):
    uniqueId = simTag+'_weights_'+str(epoch)
    if(epoch==-1):
        uniqueId = simTag+'_init_weights_'

    tempWeight = getWeightFromUniqueId(uniqueId, objFolder=objFolder)
    initWeightFile = './initWeights.dat'
    with open(initWeightFile, 'w') as f:
        f.write(str(len(tempWeight))+'\n')
        for i in range(0, len(tempWeight)):
            f.write(str(len(tempWeight[i]))+'\n')
            for j in range(0, len(tempWeight[i])):
                f.write(str(len(tempWeight[i][j]))+'\n')
                for k in range(0, len(tempWeight[i][j])):
                    f.write(("%.6f"%tempWeight[i][j][k])+'\n')

def isSimTagAvailable(simTag, objFolder='./data/obj'):
    fileList = os.listdir(objFolder)
    fileList = [i for i in fileList if simTag in i]
    if(len(fileList)>0):
        return False
    return True
