#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import requests
from serial import *
from datetime import  datetime

class scanner:
    PRESENT_Value = 0xFFFF
    POLYMONIAL = 0x8408

    test_serial = Serial('COM')


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
            value='11 222 555 33 66 55 44 55 66 55 55 444')
        self.inventory1.configure(
            justify="center",
            state="readonly",
            textvariable=self.inv1,
            validate="focusin",
            width=50)
        _text_ = '11 222 555 33 66 55 44 55 66 55 55 444'
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
        _text_ = '11 222 555 33 66 55 44 55 66 55 55 444'
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
