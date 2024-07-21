# Ref: https://python-can.readthedocs.io/en/stable/interfaces/serial.html
# +=============+===============+========================+=========================+=========================+=========+==============+
# |    Desc     |Start of frame |Timestamp               | DLC                     | Arbitration ID          | Payload | End of frame |
# +=============+===============+========================+=========================+=========================+=========+==============+
# |Length (Byte)|1              |4                       | 1                       | 4                       | 8       | 1            |
# +-------------+---------------+------------------------+-------------------------+-------------------------+---------+--------------+
# |Data type    |Byte           |Unsigned 4 byte integer | Unsigned 1 byte integer | Unsigned 4 byte integer | Byte    | Byte         |
# +-------------+---------------+------------------------+-------------------------+-------------------------+---------+--------------+
# |Byte order   |-              |Big-Endian              | Big-Endian              | Big-Endian              | -       | -            |
# +-------------+---------------+------------------------+-------------------------+-------------------------+---------+--------------+
# |Value        |0xAA           |Usually s, ms or µs     | Payload Length in byte  | -                       | -       | 0xBB         |
# +-------------+---------------+------------------------+-------------------------+-------------------------+---------+--------------+

import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)  # open serial port
print(ser.baudrate)         # check which port was really used

for i in range(10):
    # receive from CAN
    RxValue = ser.read(19)         
    print(RxValue.hex(' '))
    # send in CAN
    TxValue = 'AA 00 00 00 00 02 00 00 07 e0 11 22 33 44 55 66 77 88 BB'
    TxValue = bytes.fromhex(TxValue)
    ser.write(TxValue)
    print(TxValue.hex(' '))
ser.close()             # close port