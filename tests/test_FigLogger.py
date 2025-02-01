from SimLogger import SimLogger, FigLogger


def test_graph_save():
    x = [0, 1, 2, 3]
    y = [1, 2, 3, 4]
    simTag = "testing-simTag"
    objTag = "testing-graph"
    FigLogger.createPlot(simTag, objTag, x, y, cloudSave=False)
    SimLogger.getObj(simTag, objTag)
