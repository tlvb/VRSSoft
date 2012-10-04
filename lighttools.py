def lg2(x):
	y = 0
	while not x & 1:
		y += 1
		x >>= 1
	return y

def mk_changeset(old, new):
	changeset = [None] * len(old)
	for i in range(len(old)):
		if new[i] != old[i]:
			changeset[i] = new[i]
	return changeset

def mk_command(ctype, start=None, length=None):
	if ctype == 'channel':
		return [0, 64, 96, 112, 120, 124, 126][lg2(length)] + start
	elif ctype == 'reset':
		return 128
	elif ctype == 'limbo':
		return 129
	elif ctype == 'ok':
		return 130
	else:
		return 255


def mk_chain(new, start, length):
	return ["change({}, {}, {})".format(start, length, mk_command('channel', start, length))] + new[start:start+length]

def find_opt_comchain(changeset, new, start, length):
	if length > 1:
		print("> {} {}".format(start,length))
		comchain0 = mk_chain(new, start, length)
		comchain1 = find_opt_comchain(changeset, new, start, length>>1)
		comchain2 = find_opt_comchain(changeset, new, start+(length>>1), length>>1)
		print("cc0: ",comchain0)
		print("cc1: ",comchain1)
		print("cc2: ",comchain2)
		if len(comchain0) < len(comchain1) + len(comchain2):
			return comchain0
		else:
			return comchain1 + comchain2
	else:
		if changeset[start] != None:
			return mk_chain(new, start, length) 
		else:
			return []

if __name__ == '__main__':

	import sys

	print("#ifndef {}".format(sys.argv[1]))
	print("#define {}".format(sys.argv[1]))
	print("/* automatically generated from 'python {} {}' */".format(sys.argv[0], sys.argv[1]))

	for i in range(64):
		print("#define PR_G1_{} {}".format(i, mk_command('channel', i, 1)))
	for i in range(32):
		print("#define PR_G2_{} {}".format(i, mk_command('channel', i, 2)))
	for i in range(16):
		print("#define PR_G4_{} {}".format(i, mk_command('channel', i, 4)))
	for i in range(8):
		print("#define PR_G8_{} {}".format(i, mk_command('channel', i, 8)))
	for i in range(4):
		print("#define PR_G16_{} {}".format(i, mk_command('channel', i, 16)))
	for i in range(2):
		print("#define PR_G32_{} {}".format(i, mk_command('channel', i, 32)))
	for i in range(1):
		print("#define PR_G64_{} {}".format(i, mk_command('channel', i, 64)))
	print("#define PR_RESET {}".format(mk_command('reset')))
	print("#define PR_LIMBO {}".format(mk_command('limbo')))
	print("#define PR_OK {}".format(mk_command('ok')))

	print("#endif")





