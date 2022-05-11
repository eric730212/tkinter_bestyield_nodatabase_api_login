import serial.tools.list_ports

a = [1, 2, 3, 2, 1, 5, 6, 5, 5, 5]
b = [1, 2, 3, 4, 5]
seen = set()
duplicated = set()
print(seen)
print(duplicated)

for x in b:
    if x not in seen:
        seen.add(x)
    else:
        duplicated.add(x)
print(seen)
print(duplicated)

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    if "Comm Port" in p.description:
        COM_PORT = p.description[34:39]
        print(COM_PORT)
        print((p.description.split("(")[-1]).split(")")[0])


