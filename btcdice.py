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

class _Getch:
	"""Gets a single character from standard input.  Does not echo to the
screen."""
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self): return self.impl()


class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()

import sys
from bitcoin import key as ecdsa
from bitcoin import base58
import hashlib
import Crypto.Hash.SHA256 as sha256
import argparse
import math

def decode(s, base):
	""" Decodes the base<n>-encoded string s into an integer """
	alphabet = [hex(i).lstrip('0x') for i in range(1,base+1)]
	decoded = 0
	multi = 1
	s = s[::-1]
	for char in s:
		decoded += multi * alphabet.index(char)
		multi = multi * base
		
	return decoded

def dsha256(s):
	return sha256.new(sha256.new(s).digest()).digest()
 
def rhash(s):
	h1 = hashlib.new('ripemd160')
	h1.update(hashlib.sha256(s).digest())
	return h1.digest()

def base58_check_encode(s, version=0):
	vs = chr(version) + s
	check = dsha256(vs)[:4]
	return base58.encode(vs + check)

def get_addr(k):
	pubkey = k.get_pubkey()
	secret = k.prikey
	hash160 = rhash(pubkey)
	addr = base58_check_encode(hash160)
	payload = secret
	pkey = base58_check_encode(payload, 128)
	return addr, pkey

def main():
	parser = argparse.ArgumentParser(description="Generate a Bitcoin private key using a dice.")
	parser.add_argument("--faces", type=int, default=6, help="specify the number of faces on your dice")
	parser.add_argument("--entropy", type=int, default=256, help="desired amount of entropy (in bits)")
	args = parser.parse_args()

	#calculate how many throws we need to reach the desired amount of entropy
	entropy_per_throw = math.log(args.faces, 2)
	THROWS = int(math.ceil(args.entropy / entropy_per_throw))

	alphabet = [hex(i).lstrip('0x') for i in range(1,args.faces+1)]

	getch = _Getch()

	print "Throw a dice %d times. After each throw, enter the value thrown..." % (THROWS)
	print "Press Ctrl+C if you want to exit at any point"

	if args.faces > 9:
		print """\nNote: The following characters represent the respective
faces on the dice:"""
		for char, face in zip(alphabet, [str(i) for i in range(1,args.faces+1)]):
			print "\t%s: %s" % (char, face)

	result = []
	for i in range(0,THROWS):
		while True:
			sys.stdout.write("\nDice throw %d out of %d: " % (THROWS, i+1))
			char = getch()

			#exit on Ctrl+C
			if ord(char) == 3:
				sys.exit()

			sys.stdout.write(char)

			if char not in alphabet:
				sys.stdout.write("\nSorry. Not a valid throw. Try again.")
				continue

			if ord(char) != 3:
				result.append(char)
				break

	print "\n"

	num = decode(result, args.faces)
	secret = hex(num).lstrip('0x').rstrip('L')[0:64].ljust(64, '0').decode('hex')

	key = ecdsa.CKey()
	key.generate(secret)

	addr,pkey = get_addr(key)

	print "Address: %s" % (addr)
	print "Private key: %s" % (pkey)


if __name__ == "__main__":
	main()
