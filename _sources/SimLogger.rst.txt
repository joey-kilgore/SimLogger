SimLogger.SimLogger module
==========================

The SimLogger module is the fundamental piece of the SimLogger package.

The SimLogger functions on the key principal that everything in a simulation
can be uniquely identified with the following:
1. simTag - uniquely identifies a particular simulation configuration. 
    This is changed for every single test run. Everytime the parameters
    are changed (and you re-run your simulation) you should update your
    simTag accordingly.  
2. objTag - uniquely identifies a particular object within a simulation.
    This is the same across simulations, but should be a unique name for the 
    object within the simulation.
3. date-time string - all pickled files have an additional date-time string
    appended to the file name to avoid any accidental overwriting of data.

With that, all data can be uniquely named and pickled to file. Pickling provides
an easy way to store and load files in python, and is the compression method
used in the SimLogger.  

This could be an example script

.. code-block:: python
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

Which lays out the simTag for the simualtion, then defines an object we are going to save,
with the objTag and then stores it with the SimLogger. 
This also generates an example.log file so that you can always refer somewhere to know exactly where the data has been stored.

In future analysis, the data can be loaded as needed using the following
To reference the object you will need the unique id of the object, which is simTag_objTag

.. code-block:: python
    from SimLogger import SimLogger
    sampleArrayLoaded = SimLogger.getObjectFromuniqueId('sampleSimulation_sampleArray')
    print(sampleArrayLoaded)
    
    # Ouptuts
    # [1, 2, 3, 4]

Within this framework, various configurations can be changed:
- log file name
- folder where the pickled files get saved

SimLogger.SimLogger Functions
-----------------------------

.. automodule:: SimLogger.SimLogger
   :members:
   :undoc-members:
   :show-inheritance:

