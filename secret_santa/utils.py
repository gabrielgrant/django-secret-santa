from hashlib import sha1

def make_key(name, password):
	unhashed_key = ':'.join([name, password])
	key = sha1(unhahsed_key).hexdigest()
	return key
