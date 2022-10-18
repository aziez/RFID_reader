import time

import requests
from serial import *
from datetime import  datetime
from apscheduler.schedulers.background import BlockingScheduler


PRESET_Value = 0xFFFF
POLYNOMIAL = 0x8408

test_serial = Serial('COM3', 57600, timeout=0.1)
now = datetime.now()
dt_string = now.strftime("%d/%m/%y %H:%M:%S")

# scan
INVENTORY1 = '06 00 01 00 06'  # membaca TID
INVENTORY2 = '04 00 0F' #Membaca EPC
# read EPC
readTagMem = '12 00 02 02 11 22 33 44 01 00 04 00 00 00 00 00 00'
# change EPC
writeEpc = '0D 00 04 02 00 00 00 00 11 22 33 44'
# set data
setAddress = '05 00 24 03'

#SEND DATA TO API
url = 'https://reqres.in/api/users'
startTime = time.time()

def crc(cmd):
    cmd = bytes.fromhex(cmd)
    uiCrcValue = PRESET_Value
    for x in range((len(cmd))):
        uiCrcValue = uiCrcValue ^ cmd[x]
        for y in range(8):
            if (uiCrcValue & 0x0001):
                uiCrcValue = (uiCrcValue >> 1) ^ POLYNOMIAL
            else:
                uiCrcValue = uiCrcValue >> 1
    crc_H = (uiCrcValue >> 8) & 0xFF
    crc_L = uiCrcValue & 0xFF
    cmd = cmd + bytes([crc_L])
    cmd = cmd + bytes([crc_H])
    return cmd


def send_cmd(cmd):
    data = crc(cmd)
    # print(data)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]
    # print(hex_list)
    hex_space = ' '.join(hex_list)
    data = {
      "datetime": dt_string,
        "uid"   : hex_space
    }
    if(hex_space.find("FB") != -1):
        print("Kartu Tidak Terdeteksi")
    elif(hex_space.find("FE") != -1):
        print("Kartu tidak terdeteksi")
    elif(hex_space == ""):
        print("Data Kosong")
    else:
        sendApi = requests.post(url, json=data);
        print(sendApi.text)

while True:
    send_cmd(INVENTORY1)
    time.sleep(1 - ((time.time() - startTime) % 1))



