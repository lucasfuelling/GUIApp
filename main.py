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
        self.model = m.Model()

    # to display the current frame passed as
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
            self.model.machine = self.frames[view.MoldPage].mc_entry_var.get()
            self.model.tube = self.frames[view.MoldPage].tube_entry_var.get()
            self.model.mold_change_time = self.frames[view.MoldPage].mold_change_time_entry_var.get()

            #save to database mold change
            self.model.save_mold_change()

            # empty entry fields
            self.frames[view.MoldPage].mc_entry.delete(0, 'end')
            self.frames[view.MoldPage].tube_entry.delete(0, 'end')
            self.frames[view.MoldPage].mold_change_time_entry.delete(0, 'end')

            # go back to mainpage
            self.show_frame(view.MainPage)

        except Exception as error:
            print(repr(error))

    def save_button_clicked(self):
        try:
            # set the entry data to the model
            self.model.machine = self.frames[view.InputPage].mc_entry_var.get()
            self.model.tube = self.frames[view.InputPage].tube_entry_var.get()
            self.model.qty = self.frames[view.InputPage].qty_entry_var.get()
            self.model.start_time = self.frames[view.InputPage].start_time_entry_var.get()
            self.model.end_time = self.frames[view.InputPage].end_time_entry_var.get()
            self.model.calculate_hours()
            self.model.calculate_avg_tubes_hour()

            # save to database
            self.model.save_input()

            # empty entry fields
            self.frames[view.InputPage].mc_entry.delete(0, 'end')
            self.frames[view.InputPage].tube_entry.delete(0, 'end')
            self.frames[view.InputPage].qty_entry.delete(0, 'end')
            self.frames[view.InputPage].start_time_entry.delete(0, 'end')
            self.frames[view.InputPage].end_time_entry.delete(0, 'end')

            # go back to mainpage
            self.show_frame(view.MainPage)

        except Exception as error:
            print(repr(error))


if __name__ == "__main__":
    # Driver Code
    app = MainController()
    app.title('JiouJiou Hydroforming')
    app.mainloop()

