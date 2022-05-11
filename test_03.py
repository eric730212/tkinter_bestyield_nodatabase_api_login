import serial

ser = serial.Serial('COM11', 9600,timeout=0.5)

while ser.readline()!=b'':
    print(ser.readline())
    ser.readline()
    ser.readline()
    print("00000")