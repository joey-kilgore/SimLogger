SimLogger.FigLogger module
==========================

The FigLogger is designed to solve the problem of not being able to easily
view detailed graphs through a command line interface with remote computing
systems. To solve this, an integration between the SimLogger for data archiving
and kachery were combined to give remote access to data through a web interface.

Installation
------------

After following the initial installation steps for the SimLogger package.
Ensure the machine is setup to access the kachery cloud

``kachery-cloud-init``

and follow the steps to setup the connection.

With that you can now generate your own graphs, and then remotely view them.
The graphs are also saved to file using the SimLogger so you can always
simply load up the pickled version of the graph and show it again on a local
machine if desired.

The simplest method is to let FigLogger generate the plot for you. This is
great for when you want a simple scatter or line plot without much specifics.

.. code-block:: python
    from SimLogger import FigLogger

    simTag = "testSim"
    objTag = "samplePlot"

    epoch = [0,1,2,3,4]
    loss = [3.0, 2.7, 2.6, 2.5, 2.45]
    
    plotType = "line"
    title = "Sample Plot"
    labels={"x":"Epoch","y":"Loss"}

    FigLogger.createPlot(simTag, 
                            objTag, 
                            epoch, 
                            loss,
                            plotType=plotType, 
                            title=title, 
                            labels=labels)


Which will automatically generate a line plot with the data given, and will
give a link to the graph in the log file.

SimLogger.FigLogger functions
-----------------------------

.. automodule:: SimLogger.FigLogger
   :members:
   :undoc-members:
   :show-inheritance:

