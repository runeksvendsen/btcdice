import hashlib
import Crypto.Hash.SHA256 as sha256

from bitcoin import key as ecdsa
from bitcoin import base58
from baseconv import dice_to_10

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

def num_to_secret(num):
	return hex(num).lstrip('0x').rstrip('L')[0:64].ljust(64, '0').decode('hex')

def throws_to_keyaddr(throws, faces):
	num = dice_to_10(throws, faces)
	secret = num_to_secret(num)

	key = ecdsa.CKey()
	key.generate(secret)

	addr,pkey = get_addr(key)

	return (addr,pkey)

if __name__ == "__main__":
	#tests
	from testvectors import *

	assert throws_to_keyaddr(*base6_test['throws']) == (base6_test['address'], base6_test['privkey'])
	assert throws_to_keyaddr(*base10_test['throws']) == (base10_test['address'], base10_test['privkey'])
	assert throws_to_keyaddr(*base20_test['throws']) == (base20_test['address'], base20_test['privkey'])
