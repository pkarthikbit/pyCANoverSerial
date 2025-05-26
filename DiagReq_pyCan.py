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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('/dev/ttyUSB0', 115200)  # open serial port

# Parameters
x_len = 200         # Number of points to display
y_range = [0, 7000]  # Range of possible Y values to display
graph_val = 0

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('Engine speed over Time')
plt.xlabel('Samples')
plt.ylabel('Engine speed (rpm)')

# This function is called periodically from FuncAnimation
def animate(i, ys):
    #PID0C 2 bytes Engine speed 	0 	16,383.75 	rpm 
    retVal = can_send('00 00 07 e0', '02 01 0C 55 55 55 55 55')
    temp_c = round(retVal, 4)
    temp_f=(temp_c*9/5)+32
    # Add y to list
    ys.append(temp_f)
    # Limit y list to set number of items
    ys = ys[-x_len:]
    # Update line with new Y values
    line.set_ydata(ys)
    return line,

def can_send(tx_canid, tx_data):
    TxValue = 'AA 00 00 00 00 08'+ tx_canid + tx_data + 'BB'
    TxValue = bytes.fromhex(TxValue)
    ser.write(TxValue)
    retVal = can_receive('00 00 07 e8')
    return retVal

def can_receive(rx_canid):
    RxValue = ser.read(19)         
    if (rx_canid == RxValue.hex(' ')[18:29]):
        if('04 41' == RxValue.hex(' ')[30:35]):
            #PID0C 2 bytes Engine speed 	0 	16,383.75 	rpm 
            if('0c' == RxValue.hex(' ')[36:38]):
                pid_val = (int(RxValue.hex(' ')[39:44].replace(" ", ""), 16)) /4
                return pid_val

ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
plt.show()

ser.close()             # close port
