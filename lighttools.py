class Device:
	def __init__(self, devfile):
		self.wfd = open(devfile, 'w')
		self.rfd = open(devfile, 'r')
	def write(self, stuff):
		self.wfd.write(stuff)
	def close(self):
		if not self.wfd.closed:
			self.wfd.close()
		if not self.rfd.closed:
			self.rfd.close()

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
	return chr(mk_command('channel', start, length)) + ''.join(chr(x) for x in new[start:start+length])

def find_opt_comchain(changeset, new, start, length):
	if length > 1:
		comchain0 = mk_chain(new, start, length)
		comchain1 = find_opt_comchain(changeset, new, start, length>>1)
		comchain2 = find_opt_comchain(changeset, new, start+(length>>1), length>>1)
		if len(comchain0) < len(comchain1) + len(comchain2):
			return comchain0
		else:
			return comchain1 + comchain2
	else:
		if changeset[start] != None:
			return mk_chain(new, start, length) 
		else:
			return ''

def mk_comchain(old, new):
	changeset = mk_changeset(old, new)
	return find_opt_comchain(changeset, new, 0, len(changeset))

if __name__ == '__main__':

	o = [1,2,3,4,5,6,7,8]
	n = [7,3,2,4,5,6,9,8]
	c = mk_comchain(o, n)
	print(repr(c))






