import tkinter as tk
from tkinter import ttk
from pubsub import pub
import math

class MyView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.mc_entry_var = tk.StringVar()
        self.tube_entry_var = tk.StringVar()
        self.qty_entry_var = tk.StringVar()
        self.slider1_value = tk.DoubleVar()
        self.slider2_value = tk.DoubleVar()
        self.mold_entry_var = tk.StringVar()

        # field options
        options = {'padx': 10, 'pady': 10}

        #create notebook
        self.notebook = ttk.Notebook(self.parent)

        #set up Frame in subframes
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text="液壓/Hydroforming 1 ")
        self.notebook.add(self.frame2, text="還摸/Mold Exchange 2 ")
        self.notebook.pack(expand=1, fill='both')
        self.top_frame = ttk.Frame(self.frame1)
        self.top_frame.grid(column=0, row=0)
        self.bottom_frame = ttk.Frame(self.frame1)
        self.bottom_frame.grid(column=0, row=1, pady=30)


        # TOP FRAME
        # entrys
        self.mc_entry = ttk.Entry(self.top_frame, width=30, textvariable=self.mc_entry_var, font=('Arial',20))
        self.mc_entry.grid(column=1, row=0, sticky=tk.W, **options)
        self.mc_entry.focus()

        self.tube_entry = ttk.Entry(self.top_frame, width=30, textvariable=self.tube_entry_var, font=('Arial',20))
        self.tube_entry.grid(column=1, row=1, sticky=tk.W, **options)

        self.qty_entry = ttk.Entry(self.top_frame, width=30, textvariable=self.qty_entry_var, font=('Arial',20))
        self.qty_entry.grid(column=1, row=2, sticky=tk.W, **options)

        # MC
        self.mc_label = ttk.Label(self.top_frame, text="機器/Machine:", font=('Arial',20))
        self.mc_label.grid(column=0, row=0, sticky=tk.W, **options)

        self.MC_Button = ttk.Button(self.top_frame, text="X", style="my.TButton")
        self.MC_Button['command'] = self.mc_clear_button_clicked
        self.MC_Button.grid(column=2, row=0, **options)

        # Tube
        ttk.Label(self.top_frame, text='規格/Tube:', font=('Arial',20)).grid(column=0, row=1, sticky=tk.W, **options)
        self.tube_Button = ttk.Button(self.top_frame, text="X", style="my.TButton")
        self.tube_Button['command'] = self.tube_clear_button_clicked
        self.tube_Button.grid(column=2, row=1, **options)

        # qty
        ttk.Label(self.top_frame, text='數量/PCs:', font=('Arial',20)).grid(column=0, row=2, sticky=tk.W, **options)
        self.qty_Button = ttk.Button(self.top_frame, text="X", style="my.TButton")
        self.qty_Button['command'] = self.qty_clear_button_clicked
        self.qty_Button.grid(column=2, row=2, **options)


        #bottom Frame
        self.slider1 = ttk.Scale(self.bottom_frame, from_=8, to=22.5, length=800,variable=self.slider1_value)
        self.slider1['command'] = self.slider1_changed
        self.slider1.pack()
        self.slider1_value.set(8)
        self.slider1_label = ttk.Label(self.bottom_frame, text=self.get_slider1_value(), font=('Arial',20))
        self.slider1_label.pack()

        self.slider2 = ttk.Scale(self.bottom_frame, from_=8, to=22.5, value=17, length=800,variable=self.slider2_value)
        self.slider2['command'] = self.slider2_changed
        self.slider2.pack()
        self.slider2_value.set(17)
        self.slider2_label = ttk.Label(self.bottom_frame, text=self.get_slider2_value(), font=('Arial',20))
        self.slider2_label.pack()

        # save button
        self.save_button = ttk.Button(self.bottom_frame, text="OK", style="my.TButton")
        self.save_button['command'] = self.save_button_clicked
        self.save_button.pack(pady=50)

        self.s = ttk.Style(self.parent)
        self.s.configure('my.TButton', font=('Arial', 20))

    def mc_clear_button_clicked(self):
        self.mc_entry.delete(0, 'end')

    def tube_clear_button_clicked(self):
        self.tube_entry.delete(0, 'end')

    def qty_clear_button_clicked(self):
        self.qty_entry.delete(0, 'end')

    def save_button_clicked(self):
        pub.sendMessage("save_button_clicked")

    def get_slider1_value(self):
        minute, hour = math.modf(self.slider1_value.get())
        minute = minute * 60
        minute = math.floor(minute/15)*15
        if minute == 0:
            result_minute = "00"
        else:
            result_minute = str(minute)
        return str(int(hour)) + ":" + result_minute

    def slider1_changed(self, event):
        self.slider1_label.configure(text=self.get_slider1_value())

    def get_slider2_value(self):
        minute, hour = math.modf(self.slider2_value.get())
        minute = minute * 60
        minute = math.floor(minute/15)*15
        if minute == 0:
            result_minute = "00"
        else:
            result_minute = str(minute)
        return str(int(hour)) + ":" + result_minute

    def slider2_changed(self, event):
        self.slider2_label.configure(text=self.get_slider2_value())