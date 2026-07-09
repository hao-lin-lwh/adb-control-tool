# Android Automation Assistant V2

A PyQt5-based Android device automation control tool that implements device control and script execution functions through ADB commands.

## Features

### Device Management
- **Auto-detect devices**: Automatically detect connected Android devices on startup
- **Device selection**: Support multi-device switching
- **Real-time status display**: Show device connection status

### Script Editor
- **Command editing**: Support manual input of ADB commands
- **Double-click editing**: Double-click commands to edit quickly
- **Script save/load**: Support saving and loading script files

### Key Simulation
- Power key, Volume+, Volume-
- Home key, Back key, Menu key
- Confirm key, Delete key

### Touch Simulation
- Single tap
- Long press (1 second)
- Swipe up, down, left, right

### System Control
- Screenshot (save to /sdcard/screen.png)
- Screen recording (save to /sdcard/record.mp4)
- Reboot device
- Power off
- Enter Fastboot mode

### App Control
- Launch system apps like Browser and Settings
- List all installed applications
- Clear app cache

### Advanced Features
- **Command delay**: Automatically insert 1-second delay between commands
- **Batch execution**: Support executing multiple commands at once
- **Execution statistics**: Show success/failure command count

## Requirements

### System Requirements
- Windows 10/11
- Python 3.6+

### Dependencies
```bash
pip install PyQt5
```

### ADB Tool
- Download and install Android SDK Platform Tools
- Add `platform-tools` directory to system PATH
- Ensure ADB is available: `adb devices` command should work

## Usage

### 1. Start the Program
```bash
python main.py
```

### 2. Connect Device
- Connect Android device via USB
- Enable "Developer Options" and "USB Debugging" on the device
- Confirm device is connected: `adb devices`

### 3. Select Device
- Select device from the dropdown at the top of the program
- Status bar will show connection status

### 4. Execute Commands
#### Method 1: Use Quick Buttons
- Click quick buttons on the right panel to automatically insert ADB commands into the editor
- Enable "Insert 1-second delay after all commands" to add delay

#### Method 2: Manually Edit Script
- Enter ADB commands directly in the editor
- Format: `adb -s <device_serial> shell <command>`

### 5. Save and Load Script
- Click "Save Script" to save script to file
- Click "Load Script" to read saved script

### 6. Execute Script
- Click "▶ Execute Script" button
- Program will execute commands in the script line by line
- Show execution result statistics

## Command Examples

### Basic Keys
```
adb -s <device_id> shell input keyevent 26    # Power key
adb -s <device_id> shell input keyevent 3    # Home key
```

### Touch Operations
```
adb -s <device_id> shell input tap 500 800    # Tap at (500, 800)
adb -s <device_id> shell input swipe 500 800 500 300 1000  # Swipe up
```

### Screenshot
```
adb -s <device_id> shell screencap /sdcard/screen.png
```

### Screen Record
```
adb -s <device_id> shell screenrecord /sdcard/record.mp4
```

### Launch App
```
adb -s <device_id> shell am start -a android.intent.action.VIEW -d https://www.baidu.com
```

## Notes

1. **Device Connection**: Ensure USB debugging is enabled on the device
2. **Permission Issues**: Some operations require device root access
3. **Script Execution**: Ensure device is unlocked when executing scripts
4. **Delay Setting**: After enabling "Auto delay", each command will automatically wait 1 second
5. **ADB Environment Variable**: Ensure ADB is correctly installed and added to system PATH

## Project Structure

```
adb-control-tool-git/
├── main.py           # Main program file
├── README.md         # Project documentation (Chinese)
├── README_EN.md      # Project documentation (English)
└── .git/             # Git repository
```

## FAQ

### Q: Prompt "No devices detected"?
A: Check if USB debugging is enabled on the device, or try reconnecting the device.

### Q: How to view device serial number?
A: Type `adb devices` in command line, the first column is the device serial number.

### Q: Script execution failed?
A: Check command syntax, ensure device is connected and unlocked.

### Q: How to get device screen coordinates?
A: Use "Show touch operations" in Developer Options on the device.

## License

MIT License

## Author

hao-lin-lwh
