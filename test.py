import pickle
import json

from engine import handler



t_data = handler.Object


obj = handler.Object()


bytes_data = pickle.dumps(obj, protocol=4)

string_data = str(bytes_data)

print(string_data)
print(bytes_data.hex())

with open("test1.json", 'w') as file:
    json.dump({"test": bytes_data.hex()}, file)
    file.close()


opened = None
with open("test1.json", 'r') as file:
    opened = json.load(file)
    file.close()

decode_byte = bytes.fromhex(opened["test"])
print(decode_byte)

print(decode_byte == bytes_data)