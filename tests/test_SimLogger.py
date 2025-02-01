from SimLogger import SimLogger


def test_save_and_get():
    a = "sample-object"
    simTag = "testing-simTag"
    objTag = "testing-objTag"
    SimLogger.saveObj(simTag, objTag, a)
    aLoadedUniqueId = SimLogger.getObjectFromUniqueId(f"{simTag}_{objTag}")
    aLoadedObjTag = SimLogger.getObj(simTag, objTag)
    assert a == aLoadedUniqueId
    assert a == aLoadedObjTag
