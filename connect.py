import requests


def connect_hotspot():
    tank_url = "http://192.168.4.1/js?"
    tank_payload = {"T": 61}

    try:
        r = requests.post(tank_url, json=tank_payload, timeout=1)
    except requests.exceptions.ConnectionError:
        pass
    except:
        pass


connect_hotspot()
