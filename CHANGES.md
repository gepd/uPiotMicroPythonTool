# uPiot Release Notes

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