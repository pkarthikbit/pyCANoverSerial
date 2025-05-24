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

def can_send(tx_canid, tx_data):
    TxValue = 'AA 00 00 00 00 08'+ tx_canid + tx_data + 'BB'
    TxValue = bytes.fromhex(TxValue)
    ser.write(TxValue)
    can_receive('00 00 07 e8')

def can_receive(rx_canid):
    RxValue = ser.read(19)         
    if (rx_canid == RxValue.hex(' ')[18:29]):
        if('04 41' == RxValue.hex(' ')[30:35]):
            #PID0C 2 bytes Engine speed 	0 	16,383.75 	rpm 
            if('0c' == RxValue.hex(' ')[36:38]):
                pid_val = (int(RxValue.hex(' ')[39:44].replace(" ", ""), 16)) /4
                print('Engine speed = ', pid_val, 'rpm')

for i in range(10):
    #PID0C 2 bytes Engine speed 	0 	16,383.75 	rpm 
    can_send('00 00 07 e0', '02 01 0C 55 55 55 55 55')
    


ser.close()             # close port
