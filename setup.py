import json

def get_settings():
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    return settings

def update_settings(update):
    with open("Settings.json", "w") as f:
        json.dump(update, f, indent=4)

        

def get_status():
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    try: 
        return settings["Status"]
    except KeyError:
        settings["Status"] = {
            "Running": False,
            "Minute": "42"
        }
        update_settings(settings)
        return settings["Status"]

def update_status(update):
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    settings["Status"] = update
    update_settings(settings)

    

def get_channels():
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    try:
        return settings["Channels"]
    except KeyError:
        settings["Channels"] = {}
        update_settings(settings)
        return settings["Channels"]

def update_channels(update):
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    settings["Channels"] = update
    update_settings(settings)

def get_channel(channel_id):
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    try:
        return settings["Channels"][str(channel_id)]
    except KeyError:
        return None

def update_channel(channel_id, update):
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    settings["Channels"][str(channel_id)] = update
    update_settings(settings)

def clean_channels():
    with open("Settings.json", "r") as f:
        settings = json.load(f)
    settings["Channels"] = {}
    update_settings(settings)

