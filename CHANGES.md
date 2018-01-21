# uPiot Release Notes

## Version 0.1.6-alpha | 21 Jan 2018

#### Improvements

* Connect the console when a command is run and it's not connected (in missing commands)
* Minor code improvement writing code in a file

#### Bugs

* Bug fix cleaning a retrieved line

## Version 0.1.5-alpha | 21 Jan 2018

#### New

* Added feedback in the statusbar while the command is running
* Runs selected code (Issue: https://github.com/gepd/uPiotMicroPythonTool/issues/4)

#### Improvements

* Opens the console when a command is ran it's closed
* Make sure to always download the given file, even if it already exists
* pyboard has been renamed and refactorized to repl to organize and improve the way to work with the device
* Absolute path in make and remove folder was removed to improve the compatibility with more devices and firmwares.
* Added more feedback when there is a problem opening the console or a problem running a command.
* The sync functions shows the name of the file retrieving in realtime.

## Version 0.1.4-alpha | 12 Nov 2017

#### New

* New --close command

#### Improvements

* make the write console command only available when there is a port connected removed stablish connection.
* The main serial instance is passed to sampy to avoid multiples connect and disconnect, it may solve a problem in Linux dtr and rts are disabled before make the connection in the serial port to fix a problem with linux
* Workaround to remove the status bar color, when it wasn't closed before exit from ST
* Show a red color in the status bar when the serial instance is destroyed/closed

#### Bugs

* Fix serial listener after run a sampy command
* Fix destroying serial session when console window is closed
* Linux serial fixes
* Fixed --help command
* Other minor bug fixes

## Version 0.1.3-alpha | 06 Nov 2017

#### New

* First implementation to show a color in the status bar when a serial connection is established in a port

#### Improvements

* When the console is closed, it will destroy/close the group panel if it's empty

#### Bugs

* Fix bug make not work all commands except for "sampy run" introduced in https://github.com/gepd/uPiotMicroPythonTool/commit/6ceba526b00f3812b4e64d9ae0f0187cbaaae9a2
* Fixed --help command

## Version 0.1.2-alpha | 04 Nov 2017

#### New

* Command to send a cancel string (\x03) through the serial port including a shortcut (ctrl+shift+c).

#### Improvements

* Avoid to send empty string to the console when it's waiting for new data
* Activate the window console each time it's open or called from a sampy command.
* Warn the user to restart ST after uPiot is updated.
* 'sampy run' will now display the output in realtime.

#### Bugs

* Removed hardcoded strings to burn the firmware in other boards.
* Fix console call when multiples boards are connected (Issue: #1).


## Version 0.1.1-alpha | 28 Oct 2017

#### Improvements

* Display an error when the serial port is busy.
* Display an error when serial port loses the connection.

#### Bugs

* Clear serial input and output before listen new data to avoid undesirable characters.
* Fixed problem to enter to the raw REPL when the board has just been connected.

#### Others

* Fix github url in console header.

## Version 0.1.0-alpha | 27 Oct 2017

* First alpha release