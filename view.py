import tkinter as tk
from tkinter import ttk
import re

# standard font and padding for widgets
import main

TITLEFONT = ('Arial', 50, 'bold')
SUBTITLEFONT = ('Arial', 30, 'bold')
LARGEFONT = ("Arial", 20)
options = {'padx': 15, 'pady': 15}


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        s = ttk.Style()
        s.configure('my.Treeview', font=('Arial', 15) , rowheight=40)
        s.configure('title.TLabel', background='grey')
        s.configure('time.TLabel', font=('Arial', 20, 'bold'))

        #############
        # TOP FRAME
        #############
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill='x')
        # Main label
        self.label = ttk.Label(self.top_frame, text="久玖液壓", font=LARGEFONT)
        self.label.pack(expand=True, fill='x', side='left', **options)
        # Time label
        self.timelabel = ttk.Label(self.top_frame, text='9:00', style='time.TLabel')
        self.timelabel.pack(side='left', **options)
        # button to show pages
        self.button_mold = ttk.Button(self.top_frame, text="換摸 | Thay đổi khuôn",
                             command=lambda: controller.show_frame(MoldPage))
        self.button_mold.pack(expand=True, fill='both', side='left', **options)
        self.button_input = ttk.Button(self.top_frame, text="輸入 | Đầu vào",
                             command=lambda: controller.show_frame(InputPage))
        self.button_input.pack(expand=True, fill='both', side='left', **options)

        # separator
        self.separator_top = ttk.Separator(self, orient='horizontal')
        self.separator_top.pack(fill='x')

        #############
        # LEFT FRAME
        #############
        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(expand=True, fill='both', side='left', **options)
        # Labels for machine
        self.label2_machine = ttk.Label(self.left_frame, text="2", font=TITLEFONT)
        self.label2_machine.pack(**options)
        self.label2_qty_sum = ttk.Label(self.left_frame, text="QTY2", font=SUBTITLEFONT)
        self.label2_qty_sum.pack()

        #Treeview
        self.columns = ('date', 'tube', 'qty', 'avg_h', 'mold_time')
        self.table2 = ttk.Treeview(self.left_frame, columns=self.columns, show='headings', style='my.Treeview')
        self.table2.heading('date', text='日期')
        self.table2.heading('tube', text='規格')
        self.table2.heading('qty', text='數量')
        self.table2.heading('avg_h', text='PC/小時')
        self.table2.heading('mold_time', text='換模')
        self.table2.column('date', minwidth=0, width=120, stretch='NO')
        self.table2.column('tube', minwidth=0, width=300, stretch='NO', anchor=tk.CENTER)
        self.table2.column('qty', minwidth=0, width=70, stretch='NO')
        self.table2.column('avg_h', minwidth=0, width=70, stretch='NO')
        self.table2.column('mold_time', minwidth=0, width=70, stretch='NO')
        self.table2.pack(**options)

        # Completion time Label
        self.completion_label2 = ttk.Label(self.left_frame, text="", font=SUBTITLEFONT)
        self.completion_label2.pack(**options)

        # separator
        self.separator_middle = ttk.Separator(self, orient='vertical')
        self.separator_middle.pack(side='left', fill='y')

        #############
        # RIGHT FRAME
        #############
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(expand=True, fill='both', side='left', **options)
        # Labels for machine 1
        self.label1_machine = ttk.Label(self.right_frame, text="1", font=TITLEFONT)
        self.label1_machine.pack(**options)
        self.label1_qty_sum = ttk.Label(self.right_frame, text="QTY1", font=SUBTITLEFONT)
        self.label1_qty_sum.pack()

        #Treeview
        self.columns = ('date', 'tube', 'qty', 'avg_h', 'mold_time')
        self.table1 = ttk.Treeview(self.right_frame, columns=self.columns, show='headings', style='my.Treeview')
        self.table1.heading('date', text='日期')
        self.table1.heading('tube', text='規格')
        self.table1.heading('qty', text='數量')
        self.table1.heading('avg_h', text='PC/小時')
        self.table1.heading('mold_time', text='換模')
        self.table1.column('date', minwidth=0, width=120, stretch='NO')
        self.table1.column('tube', minwidth=0, width=300, stretch='NO', anchor=tk.CENTER)
        self.table1.column('qty', minwidth=0, width=70, stretch='NO')
        self.table1.column('avg_h', minwidth=0, width=70, stretch='NO')
        self.table1.column('mold_time', minwidth=0, width=70, stretch='NO')
        self.table1.pack(**options)

        # Completion time Label
        self.completion_label1 = ttk.Label(self.right_frame, text="", font=SUBTITLEFONT)
        self.completion_label1.pack(**options)


class InputPage(tk.Frame):

    def __init__(self, parent, controller: main.MainController):
        tk.Frame.__init__(self, parent)

        # register validation commands lambda input, typez="int": callback(input, typez=typez)
        v_cmd = (self.register(self.validate_time_start), '%P')
        iv_start_cmd = (self.register(self.on_invalid_start),)

        v_end_cmd = (self.register(self.validate_time_end), '%P')
        iv_end_cmd = (self.register(self.on_invalid_end),)

        # configure Styles
        s = ttk.Style()
        s.configure('My.TFrame', background='blue')
        s.configure('Save.TButton', font=LARGEFONT)
        s.configure('valid.TLabel', background='red')
        # define input variables
        self.mc_entry_var = tk.StringVar()
        self.tube_entry_var = tk.StringVar()
        self.qty_sum_entry_var = tk.IntVar()
        self.qty_broken_entry_var = tk.IntVar()
        self.start_time_entry_var = tk.StringVar()
        self.start_time_entry_var.set('800')
        self.end_time_entry_var = tk.StringVar()
        self.end_time_entry_var.set('1700')

        ############
        # TOP FRAME
        ############
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill='both', **options)
        # Title of the page
        self.input_title_label = ttk.Label(self.top_frame, text='輸入 | đầu vào', font=LARGEFONT)
        self.input_title_label.pack(side='left')
        # back button
        button_back = ttk.Button(self.top_frame, text="←", command=lambda: controller.show_frame(MainPage))
        button_back.pack(expand=True, fill='y', side='right', anchor='e')

        # separator
        self.separator_top = ttk.Separator(self, orient='horizontal')
        self.separator_top.pack(fill='x')

        ############
        # MIDDLE FRAME
        ############
        self.middle_frame = ttk.Frame(self)
        self.middle_frame.pack(fill='y')
        self.middle_frame.columnconfigure(0, weight=2)
        self.middle_frame.columnconfigure(1, weight=6)
        self.middle_frame.columnconfigure(2, weight=1)
        # entry fields
        self.mc_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.mc_entry_var, font=LARGEFONT)
        self.mc_entry.grid(column=1, row=0, sticky=tk.W, **options)
        self.tube_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.tube_entry_var, font=LARGEFONT)
        self.tube_entry.grid(column=1, row=1, sticky=tk.W, **options)
        self.qty_sum_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.qty_sum_entry_var, font=LARGEFONT)
        self.qty_sum_entry.bind('<KP_Enter>', 'event generate %W <Tab>')
        self.qty_sum_entry.grid(column=1, row=2, sticky=tk.W, **options)
        self.qty_broken_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.qty_broken_entry_var, font=LARGEFONT)
        self.qty_broken_entry.bind('<KP_Enter>', 'event generate %W <Tab>')
        self.qty_broken_entry.grid(column=1, row=3, sticky=tk.W, **options)
        self.start_time_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.start_time_entry_var, font=LARGEFONT)
        self.start_time_entry.bind('<KP_Enter>', 'event generate %W <Tab>')
        self.start_time_entry.config(validate='focusout', validatecommand=v_cmd, invalidcommand=iv_start_cmd)
        self.start_time_entry.grid(column=1, row=4, sticky=tk.W, **options)
        self.end_time_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.end_time_entry_var, font=LARGEFONT)
        self.end_time_entry.config(validate='focusout', validatecommand=v_end_cmd, invalidcommand=iv_end_cmd)
        self.end_time_entry.bind('<KP_Enter>', 'event generate %W <Tab>')
        self.end_time_entry.grid(column=1, row=5, sticky=tk.W, **options)
        # labels
        self.mc_label = ttk.Label(self.middle_frame, text="機器 | cỗ máy:", font=LARGEFONT)
        self.mc_label.grid(column=0, row=0, sticky=tk.W, **options)
        self.tube_label = ttk.Label(self.middle_frame, text='規格 | Sự chỉ rõ:', font=LARGEFONT)
        self.tube_label.grid(column=0, row=1, sticky=tk.W, **options)
        self.qty_sum_label = ttk.Label(self.middle_frame, text='總數 | tổng số lượng:', font=LARGEFONT)
        self.qty_sum_label.grid(column=0, row=2, sticky=tk.W, **options)
        self.qty_broken_label = ttk.Label(self.middle_frame, text='數量壞 | PCs bị hỏng:', font=LARGEFONT)
        self.qty_broken_label.grid(column=0, row=3, sticky=tk.W, **options)
        self.start_time_label = ttk.Label(self.middle_frame, text='開始 | Bắt đầu:', font=LARGEFONT)
        self.start_time_label.grid(column=0, row=4, sticky=tk.W, **options)
        self.end_time_label = ttk.Label(self.middle_frame, text='結束 | Chấm dứt:', font=LARGEFONT)
        self.end_time_label.grid(column=0, row=5, sticky=tk.W, **options)
        # validation labels
        self.mc_label_valid = ttk.Label(self.middle_frame, text="    ", font=LARGEFONT, style='')
        self.mc_label_valid.grid(column=2, row=0, sticky=tk.W, **options)
        self.tube_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='')
        self.tube_label_valid.grid(column=2, row=1, sticky=tk.W, **options)
        self.qty_sum_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='')
        self.qty_sum_label_valid.grid(column=2, row=2, sticky=tk.W, **options)
        self.qty_broken_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='')
        self.qty_broken_label_valid.grid(column=2, row=3, sticky=tk.W, **options)
        self.start_time_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='valid.TLabel')
        self.start_time_label_valid.grid(column=2, row=4, sticky=tk.W, **options)
        self.end_time_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='valid.TLabel')
        self.end_time_label_valid.grid(column=2, row=5, sticky=tk.W, **options)
        # save button
        self.save_button = ttk.Button(self.middle_frame, text="OK", style='Save.TButton', command=lambda: controller.save_button_clicked())
        self.save_button.bind('<KP_Enter>', lambda event, arg=controller: self.saved_pressed(controller))
        self.save_button.grid(column=1, row=6, sticky=tk.E, **options)
        self.save_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='')
        self.save_valid.grid(column=2, row=6, **options)

    def saved_pressed(self, contr):
        contr.save_button_clicked()

    def on_invalid_start(self):
        self.start_time_label_valid.config(style='invalid.TLabel')

    def validate_time_start(self, str_value):
        pattern = '^(2[0-3]|[01]?[0-9])([0-5][0-9])$'
        if re.fullmatch(pattern, str_value) is None:
            return False
        else:
            self.start_time_label_valid.config(style='valid.TLabel')
            return True

    def on_invalid_end(self):
        self.end_time_label_valid.config(style='invalid.TLabel')

    def validate_time_end(self, str_value):
        pattern = '^(2[0-3]|[01]?[0-9])([0-5][0-9])$'
        if re.fullmatch(pattern, str_value) is None:
            return False
        else:
            self.end_time_label_valid.config(style='valid.TLabel')
            return True


class MoldPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # configure Styles
        s = ttk.Style()
        s.configure('Save.TButton', font=LARGEFONT)
        s.configure('invalid.TLabel', font=LARGEFONT, background='red')
        s.configure('valid.TLabel', font=LARGEFONT, background='green')

        # define input variables
        self.mc_entry_var = tk.StringVar()
        self.tube_entry_var = tk.StringVar()
        self.mold_change_time_entry_var = tk.IntVar()
        self.order_qty_entry_var = tk.IntVar()

        ############
        # TOP FRAME
        ############
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill='both', **options)
        # Title of the page
        self.mold_title_label = ttk.Label(self.top_frame, text='換模 | Thay đổi khuôn', font=LARGEFONT)
        self.mold_title_label.pack(side='left')
        # back button
        self.button_back = ttk.Button(self.top_frame, text="←", command=lambda: controller.show_frame(MainPage))
        self.button_back.pack(expand=True, fill='y', side='right', anchor='e')

        # separator
        self.separator_top = ttk.Separator(self, orient='horizontal')
        self.separator_top.pack(fill='x')

        ############
        # MIDDLE FRAME
        ############
        self.middle_frame = ttk.Frame(self)
        self.middle_frame.pack(fill='y')
        self.middle_frame.columnconfigure(0, weight=2)
        self.middle_frame.columnconfigure(1, weight=6)
        self.middle_frame.columnconfigure(2, weight=1)
        # entry fields
        self.mc_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.mc_entry_var, font=LARGEFONT)
        self.mc_entry.grid(column=1, row=0, sticky=tk.W, **options)
        self.tube_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.tube_entry_var, font=LARGEFONT)
        self.tube_entry.grid(column=1, row=1, sticky=tk.W, **options)
        self.mold_change_time_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.mold_change_time_entry_var, font=LARGEFONT)
        self.mold_change_time_entry.bind('<KP_Enter>', 'event generate %W <Tab>')
        self.mold_change_time_entry.grid(column=1, row=2, sticky=tk.W, **options)
        self.order_qty_entry = ttk.Entry(self.middle_frame, width=30, textvariable=self.order_qty_entry_var, font=LARGEFONT)
        self.order_qty_entry.bind('<KP_Enter>', 'event generate %W <Tab>')
        self.order_qty_entry.grid(column=1, row=3, sticky=tk.W, **options)
        # labels
        self.mc_label = ttk.Label(self.middle_frame, text="機器 | cỗ máy:", font=LARGEFONT)
        self.mc_label.grid(column=0, row=0, sticky=tk.W, **options)
        self.tube_label = ttk.Label(self.middle_frame, text='規格 | Sự chỉ rõ:', font=LARGEFONT)
        self.tube_label.grid(column=0, row=1, sticky=tk.W, **options)
        self.mold_change_time_label = ttk.Label(self.middle_frame, text='時間 | thời gian:', font=LARGEFONT)
        self.mold_change_time_label.grid(column=0, row=2, sticky=tk.W, **options)
        self.order_qty_label = ttk.Label(self.middle_frame, text='訂單數量 | số lượng đặt hàng:', font=LARGEFONT)
        self.order_qty_label.grid(column=0, row=3, sticky=tk.W, **options)
        # validation labels
        self.mc_label_valid = ttk.Label(self.middle_frame, text="    ", font=LARGEFONT, style='')
        self.mc_label_valid.grid(column=2, row=0, sticky=tk.W, **options)
        self.tube_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='')
        self.tube_label_valid.grid(column=2, row=1, sticky=tk.W, **options)
        self.mold_change_time_label_valid = ttk.Label(self.middle_frame, text='    ', font=LARGEFONT, style='')
        self.mold_change_time_label_valid.grid(column=2, row=2, sticky=tk.W, **options)
        # save button
        self.save_button = ttk.Button(self.middle_frame, text="OK", style='Save.TButton', command=lambda: controller.save_button_mold_clicked())
        self.save_button.bind('<KP_Enter>', lambda event, arg=controller: self.saved_pressed(controller))
        self.save_button.grid(column=1, row=6, sticky=tk.E, **options)
        self.save_valid_label = ttk.Label(self.middle_frame, text='   ', font=LARGEFONT)
        self.save_valid_label.grid(column=2, row=6, **options)

    def saved_pressed(self, contr):
        contr.save_button_mold_clicked()

    def focus_next(self, event):
        event.mold_change_time_entry.tk_focusNext().focus_set()