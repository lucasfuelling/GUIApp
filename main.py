import time
import tkinter as tk
import view
import model as m


class MainController(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (view.InputPage, view.MoldPage, view.MainPage):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(view.MainPage)

        # instantiate Model
        self.model = m.Model()
        self.update_view_mainpage()


    # display the frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        #set focus on entry first field
        if cont == view.InputPage:
            self.frames[view.InputPage].mc_entry.focus()
        if cont == view.MoldPage:
            self.frames[view.MoldPage].mc_entry.focus()

    def save_button_mold_clicked(self):
        try:
            # set the entry data to the model
            machine = self.frames[view.MoldPage].mc_entry_var.get()
            tube = self.frames[view.MoldPage].tube_entry_var.get()
            mold_change_time = self.frames[view.MoldPage].mold_change_time_entry_var.get()
            order_qty = self.frames[view.MoldPage].order_qty_entry_var.get()

            #save to database mold change
            self.model.save_mold_change(machine, tube, mold_change_time, order_qty)

            # empty entry fields
            self.frames[view.MoldPage].mc_entry.delete(0, 'end')
            self.frames[view.MoldPage].tube_entry.delete(0, 'end')
            self.frames[view.MoldPage].mold_change_time_entry.delete(0, 'end')
            self.frames[view.MoldPage].order_qty_entry.delete(0, 'end')

            # go back to mainpage and update the page
            self.show_frame(view.MainPage)
            self.update_view_mainpage()

        except Exception as error:
            print(repr(error))

    def save_button_clicked(self):
        # set the entry data to the model
        self.model.machine = self.frames[view.InputPage].mc_entry_var.get()
        self.model.tube = self.frames[view.InputPage].tube_entry_var.get()
        self.model.qty_sum = self.frames[view.InputPage].qty_sum_entry_var.get()
        self.model.start_time = self.frames[view.InputPage].start_time_entry_var.get()
        self.model.end_time = self.frames[view.InputPage].end_time_entry_var.get()
        self.model.calc_qty()
        self.model.calculate_hours()
        self.model.calculate_avg_tubes_hour()

        # save to database
        self.model.save_input()

        # empty entry fields
        self.frames[view.InputPage].mc_entry.delete(0, 'end')
        self.frames[view.InputPage].tube_entry.delete(0, 'end')
        self.frames[view.InputPage].qty_sum_entry.delete(0, 'end')
        self.frames[view.InputPage].start_time_entry.delete(0, 'end')
        self.frames[view.InputPage].end_time_entry.delete(0, 'end')

        # go back to mainpage and update mainpage
        self.show_frame(view.MainPage)
        self.update_view_mainpage()

    def update_view_mainpage(self):
        # update FRAME for machine 1
        self.model.set_last_data_entry('1')
        self.frames[view.MainPage].label1_tube.config(text = self.model.tube)
        self.frames[view.MainPage].label1_qty_sum.config(text=str(self.model.qty_sum) + ' / ' + str(self.model.order_qty))
        self.frames[view.MainPage].label1_avg.config(text=str(self.model.avg_tubes_hour) + ' pcs/h')

        # update FRAME for machine 2
        self.model.set_last_data_entry('2')
        self.frames[view.MainPage].label2_tube.config(text = self.model.tube)
        self.frames[view.MainPage].label2_qty_sum.config(text=str(self.model.qty_sum) +' / ' + str(self.model.order_qty))
        self.frames[view.MainPage].label2_avg.config(text=str(self.model.avg_tubes_hour) + ' pcs/h')

    def get_order_qty(self):
        self.model.set_last_data_entry(self.frames[view.InputPage].mc_entry_var.get())
        return self.model.order_qty

if __name__ == "__main__":
    # Driver Code
    app = MainController()
    app.title('JiouJiou Hydroforming')
    # maximize window
    app.state('zoomed')
    app.mainloop()

