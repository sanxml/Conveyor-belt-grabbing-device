'''添加CRC检验示例程序'''
from binascii import unhexlify
from crcmod import mkCrcFun

# CRC16/MODBUS
def crc16_modbus(s):
    crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    return get_crc_value(s, crc16)

# common func
def get_crc_value(s, crc16):
    data = s.replace(' ', '')
    crc_out = hex(crc16(unhexlify(data))).upper()
    str_list = list(crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = ''.join(str_list[2:])
    return s + crc_data[2:] + crc_data[:2]

in_str = "0110000800050A0000FC18F06000000000"

out_str = crc16_modbus(in_str)

print(out_str)

hex_data = bytes.fromhex(out_str)

print(hex_data)

