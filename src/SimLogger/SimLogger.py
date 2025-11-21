import logging
import pickle
from datetime import datetime
from pathlib import Path
import pandas as pd
import os
from git import Repo
import argparse

isLoaded = False
_simTag = None  # Global variable to store the simulation tag for auto-saving


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


def saveArgs(simTag, args, objFolder=os.path.join("data", "obj"), makeNote=True):
    """Save argparse command line arguments to a pickle file and optionally log them.
    This is a convenience function to automatically save CLI arguments from argparse.

    Args:
        simTag (str): Unique tag for the simulation
        args (argparse.Namespace): Parsed arguments from argparse
            ArgumentParser.parse_args()
        objFolder (str): Folder where the pickled file will be saved
        makeNote (bool): Sets whether an additional note is made about the
            arguments

    Returns:
        filePath (str): the unique file path where the pickled arguments are saved

    Example:
        >>> import argparse
        >>> from SimLogger import SimLogger
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--param1', type=int, default=10)
        >>> parser.add_argument('--param2', type=str, default='test')
        >>> args = parser.parse_args()
        >>> SimLogger.saveArgs('mySimulation', args)
    """
    # Convert argparse.Namespace to dictionary for better readability
    args_dict = vars(args)

    # Save the arguments as a pickled object
    filePath = saveObj(simTag, "args", args_dict, objFolder=objFolder, makeNote=False)

    # Log each argument individually for easy reference
    if makeNote:
        logNotes("ARGS," + simTag + ",saved," + filePath)
        for key, value in args_dict.items():
            logNotes("ARG," + simTag + "," + key + "," + str(value))

    return filePath


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


def getObj(simTag, objTag, objFolder=os.path.join("data", "obj")):
    """Loads a previously saved object using the simTag and objTag
    If there are multiple objects that have this, we are automatically
    grabbing the first instance found (by alphabetical file name).
    If you accidently saved multiple copies (differentiated by the
    date-time string, you should use `getObjectFromUniqueId()`

    Args:
        simTag (str): Unique tag for the simulation
        objTag (str): Unique tag for the object saved
        objFolder (str): Folder containing the pickled file

    Returns:
        obj (Object): Loaded pickled object
    """
    return getObjectFromUniqueId(f"{simTag}_{objTag}", objFolder=objFolder)


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


class ArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that automatically saves arguments when
    parse_args() is called.

    This class extends argparse.ArgumentParser to provide automatic saving of
    command-line arguments. When parse_args() is called, the arguments are
    automatically saved using saveArgs() if a simulation tag has been set.

    To use this feature:
    1. Set the simulation tag using setSimTag() before parsing arguments
    2. Use SimLogger.ArgumentParser instead of argparse.ArgumentParser
    3. Call parse_args() as usual - arguments will be saved automatically

    Example:
        >>> from SimLogger import SimLogger
        >>> SimLogger.setSimTag('myExperiment')
        >>> parser = SimLogger.ArgumentParser()
        >>> parser.add_argument('--learning_rate', type=float, default=0.001)
        >>> args = parser.parse_args()  # Arguments are automatically saved!
    """

    def __init__(self, *args, simTag=None, autoSave=True, **kwargs):
        """Initialize the ArgumentParser.

        Args:
            simTag (str): Optional simulation tag for auto-saving arguments.
                If not provided, uses the global simTag set by setSimTag().
            autoSave (bool): Whether to automatically save arguments when
                parse_args() is called. Default is True.
            *args, **kwargs: All other arguments are passed to
                argparse.ArgumentParser
        """
        super().__init__(*args, **kwargs)
        self._simTag = simTag
        self._autoSave = autoSave

    def parse_args(self, args=None, namespace=None):
        """Parse arguments and automatically save them if autoSave is enabled.

        Args:
            args: List of strings to parse. If None, uses sys.argv.
            namespace: Object to populate with parsed arguments.

        Returns:
            Namespace object with parsed arguments
        """
        parsed_args = super().parse_args(args, namespace)

        # Auto-save if enabled and we have a simTag
        if self._autoSave:
            simTag = self._simTag if self._simTag is not None else _simTag
            if simTag is not None:
                saveArgs(simTag, parsed_args)
            else:
                # Log a warning if auto-save is enabled but no simTag is set
                global isLoaded
                if not isLoaded:
                    setupLogger()
                logging.warning(
                    "ArgumentParser auto-save is enabled but no simTag is set. "
                    "Use setSimTag() or pass simTag to ArgumentParser constructor."
                )

        return parsed_args


def setSimTag(simTag):
    """Set the global simulation tag for automatic argument saving.

    This sets the simulation tag that will be used by SimLogger.ArgumentParser
    for automatic saving of parsed arguments.

    Args:
        simTag (str): Unique tag for the simulation

    Example:
        >>> from SimLogger import SimLogger
        >>> SimLogger.setSimTag('myExperiment')
        >>> parser = SimLogger.ArgumentParser()
        >>> parser.add_argument('--param1', type=int)
        >>> args = parser.parse_args()  # Automatically saved to 'myExperiment'
    """
    global _simTag
    _simTag = simTag
