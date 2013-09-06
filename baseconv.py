def dice_to_10(s, num_faces):
	""" Decodes the result of throwing a <num_faces>-sided dice into a base 10 number """
	alphabet = get_alphabet(num_faces)
	decoded = 0
	multi = 1
	s = s[::-1]
	for char in s:
		#try:
		decoded += multi * alphabet.index(char)
		#except ValueError:
		#	raise ValueError("'%s' is not a valid throw for a dice with %d faces" %\
		#		(char, num_faces))
			
		multi = multi * num_faces
		
	return decoded

def get_alphabet(num_faces):
	return [str(i) for i in range(1,num_faces+1)]

if __name__ == "__main__":
	#tests
	from testvectors import *

	assert dice_to_10(*base6_test['throws']) == base6_test['base10']
	assert dice_to_10(*base10_test['throws']) == base10_test['base10']
	assert dice_to_10(*base20_test['throws']) == base20_test['base10']
