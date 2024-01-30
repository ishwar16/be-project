import json

file = open('test.json')
data = json.load(file)

file2 = open(data['filename'], "w")
d = data['content']
print(d)
file2.write(d)
file2.close()

print(data)
file.close()