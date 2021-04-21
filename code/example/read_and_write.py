'''并联机器人通信示例程序'''
import serial
import time

ser = serial.Serial('/dev/ttyUSB1',9600,8,'E',1)
ser.flushInput()  # 清空缓冲区

flag = ser.is_open
if(flag):
    print("success\n")
    # ser.close()
else:
    print("Open Error\n")
ser.flushInput()  # 清空缓冲区
ser.write(b'\x01\x10\x00\x08\x00\x05\n\x00\x00\xfc\x18\xf0`\x00\x00\x00\x00\x0b\xd8')
# ser.write(b'\x01\x03\x00\x08\x00\x05\x04\x0B')
# ser.write(b'\x01\x10\x00\x08\x00\x05\x0A\x00\x00\xFC\x18\xF0\x60\x00\x00\x00\x00\x0B\xD8')
time.sleep(0.05) # 延时50ms
count = ser.inWaiting() # 获取串口缓冲区数据
if(count != 0):
    print(ser.read(ser.in_waiting))# 读出串口数据