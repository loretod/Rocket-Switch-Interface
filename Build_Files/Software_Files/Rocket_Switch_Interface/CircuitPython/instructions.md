# CircuitPython Firmware Installation

To install the CircuitPython Code:

1. Download the following file:

- code.py

As of CircuitPython 10, the adafruit_hid library is built in. If working with older verions, you will need to download and place the following folder in the CIRCUITPY lib folder.
- adafruit_hid folder

2. If you haven't installed CircuitPython to the board previously, double-click the reset button on the board to enter bootloader mode. Drag the .uf2 files into the BOOT drive that appears.

3. Drag and drop the code.py file into the drive.

To customize the HID commands sent for each switch press: 
1. open the **rocket-switch-configurator.html** file in the browser of your choice.

2. Select the desired command for each switch. First selecting the desired HID type (keyboard, media control, or mouse action) the the desired action.

3. Press the download button and a config.py file will generate in the default download location on your computer.

4. Drag and drop the config.py file into the CIRCUITPY drive.

You may need to press the reset button to activate the changes.