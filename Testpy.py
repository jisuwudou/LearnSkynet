import struct

data = struct.pack('BB', 2,3)


def test(data):
	print(id(data))

	data = data[1]
	print("in test()",data, id(data))

print(data, id(data))

test(data)
print(data)


a = 4

print(a & 0x1,a & (1 << 2))