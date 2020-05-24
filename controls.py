import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import solver_lib
import parameters_lib
import solver_lib
import matplotlib
import csv
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt 
import threading

NavigationToolbar2Tk.toolitems = (
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
      )


data = pd.DataFrame(columns=['time', 'coordinate', 'velocity', 'direction'])

class Time_dep(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        f = Figure(dpi=100)
        a = f.add_subplot(111)
        data = pd.read_csv('data.csv')
        a.plot(data["time"], data["coordinate"], label='Coordinate', color='red')
        a.plot(data["time"], data["velocity"], label="Velocity", color='blue')
        a.set_title('Time-dependence of coordinate and speed', fontdict={'fontname': 'Arial', 'fontsize': 18})
        a.set_xlabel('Time, s', fontdict={'fontname': 'Arial', 'fontsize': 16})
        a.set_ylabel('Coordinate, cm   /  velocity, cm/s', fontdict={'fontname': 'Arial', 'fontsize': 16})
        a.grid(linestyle='--', which='major')
        a.legend(fontsize=22)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class Portrait(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        f = Figure(dpi=100)
        a = f.add_subplot(111)
        data = pd.read_csv('data.csv')
        a.plot(data["coordinate"],data["velocity"], label='Portrait', color='Green')
        a.set_title('Phase portrait', fontdict={'fontname': 'Arial', 'fontsize': 18})
        a.set_xlabel('Coordinate, cm', fontdict={'fontname': 'Arial', 'fontsize': 16})
        a.set_ylabel('Velocity, cm/s', fontdict={'fontname': 'Arial', 'fontsize': 16})
        a.grid(linestyle='--', which='major')
        a.legend(fontsize=22)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

       

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def show_time_dep(parent):
	graph_time = Time_dep(parent)
	graph_time.pack()
	graph_time.tkraise()

def show_portrait(parent):
	graph_time = Portrait(parent)
	graph_time.pack()
	graph_time.tkraise()

def show_table(parent):
	table = tk.Frame(parent, bg='white')
	table.place(rely=0, relx=0, relwidth=1, relheight=1)
	scrollbarx = tk.Scrollbar(table, orient='horizontal')
	scrollbary = tk.Scrollbar(table, orient='vertical')
	tree = ttk.Treeview(table, columns=("time", "coordinate", "velocity",'direction'), height=400, selectmode="extended",
	                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
	scrollbary.config(command=tree.yview)
	scrollbary.pack(side='right', fill='y')
	scrollbarx.config(command=tree.xview)
	scrollbarx.pack(side='bottom', fill='x')
	tree.heading('time', text="time", anchor='w')
	tree.heading('coordinate', text="coordinate", anchor='w')
	tree.heading('velocity', text="velocity", anchor='w')
	tree.heading('direction', text="direction", anchor='w')
	tree.column('#0', stretch='no', minwidth=0, width=0)
	tree.column('#1', stretch='no', minwidth=0, width=160)
	tree.column('#2', stretch='no', minwidth=0, width=160)
	tree.column('#3', stretch='no', minwidth=0, width=160)
	tree.column('#3', stretch='no', minwidth=0, width=160)
	tree.pack()
	with open('data.csv') as f:
	  reader = csv.DictReader(f, delimiter=',')
	  for row in reader:
	    t = row['time']
	    z = row['coordinate']
	    v = row['velocity']
	    d = row['direction']
	    tree.insert("", 0, values=(t, z, v, d))



def animate(i):
    global data
    xList = data.iloc[:, 0]
    yList = data.iloc[:, 1]
    vList = data.iloc[:, 2]
    a.clear()
    a.plot(xList, yList)
    a.plot(xList, vList)

"""GRAPH THREAD """

ani = animation.FuncAnimation(f, animate, interval=500)

t_anim = threading.Thread(target=animation.FuncAnimation, args=[f, animate, 500])
t_anim.start()
t_anim.join()

"""END OF GRAPH THREAD """

num_start = 1
J = 0
c = []


def start(start_button, stop_button, start_param, entries):
	global data
	global num_start
	global J
	global c
	m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length, coord, vel, direct = start_param
	if num_start == 1:
		check_result = parameters_lib.checker(m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length, coord, vel, direct)
		if check_result:
			m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length, coord, vel = float(m_disk), float(m_axle), float(r_disk), float(r_axle), float(cyl_length), float(thr_length), float(coord), float(vel)
			s = 1 if direct == 'down' else -1
			num_start += 1
			for entry in entries:
				entry['state'] = 'disabled'
			data = data.append(pd.DataFrame({'time': 0, 'coordinate': coord, 'velocity': vel, 'direction': s}, index=[0]))

			J = solver_lib.J_cal(m_axle, m_disk, r_axle, r_disk)
			c = solver_lib.c_cal(r_disk, r_axle, m_disk, m_axle, cyl_length, J)
			l = thr_length
		else:
			return 

	if start_button['state'] == 'normal' or start_button['state'] == 'active':
		### States
		start_button['state'] = 'disabled'
		stop_button['state'] = 'normal'
		###

	i = len(data) - 1

	"""SOLVER THREAD"""

	t_solver = threading.Thread(target=one_step)
	t_solver.start()

	"""END OF SOLVER THREAD"""
	while True:
		init = [data.iloc[-1, 0], data.iloc[-1, 1], data.iloc[-1, 2], data.iloc[-1, 3]]
		z, v, s = solver_lib.one_step(init[1], init[2], init[3], c, l)
		data = data.append(pd.DataFrame({'time': init[0] + 0.01, 'coordinate': z, 'velocity': v, 'direction': s}, index=[i+1]))
		data.to_csv('data.csv')
		print(data)
		i += 1

def stop(start_button, stop_button):
	if stop_button['state'] == 'normal' or stop_button['state'] == 'active':
		### States
		stop_button['state'] = 'disabled'
		start_button['state'] = 'normal'
		t_solver.acquire()
		t_anim.acquire()
		###

