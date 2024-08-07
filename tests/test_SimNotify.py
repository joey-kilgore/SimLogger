from SimLogger import SimNotify


def test_notification():
    endpoint = "https://notify.run/c/WfwXBjk3bD3UrJOV9zRc"

    response = SimNotify.sendNotification("TEST NOTIFICATION", endpoint)
    assert response.ok
