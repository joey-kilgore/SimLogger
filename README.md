![CI Status](https://github.com/joey-kilgore/SimLogger/actions/workflows/ci.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/simlogger)

# SimLogger
Logger and python data archiving

Archive your python objects simply and easiy, and never worry about overwriting files.
All data is defined with 3 key components  
```simTag``` - tag unique for each simulation (like naming the experiment)  
```objTag``` - tag unique for each object (like the variable within the experiments)  
```date-time``` - this is automatically added by SimLogger to help ensure unqiueness of files  

With that you can save your data easily!  
```
from SimLogger import SimLogger
simTag = 'sampleSimulation'
objTag = 'sampleArray'
sampleArray = [1,2,3,4]
SimLogger.saveObj(simTag, objTag, sampleArray, makeNote=True)

# Outputs
# 2024-06-25 10:44:44,063 [INFO ] Logger Loaded
# 2024-06-25 10:44:44,064 [INFO ] OBJECT,sampleSimulation,sampleArray,data/obj/sampleSimulation_sampleArray_2024-06-25_10-44-44.pkl
#
# additionally a file is saved: data/obj/sampleSimulation_sampleArray_2024-06-25_10-44-44.pkl
```

And you can load your data later using a uniqueId  
```uniqueId``` - unique identifier that goes to the python pkl file (almost always is ```simTag_objTag```)  
```
from SimLogger import SimLogger
sampleArrayLoaded = SimLogger.getObjectFromuniqueId('sampleSimulation_sampleArray')
print(sampleArrayLoaded)

# Ouptuts
# [1, 2, 3, 4]
```

## Installation
Install the python package  
```pip install SimLogger```  

To utilize the FigLogger you will need to register your machine ssh keys with kachery  
Run the following command and follow the instructions  
```kachery-cloud-init```


## Development  
install all dependencies (including linting and testing) with:  
`pip install -e '.[lint,test]`  

run tests with:  
`pytest tests/`

run linting + formatting + etc with:  
`pre-commit run --all-files`
