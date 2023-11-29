import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, source, encode=True, keyType = 'hex'):
	source = source.encode()
	if keyType == "hex":
		 # Convert key (in hex representation) to bytes 
		key = bytes(bytearray.fromhex(key))
	# generate IV
	IV = Random.new().read(AES.block_size)
	# Create AES encryptor object
	encryptor = AES.new(key, AES.MODE_CBC, IV)
	padding = AES.block_size - len(source) % AES.block_size
	# Apply padding
	source += bytes([padding]) * padding
	data = IV + encryptor.encrypt(source)
	return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True,keyType="hex"):
	source = source.encode()
	if decode:
		source = base64.b64decode(source)

	if keyType == "hex":
		# Convert key to bytes
		key = bytes(bytearray.fromhex(key))
	# Extract IV
	IV = source[:AES.block_size]
	# Create AES decryptor object
	decryptor = AES.new(key, AES.MODE_CBC, IV)
	# Decrypt
	data = decryptor.decrypt(source[AES.block_size:])
	padding = data[-1]
	if data[-padding:] != bytes([padding]) * padding:
		raise ValueError("Invalid padding...")
	return data[:-padding]