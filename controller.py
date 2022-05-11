import tkinter as tk
import model as m
import view as v
from pubsub import pub


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.model = m.Model()
        self.view = v.MyView(parent)

        pub.subscribe(self.save_button_clicked, "save_button_clicked")

    def save_button_clicked(self):
        try:
            # set the entry data to the model
            self.model.machine = self.view.mc_entry_var.get()
            self.model.tube = self.view.tube_entry_var.get()
            self.model.qty = self.view.qty_entry_var.get()
            self.model.start_time = self.view.get_slider1_value()
            self.model.end_time = self.view.get_slider2_value()
            self.model.calculate_hours()
            self.model.calculate_avg_tubes_hour()

            # save to database
            self.model.save()
            self.view.mc_clear_button_clicked()
            self.view.tube_clear_button_clicked()
            self.view.qty_clear_button_clicked()
            self.view.mc_entry.focus()
        except Exception as error:
            print(repr(error))
