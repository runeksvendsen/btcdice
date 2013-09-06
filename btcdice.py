#!/usr/env python

"""Generate a Bitcoin private key and its corresponding
address from throwing a dice.

Borrows code from:	http://code.activestate.com/recipes/134892/
							
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

alphabet = '123456'
base_count = len(alphabet)
THROWS = 100

def decode(s):
	""" Decodes the base6-encoded string s into an integer """
	decoded = 0
	multi = 1
	s = s[::-1]
	for char in s:
		decoded += multi * alphabet.index(char)
		multi = multi * base_count
		
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

getch = _Getch()

print "Throw a dice %d times. After each throw, enter the value thrown..." % (THROWS)
print "Press Ctrl+C if you want to exit at any point"

result = ""
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
			result += char
			break

print "\n"

num = decode(result)
secret = hex(num).lstrip('0x').rstrip('L')[0:64].ljust(64, '0').decode('hex')

key = ecdsa.CKey()
key.generate(secret)

addr,pkey = get_addr(key)

print "Address: %s" % (addr)
print "Private key: %s" % (pkey)