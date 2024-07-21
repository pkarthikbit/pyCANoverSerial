# pyCANoverSerial

It is a Serial communication based low cost Canalyzer compatible with Windows and Linux. Based on https://python-can.readthedocs.io/en/stable/interfaces/serial.html, the serial format is adapted as,
```
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
```
**Hardware setup:**
- STM32F103C8T6 (bluepill_f103c8)
- TJA1050

CAN-Interface
-------------
```
/* CAN1 / CAN GPIO */
CAN_PB_RX   PB8
CAN_PB_TX   PB9
```

Flashing Serial
---------------
using SWD interface with st-flash or serial loader stm32-flash (works only with USART1)

For programming BluePill:
1. Install stm32 cube programmer
2. Do the below for Linux
```
cd /dev
sudo chown <user> ttyUSB0
```
3. Connect the UART and it works
```
/* USART1 GPIO */
USART1_TX   PA9 
USART1_RX   PA10
```

Debugging
-----
connect your favorite/cheap 3V3 USB2Serial board to USART2:
```
/* USART2 GPIO */
USART2_CTS  PA0
USART2_RTS  PA1
USART2_TX   PA2
USART2_RX   PA3
```
USB
-----
```
USB-    PA11
USB+    PA12
```
**Python script to test:**
```
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
```
