import tkinter as tk
import user_interface

HEIGHT = 1200
WIDTH = 1600

root = tk.Tk()
root.wm_title("Maxwell pendulum modeling")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

user_interface.turn_interface(root)

root.mainloop()