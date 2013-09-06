#!/usr/env python

"""Generate a Bitcoin private key and its corresponding
address from throwing a dice.

Borrows code from:
	http://code.activestate.com/recipes/134892/
	https://gist.github.com/josephdunn/5347612/
							
Depends on: https://github.com/jgarzik/python-bitcoinlib

Installation:

	1. Clone the above github repository.
	2. Place this script inside the created folder (python-bitcoinlib)

Usage:

	Simply run the script and start throwing your dice. After every
	throw enter the result on the screen. Repeat 100 times for 256 bits
	of entropy."""

import sys
import argparse
import math
from getch import _Getch
import privaddr
from baseconv import get_alphabet

def getch_print(getch):
	char = getch()
	sys.stdout.write(char)
	return char

def main():
	parser = argparse.ArgumentParser(description="Generate a Bitcoin private key using a dice.")
	parser.add_argument("--faces", type=int, default=6, help="specify the number of faces on your dice")
	parser.add_argument("--entropy", type=int, default=256, help="desired amount of entropy (in bits)")
	args = parser.parse_args()

	#calculate how many throws we need to reach the desired amount of entropy
	entropy_per_throw = math.log(args.faces, 2)
	THROWS = int(math.ceil(args.entropy / entropy_per_throw))

	alphabet = get_alphabet(args.faces)

	getch = _Getch()

	print("Throw a dice %d times. After each throw, enter the value thrown..." % (THROWS))
	print("Press Ctrl+C if you want to exit at any point")

	result = []
	for i in range(0,THROWS):
		while True:
			sys.stdout.write("\nDice throw %d out of %d: " % (i+1, THROWS))
			
			char = getch_print(getch)

			#exit on Ctrl+C
			if ord(char[0]) == 3:
				sys.exit()

			if args.faces >= 10:
				char += getch_print(getch)

			char = char.rstrip('\r')

			try:
				char = str(int(char)) #strip any leading zeros
			except ValueError:
				pass

			if char not in alphabet:
				sys.stdout.write("\nSorry. Not a valid throw. Try again.")
				continue

			result.append(char)
			break

	print("\n")

	addr,pkey = privaddr.throws_to_keyaddr(result, args.faces)

	print("Address: %s" % (addr))
	print("Private key: %s" % (pkey))

if __name__ == "__main__":
	main()
