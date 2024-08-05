from SimLogger import SimLogger
import figurl as fig
import plotly.express as px
import pandas as pd
import os


def createPlot(
    simTag,
    objTag,
    x,
    y,
    objFolder=os.path.join("data", "obj"),
    z=None,
    plotType="scatter",
    title="Plot",
    labels={"x": "x", "y": "y", "z": "z"},
    makeNote=True,
    **kwargs,
):
    """Generate a plot that will automatically be saved (using SimLogger)
    and will generate a url to access the graph through the cloud
    (see kachery-cloud-init)

    Args:
        simTag (str): Unique id for the simulation
        objTag (str): Unique id for this graph within the simulation
        x ([int|float]): x values for the graph
        y ([int|float]): y values for the graph
        objFolder (str): location where the pickled objects should go
        z ([int|float[): z values for the graph (optional, but only for 3d scatter)
        plotType (str): Either "scatter" for scatter plots
                        Or "line" for line plots (not for 3d plots)
        title (str): Title for the plot
        labels ({str:str}): Key value pairs for the keys "x", "y", ("z") that go to
                            the values corresponding to the axis labels
        makeNote (bool): Whether the log should be noted with the saved files
        **kwargs: Additional args for the plotly express graph

    Returns:
        url (str): The figurl link to access the graph
    """
    data = {"x": x, "y": y}
    if z is not None:
        data["z"] = z

    df = pd.DataFrame(data)

    if plotType == "scatter":
        if z is not None:
            fig = px.scatter_3d(
                df, x="x", y="y", z="z", title=title, labels=labels, **kwargs
            )
        else:
            fig = px.scatter(df, x="x", y="y", title=title, labels=labels, **kwargs)
    elif plotType == "line":
        fig = px.line(df, x="x", y="y", title=title, labels=labels, **kwargs)
    else:
        raise ValueError("Unsupported plotType. Supported types: 'scatter', 'line'.")

    url = savePlotly(
        simTag, objTag, fig, label=title, objFolder=objFolder, makeNote=makeNote
    )
    return url


def savePlotly(
    simTag, objTag, ff, label="", objFolder=os.path.join("data", "obj"), makeNote=True
):
    """Save a previously created plotly graph to the cloud for remote access
    and pickle the graph for access later

    Args:
        simTag (str): Unique id for the simulation
        objTag (str): Unique id for the graph within the simulation
        ff (plotly figure): User created figure (with plotly)
        label (str): Optional label for the figurl cloud saved graph
        objFolder (str): location where the pickled objects should go
        makeNote (str): Note in the log that the pickled file was saved

    Returns:
        url (str): The figurl link to access the graph
    """
    if label == "":
        label = objTag
    url = fig.Plotly(ff).url(label=label)
    SimLogger.logNotes(f"{label} GRAPH AVAILABLE AT: {url}")
    SimLogger.saveObj(simTag, objTag, ff, objFolder=objFolder, makeNote=makeNote)

    return url
