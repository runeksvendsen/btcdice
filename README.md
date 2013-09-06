btcdice
=======


Generate a Bitcoin private key and its corresponding
address from throwing a dice.

Borrows code from:	http://code.activestate.com/recipes/134892/
							
Depends on: https://github.com/jgarzik/python-bitcoinlib

Installation:

	1. Clone the above github repository.
	2. Place this script inside the created folder (python-bitcoinlib)

Usage:

	Simply run the script and start throwing your dice. After every
	throw enter the result on the screen. Repeat 100 times for 256 bits
	of entropy with a dice with six faces.

Options:

	`--faces`
	With the `--faces` option you can specify how many sides your dice
	has. This will automatically adjust the number of required throws
	to produce 256 bits of entropy by default.

	`--entropy`
	The amount of required entropy can be changed using the `--entropy`
	option.
