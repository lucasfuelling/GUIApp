import tkinter as tk
import controller as c

if __name__ == "__main__":
    root = tk.Tk()
    root.title("JiouJiou Hydroforming")
    root.geometry('800x480')
    app = c.Controller(root)
    root.mainloop()
