import os
import json

# This file is generated for caching settings at start of application 
# or after a change in settings.json file. This way we don't need to call
# file every time if we already have values from it.

# Settings can be configured from UI or file itself

echoTestHost = ""
echoTestDataPayload = 0
echoTestBacklog = 1
echoTestPort = 0
echoTestTimeout = 0.0

def cache():
    """Reads settings from settings.json and caches them into global variables."""
    global echoTestHost, echoTestPort, echoTestBacklog, echoTestDataPayload, echoTestTimeout
    try:
        # load file as object
        SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")
        # open file and read from it
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            # Host name. Default is localhost
            echoTestHost = settings.get("echoTestHost", "localhost")
            # Data size in bytes. Default is 2048 (2KB)
            echoTestDataPayload = settings.get("echoTestDataPayload", 2048)
            # Number of clients to listen. Default is 1 since this is a test server
            echoTestBacklog = settings.get("echoTestBacklog", 1)
            # Port which server will listen on. Default is 8080
            echoTestPort = settings.get("echoTestPort", 8080)
            # Timeout value for echo test. Default is 3.0
            echoTestTimeout = settings.get("echoTestTimeout", 3.0)
    except Exception as error:
        print(f"Error loading settings: {error}")


def set(
    *,
    echo_test_host=None,
    echo_test_port=None,
    echo_test_backlog=None,
    echo_test_data_payload=None,
    echo_test_timeout=None,
    save_to_file=True,
):
    """Sets configuration values with strict type checking and updates settings.json."""
    global echoTestHost, echoTestPort, echoTestBacklog, echoTestDataPayload, echoTestTimeout

    if echo_test_host is not None:
        if not isinstance(echo_test_host, str):
            raise TypeError(f"echo_test_host must be a str, got {type(echo_test_host).__name__}")
        echoTestHost = echo_test_host

    if echo_test_port is not None:
        if not isinstance(echo_test_port, int) or isinstance(echo_test_port, bool):
            raise TypeError(f"echo_test_port must be an int, got {type(echo_test_port).__name__}")
        if not (1 <= echo_test_port <= 65535):
            raise ValueError(f"echo_test_port must be between 1 and 65535, got {echo_test_port}")
        echoTestPort = echo_test_port

    if echo_test_backlog is not None:
        if not isinstance(echo_test_backlog, int) or isinstance(echo_test_backlog, bool):
            raise TypeError(f"echo_test_backlog must be an int, got {type(echo_test_backlog).__name__}")
        if echo_test_backlog < 1:
            raise ValueError(f"echo_test_backlog must be >= 1, got {echo_test_backlog}")
        echoTestBacklog = echo_test_backlog

    if echo_test_data_payload is not None:
        if not isinstance(echo_test_data_payload, int) or isinstance(echo_test_data_payload, bool):
            raise TypeError(f"echo_test_data_payload must be an int, got {type(echo_test_data_payload).__name__}")
        if echo_test_data_payload < 1:
            raise ValueError(f"echo_test_data_payload must be >= 1, got {echo_test_data_payload}")
        echoTestDataPayload = echo_test_data_payload

    if echo_test_timeout is not None:
        if not isinstance(echo_test_timeout, (int, float)) or isinstance(echo_test_timeout, bool):
            raise TypeError(f"echo_test_timeout must be a float or int, got {type(echo_test_timeout).__name__}")
        if echo_test_timeout <= 0:
            raise ValueError(f"echo_test_timeout must be > 0, got {echo_test_timeout}")
        echoTestTimeout = float(echo_test_timeout)

    # Persist updated values to settings.json
    if save_to_file:
        try:
            data = {
                "echoTestHost": echoTestHost,
                "echoTestPort": echoTestPort,
                "echoTestBacklog": echoTestBacklog,
                "echoTestDataPayload": echoTestDataPayload,
                "echoTestTimeout": echoTestTimeout,
            }

            SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")
            with open(SETTINGS_FILE, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            print(f"Error persisting settings to file: {error}")

# Load initial cached settings on import
cache()