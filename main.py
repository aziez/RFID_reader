import threading
import time
from tkinter import  *
from tkinter import ttk
import requests
from serial import *
from datetime import  datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PRESET_Value = 0xFFFF
POLYNOMIAL = 0x8408

port = ['COM1', 'COM2', 'COM3', 'COM4']
reader_add = "FF"
test_serial = Serial('COM3', 57600, timeout=0.1);

now = datetime.now()
dt_string = now.strftime("%d/%m/%y %H:%M:%S")

#SCANNER UNTUK RFID
#scan
INVENTORY1 = f'06 {reader_add} 01 00 06' #Membaca TID
INVENTORY2 = f'04 {reader_add} 0F' #Membaca EPC

#Read EPC
readTagMem = f'12 {reader_add} 02 02 11 22 33 44 01 00 04 00 00 00 00 00 02'

#Change EPC
writeEpc = '0F 03 04 03 00 00 00 00 11 22 33 44 55 66'

#Set Data
setAddress = '05 03 24 00'

#TRIGGER

start = True
btnScan = ttk.Button
frame = ttk.LabelFrame
uiEntry = ttk.Entry
btnClse = ttk.Button
uuid = ""
thread = None


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
    global uuid

    data = crc(cmd)
    # print(data)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]
    # print(hex_list)
    hex_space = ' '.join(hex_list)
    uid = hex_space[-6:]
    uid_no = uid.replace(" ", "")
    uuid = uid_no
    url = 'https://fekdi.co.id/rfid'
    data = {
      # "datetime": dt_string,
        "kode"   : uuid
    }
    if(hex_space.find("FB") != -1):
        print("Kartu Tidak Terdeteksi")
    elif(hex_space.find("FE") != -1):
        print("Kartu tidak terdeteksi")
    elif(hex_space == ""):
        print("Data Kosong")
    else:
        print(f"UID Kartu : {uuid}")
        sendApi = requests.get(url, params=data, verify=False)
        print(sendApi)

# threading.Timer(0.1, send_cmd(INVENTORY1)).start()

def sendData():
    global thread
    global uiEntry

    send_cmd(INVENTORY1)
    thread = threading.Timer(1.0, sendData)
    thread.start()
def trigerScan():
    global start

    if start:
        btnScan.configure(text="STOP SCAN")
        sendData()
        start = False
    else:
        btnScan.configure(text="START SCAN")
        thread.cancel()
        start = True

def CloseWin():
    if not start:
        thread.cancel()

    main.destroy()


# # GUI CODE
main = Tk()
main.geometry("800x500")

# FRAME UNTUK SETUP READER
configFrame = ttk.LabelFrame(main)
configFrame.configure(height=150, width=300, text="Setup Scanner")
configFrame.grid(column=0, row=0)

lbPort = ttk.Label(configFrame, text="COM Port communication", anchor="w")
lbPort.grid(column=0, row=0)

cbPort = ttk.Combobox(configFrame)
cbPort.configure(values=port)
cbPort.grid(column=0, row=1)

lbReader = ttk.Label(configFrame, text="ID Reader")
lbReader.grid(column=1, row=0)

lbReader = ttk.Entry(configFrame)
lbReader.grid(column=1, row=1)
lbReader.insert("0", reader_add)
lbReader.configure(width=30)

btnReader = ttk.Button(configFrame,)
btnReader.configure(text="Open Port COM")
btnReader.grid(column=2, row=1)

lbreaderNow = ttk.Label(configFrame, text=f"COMP Port : {reader_add}")
lbreaderNow.grid(column=1, row=2)


    # DATA YANG DI BACA KARTU
frame = ttk.LabelFrame(main)
frame.configure(height=150, width=300, text="Data Kartu")
frame.grid(column=0, row=1)

# LABEL
lb1 = ttk.Label(frame, text="Date Time", foreground="blue", font=("Helvetica", 12), padding=10)
lb1.grid(column=0, row=0)
lb2 = ttk.Label(frame, text="Unique ID", foreground="blue", font=("Helvetica", 12), padding=10)
lb2.grid(column=0, row=1)

ev1 = ttk.Entry(frame)
ev1.grid(column=1, row=0)
ev1.insert("0", dt_string)
ev1.configure(state="readonly", width=50)

uidEntry = ttk.Entry(frame)
uidEntry.grid(column=1, row=1)
uidEntry.insert("0",uuid )
uidEntry.configure(state="readonly", width=50)

btnScan = ttk.Button(frame, command=trigerScan)
btnScan.configure(text="START SCAN")
btnScan.grid(column=2, row=1)


btnClse = ttk.Button(frame, command=CloseWin)
btnClse.configure(text="CLOSE APPS")
btnClse.grid(column=2, row=2)


def disable_event():
    pass


main.protocol("WM_DELETE_WINDOW", disable_event)
main.mainloop()


