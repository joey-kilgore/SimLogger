from SimLogger import SimLogger


def test_save_and_get():
    a = "sample-object"
    simTag = "testing-simTag"
    objTag = "testing-objTag"
    SimLogger.saveObj(simTag, objTag, a)
    aLoaded = SimLogger.getObjectFromUniqueId(f"{simTag}_{objTag}")
    assert a == aLoaded
