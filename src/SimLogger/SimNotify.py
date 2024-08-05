from notify_run import Notify
from SimLogger import SimLogger


def sendNotification(text, endpoint=None):
    """Send notification using notify! Check the README.md for setup details.

    Args:
        text (str): text that will be sent as the notification (typically simTag and
            message) endpoint (str, optional): If a notify channel (endpoint) has
            been setup (*which you should*) include the link here, and the
            notification will be sent to that channel. If you don't include this
            then a channel will be generated and you can view it after the fact.

    """
    if endpoint is None:
        notify = Notify()
        endpoint = notify.register()
        SimLogger.logNotes("WARNING: NOTIFY NOT CONFIGURED. PLEASE SEE README.MD")
    else:
        # simplify handling if users don't remove /c/
        endpoint = endpoint.replace("/c/", "/")
        notify = Notify(endpoint=endpoint)

    SimLogger.logNotes(f"USING NOTIFY ENDPOINT: {endpoint}")
    notify.send(text)
