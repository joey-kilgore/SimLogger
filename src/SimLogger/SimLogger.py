import logging
import pickle
from datetime import datetime
from pathlib import Path
import pandas as pd
import os
from git import Repo

isLoaded = False


def setupLogger(fileName="example.log", githubLink=None):
    """Initialize the logger. Sets the log directory and the default object directoy.

    Args:
        fileName (str): file name for the log output
        githubLink (str): link to the github repository to allow for the note
            of the most recent commit to be in the form of a github link
            directly to that commit ex. "www.github.com/joey-kilgore/SimLogger"

    Returns:
        None
    """
    global isLoaded
    Path("data").mkdir(parents=True, exist_ok=True)
    Path(os.path.join("data", "obj")).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-5.5s] %(message)s",
        datefmt="%Y/%m/%d %I:%M:%S %p",
        filename=fileName,
        level=logging.INFO,
    )
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    isLoaded = True
    logging.info("Logger Loaded")

    try:
        repo = Repo(".")
        commitSHA = repo.head.object.hexsha
        if githubLink is not None:
            logNotes("COMMIT LINK: " + githubLink + "/commit/" + commitSHA)
        else:
            logNotes("COMMIT SHA: " + commitSHA)
    except Exception as e:
        logNotes("ERROR LOADING GIT: " + str(e))


def logNotes(notes):
    """Save a notes string to the log directly

    Args:
        notes (str): text that will be written to the log

    Returns:
        None
    """
    global isLoaded
    if not isLoaded:
        setupLogger()
    logging.info(notes)


def saveObj(simTag, objTag, obj, objFolder=os.path.join("data", "obj"), makeNote=False):
    """Save an object (obj) to pickle file in the object folder.
    The file name will be the {simTag}_{objTag}_{dateTimeString}.pkl

    Args:
        simTag (str): Unique tag for the simulation
        objTag (str): Unique tag for the object within the simulation
        obj (Object): Object to be pickled and saved to file
        objFolder (str): Folder where the pickled file will be saved
        makeNote (bool): Sets whether an additional note is made about the object

    Returns:
        filePath (str): the unique file path where the pickled object is saved
    """
    global isLoaded
    if not isLoaded:
        setupLogger()

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    filePath = os.path.join(objFolder, simTag + "_" + objTag + "_" + dt_string + ".pkl")
    with open(filePath, "wb") as file:
        pickle.dump(obj, file, protocol=3)

    if makeNote:
        logNotes("OBJECT," + simTag + "," + objTag + "," + filePath)

    return filePath


def saveSimulation(simTag, inputDict, outputDict, notes="No additional notes"):
    """Save inputs and outputs of a simulation

    Args:
        simTag (str): Unique tag for the simulation
        inputDict ({str:Object}): list of object names (keys) and
                                    the objects to be saved (values)
        outputDict ({str:Object}): same structure as the inputDict
        notes (str): Additional notes to be written at the end of the log

    Returns:
        None
    """
    global isLoaded
    if not isLoaded:
        setupLogger()

    logging.info("SIMULATION " + simTag + " INPUTS")
    for key in inputDict.keys():
        if not isinstance(inputDict[key], str):
            filePath = saveObj(simTag, key, inputDict[key])
            text = "INPUT," + simTag + "," + key + "_file," + filePath
        else:
            text = "INPUT," + simTag + "," + key + "," + inputDict[key]
        logging.info(text)
    logging.info("SIMULATION " + simTag + " OUTPUTS")
    for key in outputDict.keys():
        if not isinstance(outputDict[key], str):
            filePath = saveObj(simTag, key, outputDict[key])
            text = "OUTPUT," + simTag + "," + key + "_file," + filePath
        else:
            text = "OUTPUT," + simTag + "," + key + "," + outputDict[key]
        logging.info(text)
    logging.info("SIMULATION " + simTag + " NOTES")
    logging.info("NOTE," + simTag + "," + notes)


def convertLog(logfile="example.log", logdir="."):
    """Convert a log to a csv format based on the simulation input/outputs

    Args:
        logfile (str): the log file name
        logdir (str): directory where the file is located

    Returns:
        None
    """
    lines = []
    with open(os.path.join(logdir, logfile), "r") as f:
        lines = f.readlines()
    curSimTag = ""
    simData = {}
    for line in lines:
        lineSplit = line.split(",")
        try:
            simTag = lineSplit[1]
            objTag = lineSplit[2]
            obj = lineSplit[3].replace("\n", "")
            date = lineSplit[0].split(" ")[0]
            time = lineSplit[0].split(" ")[1]
            lineSplit[0].split("]")[1].replace(" ", "")
        except Exception:
            print("non-object line : " + line)
            continue
        if curSimTag != simTag:
            simData[simTag] = {"simTag": simTag}
            simData[simTag]["date"] = date
            simData[simTag]["time"] = time
            curSimTag = simTag
        simData[simTag][objTag] = obj
    objTagList = []
    for simTag in simData.keys():
        for objTag in simData[simTag].keys():
            if objTag not in objTagList:
                objTagList.append(objTag)
    df = pd.DataFrame(columns=objTagList)
    for simTag in simData.keys():
        df = df.append(simData[simTag], ignore_index=True)
    fileName = logdir + "/" + logfile.split(".")[0] + ".csv"
    df.to_csv(fileName, sep=",")


def getObjectFromUniqueId(uniqueId, objFolder=os.path.join("data", "obj")):
    """Loads an object previously saved from the unique id ({simTag}_{objTag})

    Args:
        uniqueId (str): Unique id of the pickled file name ({simTag}_{objTag})
        objFolder (str): Folder containing the pickled files

    Returns:
        obj (Object): Loaded pickled object
    """
    fileList = os.listdir(objFolder)
    filePath = [i for i in fileList if uniqueId in i][0]
    with open(os.path.join(objFolder, filePath), "rb") as f:
        tempObj = pickle.load(f)

    return tempObj


def isSimTagUsed(simTag, objFolder=os.path.join("data", "obj")):
    """Checks if there are any objects already saved in the objFolder
    that uses the simTag

    Args:
        simTag (str): Unique simulation id
        objFolder (str): Folder containing the pickled files

    Returns:
        isUsed (bool): whether there are pkl files with the simTag used
    """
    fileList = os.listdir(objFolder)
    fileList = [i for i in fileList if simTag in i]
    if len(fileList) > 0:
        return False
    return True
