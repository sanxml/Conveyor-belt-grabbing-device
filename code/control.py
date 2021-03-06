'''并联机器人控制示例程序'''
import serial
import time
from binascii import unhexlify
from crcmod import mkCrcFun

def coordinate_read():
    '''对坐标进行读操作'''
    write_data = b'\x01\x03\x00\x08\x00\x05\x04\x0B'

    read_data = serial_operation(write_data).hex()
    read_data_copy = read_data[:-4]
    read_data_copy = crc16_modbus(read_data_copy).hex()
    read_data_dict = {'x':0, 'y':0, 'z':0, 'a':0, 'v':0, 's':0}
    if(read_data_copy != read_data):
        return -1

    read_data = read_data[6:-4]
    for index in range(4):
        single_data = int(read_data[index*4:(index+1)*4],16)
        if(single_data>10000):
            single_data = single_data-2**16
        if(index == 0):
            read_data_dict['x'] = single_data/10
        elif(index == 1):
            read_data_dict['y'] = single_data/10
        elif(index == 2):
            read_data_dict['z'] = single_data/10
        elif(index == 3):
            read_data_dict['a'] = single_data/10
    read_data_dict['v'] = read_data[-3:-2]
    read_data_dict['s'] = read_data[-1:]
    # int(read_data[:4],16)
    print(read_data_dict)
    return read_data_dict

def coordinate_write(x=0, y=0, z=0, a=0, v=0, s=0):
    '''对坐标进行写操作

    x-x坐标值，y-y坐标值，z-z坐标值，a-角度值，v-吸盘速度值， s-吸盘状态值

    x, y取值范围：  -200.0 ～ 200.0；
    z取值范围：     -460.0 ～ -290.0；
    a取值范围：     -180.0 ～ 180.0；
    v取值范围：     0 ～ 9 (其中 0 为最快速度，9 为最慢速度)；
    s取值范围：     0 or 1 (0 为释放，1 为吸气状态coordinate_write_seven(P1,P2,P3,P4,P5,P6,P7))；
    '''
    write_data = "0110000800050a"
    if(-200<=x<=200 and -200<=y<=200 and -460<=z<=-290 and -180<=a<=180 and 0<=v<=9 and 0<=s<=1):
        write_data = write_data + inverse_code(int(x*10)) + inverse_code(int(y*10))  + inverse_code(int(z*10))  + inverse_code(int(a*10)) + '0' + str(v) + '0' + str(s)
        # print(write_data)
        write_data = crc16_modbus(write_data)
        # print(write_data)
        return serial_operation(write_data)
    else:
        print("Invalid input value")
        return -1

def coordinate_write_seven(list1,list2,list3,list4,list5,list6,list7):
    '''对7个坐标进行写操作

    输入7组元组数据， list[1]-x坐标值，list[2]-y坐标值，list[3]-z坐标值，list[4]-角度值，list[5]-吸盘速度值， list[6]-吸盘状态值

    list[1], list[2]取值范围：  -200.0 ～ 200.0coordinate_write_seven(P1,P2,P3,P4,P5,P6,P7)；
    list[3]取值范围：     -460.0 ～ -290.0；
    list[4]取值范围：     -180.0 ～ 180.0；
    list[5]取值范围：     0 ～ 9 (其中 0 为最快速度，9 为最慢速度)；
    list[6]取值范围：     0 or 1 (0 为释放，1 为吸气状态)；
    '''
    write_data = "01100064002346"
    list = list1 + list2 + list3 + list4 + list5 + list6 +list7
    # print(list)
    if(len(list)!=42):
        print("Invalid input value")
        return -1
    for index in range(len(list)):
        if(((index%6==0 or index%6==1) and -200<=list[index]<=200) or (index%6==2 and -460<=list[index]<=-290) or (index%6==3 and -180<=list[index]<=180)):
            write_data = write_data + inverse_code(int(list[index]*10))
        elif((index%6==4 and 0<=list[index]<=9) or (index%6==5 and 0<=list[index]<=1)):
            write_data = write_data + '0' + str(list[index])
        else:
            print("Invalid input value")
            return -1
    print(write_data)
    write_data = crc16_modbus(write_data)
    return serial_operation(write_data)
    # else:
    #     print("Invalid input value")

def crc16_modbus(s):
    '''CRC16/MODBUS.计算CRC检验并转成字节数据'''
    crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    return get_crc_value(s, crc16)

def get_crc_value(s, crc16):
    '''CRC计算函数，返回字节数据'''
    data = s.replace(' ', '')
    crc_out = hex(crc16(unhexlify(data))).upper()
    str_list = list(crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = ''.join(str_list[2:])
    s = s + crc_data[2:] + crc_data[:2]
    # print(s)
    return bytes.fromhex(s)

def inverse_code(in_code):
    '''计算16位补码'''
    outcode = bin(in_code & 0xFFFF)
    outcode = hex(int(outcode,2))[2:]
    while(len(outcode)!=4):
        outcode = '0' + outcode
    return outcode

# coordinate_write(0,100,-320,90,6,1)

def serial_operation(write_data):
    '''串口写入并输出返回值'''
    ser = serial.Serial('/dev/ttyUSB0',9600,8,'E',1)
    flag = ser.is_open
    if(flag):
        # print("success\n")
        # ser.close()
        pass
    else:
        print("Open Error\n")
        # return -1
    ser.flushInput()  # 清空缓冲区
    ser.write(write_data)

    time.sleep(0.1) # 延时50ms
    count = ser.inWaiting() # 获取串口缓冲区数据
    if(count != 0):
        read_data = ser.read(ser.in_waiting)# 读出串口数据
        # print(read_data)
        return read_data

# P1 = [0, 100, -320, 90, 6, 1]
# P2 = [0, 100, -380, 90, 6, 1]
# P3 = [0, 100, -320, 90, 6, 1]
# P4 = [0, -100, -320, 0, 6, 1]
# P5 = [0, -100, -380, 0, 6, 1]
# P6 = [0, -100, -320, 0, 6, 0]
# P7 = [0,    0, -320, 0, 6, 0]


# coordinate_write(0,0,-300)
# coordinate_write_seven(P1,P2,P3,P4,P5,P6,P7)
# coordinate_read()
