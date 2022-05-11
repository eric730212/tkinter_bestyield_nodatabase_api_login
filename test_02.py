import serial

while True:
    ser = serial.Serial('COM11',9600,timeout=None)
    read_buffer = b''

    while True:
        print(ser.readline())
        byte_chunk = ser.read(20)
        read_buffer+=byte_chunk
        print(read_buffer)
        if len(read_buffer)>200:
            read_buffer=b''
            print(("111111111111111111111111111"))
        if not len(byte_chunk) == 20:
            break;
        print(("00000000000000000000000000"))

    print("break")