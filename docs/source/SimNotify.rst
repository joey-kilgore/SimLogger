SimLogger.SimNotify module
==========================

Often when simulations are running for an extended period of time on a cluster machine,
not to mention the time spent waiting for available resource, it is useful to get remote
updates to know how well a simulation is performing. This module seeks to solve that
problem while being integrated into the SimLogger system. Additionally, this uses
an openly and freely available system for remote web notifications notify-run

In this package we don't reference the python interface for notify-run since configuration
can be finicky. Instead, we will directly send post requests to simplify the process.

Installation
------------

Nofity runs on channels, that you can then easily subscribe to through the web interface.
To do this, go to https://notify.run/ and create a new channel. Copy the link that it
generates. This link will be the URL to go to and see any notifications.

Using that link you can then send notifications:

.. code-block:: python

    from SimLogger import SimNotify
    endpoint = "paste-link-here"
    SimNotify.sendNotification("Hello World", endpoint)


Which will post a Hello World message on the channel.

Additionally, the notification, endpoint, and response code from the server are all
listed in the log file.

SimLogger.FigLogger functions
-----------------------------

.. automodule:: SimLogger.SimNotify
   :members:
   :undoc-members:
   :show-inheritance:

