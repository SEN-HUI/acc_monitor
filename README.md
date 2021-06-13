# Powered Exoskeleton Monitor

A GUI to receive and visualize real-time data from a powered exoskeleton device.

## Prerequisites
- [python 3](https://www.python.org/)

## Installation
### Windows
#### Install the project
1. Open a Command Prompt and navigate to a directory where you want to store the project.
2. Type the following commands.
	```
	git clone https://github.com/SEN-HUI/acc_monitor.git
	cd acc_monitor
	py -m venv acc_monitor_env
	.\acc_monitor_env\Scripts\activate.bat
	py -m pip install -r requirements.txt
	```
#### Install the app
Download and extract the archive [Windows installer](dist/installers/acc_monitor_win.tar.gz)


## Usage
### Windows
#### Run from source code

1. Open a Command Prompt and navigate the project root directory.
2. Type the following commands.

	```
	.\acc_monitor_env\Scripts\activate.bat
	py src\acc_monitor\index.py
	```
#### Run the execuable
Run `index.exe` under the extracted archive root directory.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
