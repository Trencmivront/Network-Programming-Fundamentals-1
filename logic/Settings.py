import os
import json

from logger import get_logger

logger = get_logger("Settings")

# This file is generated for caching settings at start of application 
# or after a change in settings.json file. This way we don't need to call
# file every time if we already have values from it.

# Settings can be configured from UI or file itself
echoServerHost = ""
echoServerDataPayload = 0
echoServerBacklog = 1
echoServerPort = 0
echoTestTimeout = 0.0
echoClientPayloadCount = 0

ntpURL = ''

loggingEnabled = True
debuggingEnabled = False

def cache():
    """Reads settings from settings.json and caches them into global variables."""
    global echoServerHost, echoServerPort, echoServerBacklog, echoServerDataPayload, echoTestTimeout, ntpURL, echoClientPayloadCount, loggingEnabled, debuggingEnabled
    try:
        # load file as object
        SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")
        # open file and read from it
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            # Host name. Default is localhost
            echoServerHost = settings.get("echoServerHost", "localhost")
            # Data size in bytes. Default is 2048 (2KB)
            echoServerDataPayload = settings.get("echoServerDataPayload", 2048)
            # Number of clients to hold in line. Default is 1 since this is a test server.
            # Remember to increase this value if you are going to use multiple test clients.
            echoServerBacklog = settings.get("echoServerBacklog", 1)
            # Port which server will listen on. Default is 8080
            echoServerPort = settings.get("echoServerPort", 8080)
            # Timeout value for echo test. Default is 3.0
            echoTestTimeout = settings.get("echoTestTimeout", 3.0)
            # NTPClient.request() parameter, the url of ntp server. Default is 'pool.ntp.org'
            ntpURL = settings.get("ntpURL", 'pool.ntp.org')
            # Repeat count of which how many payload client will send before closing. Set this value to -1 for infinite.
            # The default is 1, and 0 makes server close immidiately
            echoClientPayloadCount = settings.get("echoClientPayloadCount", 1)
            # Logging and debugging flags (no logic assigned yet)
            loggingEnabled = settings.get("logging", True)
            debuggingEnabled = settings.get("debugging", False)
    except Exception as error:
        print(f"Error loading settings: {error}")


def init():
    """Initializes settings to default values and updates settings.json."""
    set(
        echo_server_host="localhost",
        echo_server_port=8080,
        echo_server_backlog=1,
        echo_server_data_payload=2048,
        echo_test_timeout=3.0,
        ntp_url="pool.ntp.org",
        echo_client_payload_count=1,
        logging_enabled=True,
        debugging_enabled=False,
    )


def set(
    *,
    echo_server_host=None,
    echo_server_port=None,
    echo_server_backlog=None,
    echo_server_data_payload=None,
    echo_test_timeout=None,
    ntp_url=None,
    echo_client_payload_count=None,
    logging_enabled=None,
    debugging_enabled=None,
    save_to_file=True,
):
    """Sets configuration values with strict type checking and updates settings.json."""
    global echoServerHost, echoServerPort, echoServerBacklog, echoServerDataPayload, echoTestTimeout, ntpURL, echoClientPayloadCount, loggingEnabled, debuggingEnabled

    if echo_server_host is not None:
        if not isinstance(echo_server_host, str):
            raise TypeError(f"echo_server_host must be a str, got {type(echo_server_host).__name__}")
        echoServerHost = echo_server_host

    if echo_server_port is not None:
        if not isinstance(echo_server_port, int) or isinstance(echo_server_port, bool):
            raise TypeError(f"echo_server_port must be an int, got {type(echo_server_port).__name__}")
        if not (1 <= echo_server_port <= 65535):
            raise ValueError(f"echo_server_port must be between 1 and 65535, got {echo_server_port}")
        echoServerPort = echo_server_port

    if echo_server_backlog is not None:
        if not isinstance(echo_server_backlog, int) or isinstance(echo_server_backlog, bool):
            raise TypeError(f"echo_server_backlog must be an int, got {type(echo_server_backlog).__name__}")
        if echo_server_backlog < 1:
            raise ValueError(f"echo_server_backlog must be >= 1, got {echo_server_backlog}")
        echoServerBacklog = echo_server_backlog

    if echo_server_data_payload is not None:
        if not isinstance(echo_server_data_payload, int) or isinstance(echo_server_data_payload, bool):
            raise TypeError(f"echo_server_data_payload must be an int, got {type(echo_server_data_payload).__name__}")
        if echo_server_data_payload < 1:
            raise ValueError(f"echo_server_data_payload must be >= 1, got {echo_server_data_payload}")
        echoServerDataPayload = echo_server_data_payload

    if echo_test_timeout is not None:
        if not isinstance(echo_test_timeout, (int, float)) or isinstance(echo_test_timeout, bool):
            raise TypeError(f"echo_test_timeout must be a float or int, got {type(echo_test_timeout).__name__}")
        if echo_test_timeout <= 0:
            raise ValueError(f"echo_test_timeout must be > 0, got {echo_test_timeout}")
        echoTestTimeout = float(echo_test_timeout)

    if ntp_url is not None:
        if not isinstance(ntp_url, str):
            raise TypeError(f"ntp_url must be a str, got {type(ntp_url).__name__}")
        ntpURL = ntp_url

    if echo_client_payload_count is not None:
        if not isinstance(echo_client_payload_count, int) or isinstance(echo_client_payload_count, bool):
            raise TypeError(f"echo_client_payload_count must be an int, got {type(echo_client_payload_count).__name__}")
        if echo_client_payload_count == 0:
            logger.warning("Expected payload count is 0, echo test server won't run. If this was a mistake, check application settings.")
        echoClientPayloadCount = echo_client_payload_count

    # logging and debugging: no logic assigned yet, just persist the values
    if logging_enabled is not None:
        loggingEnabled = logging_enabled
    if debugging_enabled is not None:
        debuggingEnabled = debugging_enabled

    # Persist updated values to settings.json
    if save_to_file:
        try:
            data = {
                "echoServerHost": echoServerHost,
                "echoServerPort": echoServerPort,
                "echoServerBacklog": echoServerBacklog,
                "echoServerDataPayload": echoServerDataPayload,
                "echoTestTimeout": echoTestTimeout,
                "ntpURL": ntpURL,
                "echoClientPayloadCount": echoClientPayloadCount,
                "logging": loggingEnabled,
                "debugging": debuggingEnabled,
            }

            SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings.json")
            with open(SETTINGS_FILE, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            print(f"Error persisting settings to file: {error}")


# Load initial cached settings on import
cache()