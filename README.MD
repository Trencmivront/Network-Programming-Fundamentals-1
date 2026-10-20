# Network Utils in Python
This project is a GUI application, contains various of network actions.
System network information (hostname, IP addresses, network interfaces), client-server connection testing, chat module, SNTP time information, settings and error handling.

## Device Network Info
This module displays hostname of the current computer, network interfaces and ip addresses related to network interfaces.

Instead of using `getbyhostname()`, it uses `netifaces` library and gets ip addresses of each network interface. This is a faster approach (saves 10 seconds on my computer) and returns more detailed information.

## Client-Server Echo Test Module
In this module one computer picks client and other picks server mode. The server constants like **hostname, port, backlog, payload size, timeout** and **accept count** can be changed from in-app settings panel or `settings.json` file located in root folder of this application.

Server can be opened with one click and if there is an error occours, error window will pop up.

The server accepts messages count of **echoClientPayloadCount** value in settings. If value is set to `0`, server will be `closed` immidiately. If value is `-1`, server will accept `unlimited` number of payload.

Client must write **hostname, port** and **message** values by hand for every test.

## Chat Module
Again in this module one computer becomes server and others client. Multiple clients can connect to same chat server.

Server values can be set from settings panel. Client values are taken from user for every connection.

Server starts, stores each client connection and travels on them for each new message. The received messages are being displayed on the window. If server sends a message, it will be sent to all stored connected clients. Each message successfully being sent and received will be written into file with name `"<current_date>.txt"` under folder `chats` on root folder. The write operation is done when the server disconnects (closing the writer).

Client connects with a **name, hostname** and **port** values. Name is username of the client, rest belongs to the server. Again same logic holds here. When a client sends message, it is sent to all clients and server. File output logic is same.

## SNTP
This is the simpliest module. It just retrieves the time information from given SNTP server URL in settings and displays it along side with local time information.

## Settings
Different values for different modules can be changed here.

Changing `logging` will only disable file output, command line logging stays.

`Debugging` setting will show a debug window, which displays logs in real time. Work principle is simple, if debugging and debug window, show in debug window. It uses a custom `StreamHandler` for this work.

## Error Handling
There is a `logs` folder which contains `error.log` and `app.log`. You can get what they log by looking at the names.

Writing logs into a file can be disabled from settings, but console logging is permanent.

When an error occours during runtime, the error will be displayed to the user in a pop-up window. If it happens during loading a panel, the WindowHandler will check if the panel exists. Because each panel with exception possibility has `destroy()` being used on them when exception happens. So, panel should not exists. This makes checking state of current panel easier. Then we use `cache.py` to get the last panel that user were on. 

`cache.py` file contains panels in a array field. I decided to make this array look like a queue. This is best for return operations only.

Debug window only displays the real-time logs and can't be closed unless value is changed from settings.

## Python
- Python version 3.* must be installed
### Required Libraries
- python3-tk (tkinter UI library)
- socket
- netifaces (displaying network interfaces)
- ntplib (SNTP time module to retrieve remote time information)
- json (saving settings file)

## Run the application
From the root folder of the application, run:
```python
python3 App.py
```
You can replace **python3** with **phyton** if you have a different installation.

## Project Structure

```mermaid
flowchart LR
    Root["NP_PROJECT_1"]
    Root --> App["App.py"]
    Root --> Logger["logger.py"]
    Root --> SettingsJson["settings.json"]
    Root --> GUI["gui/"]
    Root --> Logic["logic/"]

    GUI --> Components["components/"]
    Components --> C_Back["BackButton.py"]
    Components --> C_Chat["ChatButton.py"]
    Components --> C_Dev["DeviceInfoButton.py"]
    Components --> C_Echo["EchoTestButton.py"]
    Components --> C_Menu["MenuButtons.py"]
    Components --> C_Time["RetrieveTimeButton.py"]
    Components --> C_Set["SettingsButton.py"]

    GUI --> Frames["frames/"]
    Frames --> F_Main["Main.py"]
    Frames --> F_Debug["DebugFrame.py"]

    GUI --> Panels["panels/"]
    Panels --> P_Chat["ChatPanel.py"]
    Panels --> P_ChatCC["ChatClientConnectPanel.py"]
    Panels --> P_ChatCP["ChatClientPanel.py"]
    Panels --> P_ChatSP["ChatServerPanel.py"]
    Panels --> P_Echo["EchoPanel.py"]
    Panels --> P_EchoCT["EchoClientTestPanel.py"]
    Panels --> P_EchoST["EchoServerTestPanel.py"]
    Panels --> P_Info["InfoPanel.py"]
    Panels --> P_MainB["MainButtonSetPanel.py"]
    Panels --> P_Time["RetrieveTimePanel.py"]
    Panels --> P_Set["SettingsPanel.py"]

    Logic --> L_CC["ChatClient.py"]
    Logic --> L_CS["ChatServer.py"]
    Logic --> L_DLH["DebugLogHandler.py"]
    Logic --> L_DI["DeviceInfo.py"]
    Logic --> L_ECT["EchoClientTest.py"]
    Logic --> L_EST["EchoServerTest.py"]
    Logic --> L_GEDH["GlobalErrorDisplayHandler.py"]
    Logic --> L_GEH["GlobalExceptionHandler.py"]
    Logic --> L_Set["Settings.py"]
    Logic --> L_SNTP["SNTP.py"]
    Logic --> L_WH["WindowHandler.py"]
    Logic --> L_Cache["cache.py"]

    click App "./App.py"
    click Logger "./logger.py"
    click SettingsJson "./settings.json"

    click GUI "./gui"
    click Components "./gui/components"
    click C_Back "./gui/components/BackButton.py"
    click C_Chat "./gui/components/ChatButton.py"
    click C_Dev "./gui/components/DeviceInfoButton.py"
    click C_Echo "./gui/components/EchoTestButton.py"
    click C_Menu "./gui/components/MenuButtons.py"
    click C_Time "./gui/components/RetrieveTimeButton.py"
    click C_Set "./gui/components/SettingsButton.py"

    click Frames "./gui/frames"
    click F_Main "./gui/frames/Main.py"
    click F_Debug "./gui/frames/DebugFrame.py"

    click Panels "./gui/panels"
    click P_Chat "./gui/panels/ChatPanel.py"
    click P_ChatCC "./gui/panels/ChatClientConnectPanel.py"
    click P_ChatCP "./gui/panels/ChatClientPanel.py"
    click P_ChatSP "./gui/panels/ChatServerPanel.py"
    click P_Echo "./gui/panels/EchoPanel.py"
    click P_EchoCT "./gui/panels/EchoClientTestPanel.py"
    click P_EchoST "./gui/panels/EchoServerTestPanel.py"
    click P_Info "./gui/panels/InfoPanel.py"
    click P_MainB "./gui/panels/MainButtonSetPanel.py"
    click P_Time "./gui/panels/RetrieveTimePanel.py"
    click P_Set "./gui/panels/SettingsPanel.py"

    click Logic "./logic"
    click L_CC "./logic/ChatClient.py"
    click L_CS "./logic/ChatServer.py"
    click L_DLH "./logic/DebugLogHandler.py"
    click L_DI "./logic/DeviceInfo.py"
    click L_ECT "./logic/EchoClientTest.py"
    click L_EST "./logic/EchoServerTest.py"
    click L_GEDH "./logic/GlobalErrorDisplayHandler.py"
    click L_GEH "./logic/GlobalExceptionHandler.py"
    click L_Set "./logic/Settings.py"
    click L_SNTP "./logic/SNTP.py"
    click L_WH "./logic/WindowHandler.py"
    click L_Cache "./logic/cache.py"
```
