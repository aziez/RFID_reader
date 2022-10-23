#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import requests
from serial import *
from datetime import  datetime

from main import crc

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

class main:
    def __init__(self, master=None):
        # build ui
        self.frame = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame.configure(
            background="#00ff80",
            height=200,
            highlightbackground="#00ff80",
            width=600)
        self.frame1 = ttk.Labelframe(self.frame)
        self.frame1.configure(
            borderwidth=1,
            height=500,
            padding=10,
            relief="raised",
            text='RFID Reader',
            width=350)
        self.ttk_inv1 = ttk.Label(self.frame1)
        self.ttk_inv1.configure(
            compound="center",
            justify="center",
            padding=5,
            state="normal",
            text='INVENTORY 1')
        self.ttk_inv1.grid(column=0, row=0)
        self.inventory1 = ttk.Entry(self.frame1)
        self.inv1 = tk.StringVar(
            value= INVENTORY1)
        self.inventory1.configure(
            justify="center",
            state="readonly",
            textvariable=self.inv1,
            validate="focusin",
            width=50)
        _text_ = INVENTORY1
        self.inventory1["state"] = "normal"
        self.inventory1.delete("0", "end")
        self.inventory1.insert("0", _text_)
        self.inventory1["state"] = "readonly"
        self.inventory1.grid(column=1, row=0)
        self.ttk_inv2 = ttk.Label(self.frame1)
        self.ttk_inv2.configure(
            compound="center",
            justify="center",
            padding=5,
            state="normal",
            text='INVENTORY 2')
        self.ttk_inv2.grid(column=0, row=1, rowspan=10)
        self.inv2 = ttk.Entry(self.frame1)
        self.inv2.configure(
            justify="center",
            state="readonly",
            textvariable=self.inv1,
            width=50)
        _text_ = INVENTORY2
        self.inv2["state"] = "normal"
        self.inv2.delete("0", "end")
        self.inv2.insert("0", _text_)
        self.inv2["state"] = "readonly"
        self.inv2.grid(column=1, row=1, rowspan=10)
        self.btn_scan = ttk.Button(self.frame1)
        self.btn_scan.configure(
            compound="center",
            default="normal",
            text='SCAN MANUAL')
        self.btn_scan.grid(
            column=3,
            columnspan=10,
            ipadx=10,
            ipady=10,
            padx=10,
            pady=10,
            row=3,
            rowspan=10,
            sticky="se")
        self.frame1.pack(expand="true", side="top")
        self.frame1.grid_anchor("n")
        self.frame.pack_propagate(0)

        # Main widget
        self.mainwindow = self.frame

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = main()
    app.run()


