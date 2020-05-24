import parameters_lib
import solver_lib
import controls
import tkinter as tk 
from tkinter import font



# User interface below

bg_color = '#3c3f4d'
second_color = '#f7ad00'

headers_font = 'Avenir Next'
general_font = 'American Typewriter'
font_comb = (general_font, 22)


class MyFrame:
	def __init__(self):
		self.frame = None
		self.label = None


	def set_frame(self,parent_container, x_shift, y_shift, Width, Height):
		self.frame = tk.Frame(parent_container, bg=bg_color, highlightthickness=3)
		self.frame.config(highlightbackground = second_color, highlightcolor= second_color)
		self.frame.place(relx=x_shift, rely=y_shift, relwidth=Width, relheight=Height)

	def set_label(self, label_text, Width, Height=1):
		self.label = tk.Label(self.frame, bg=second_color, text=label_text, font=(headers_font, 22))
		self.label.place(bordermode='inside', relx=0, rely=0, relwidth=Width, relheight=Height)



class Param_block:
	def __init__(self, parent_container, label_text, initial_value, x_shift, y_shift_label, y_shift_field, Height=0.25):
		self.label = tk.Label(parent_container, text=label_text, font=(general_font, 16), bg=bg_color, fg=second_color)
		self.label.place(relx=x_shift, rely=y_shift_label, relwidth=0.25, relheight=Height)
		self.field = tk.Entry(parent_container, font=(general_font, 14), bg='white', fg=bg_color)
		self.field.place(relx=x_shift, rely=y_shift_field, relwidth=0.25, relheight=Height)

class Control_button:
	def __init__(self, parent_container, button_text, button_command, x_shift, y_shift):
		self.button = tk.Button(parent_container, text=button_text, command=button_command, bg=second_color, fg=bg_color, font=(general_font, 20))
		self.button.place(relx=x_shift, rely=y_shift, relwidth=0.3, relheight=0.8)



def turn_interface(root):

	main_frame = tk.Frame(root, bg=bg_color, bd=0)
	main_frame.place(relx = 0, rely = 0, relwidth=1, relheight=1)

	"""HEADER"""

	subframe_name = tk.Frame(main_frame, bg=second_color, bd=0)
	subframe_name.place(relx=0, rely=0, relwidth=1, relheight=0.06)

	name_label = tk.Label(subframe_name, text='Maxwell pendulum modeling', font=(headers_font, 30), bg=second_color)
	name_label.place(relx = 0.05, rely = 0.5, anchor='w')

	author_label = tk.Label(subframe_name, text='designed by Timofey Antipov', font=(headers_font, 10), bg=second_color)
	author_label.place(relx=0.9, rely=0.95, anchor='se')

	"""END OF HEADER"""


	"""PARAMETERS FRAME"""

	parameters_frame = MyFrame()
	parameters_frame.set_frame(main_frame, 0.02, 0.075, 0.45, 0.12)
	parameters_frame.set_label("Model\nparameters", 0.25)

	# Radius area

	r_ax = Param_block(parameters_frame.frame, "Axle radius (cm):", 1, 0.25, 0, 0.25)
	r_disk = Param_block(parameters_frame.frame, "Disk radius (cm):", 1, 0.25, 0.5, 0.75)

	# Mass area

	m_ax = Param_block(parameters_frame.frame, "Axle mass (g):", 1, 0.5, 0, 0.25)
	m_disk = Param_block(parameters_frame.frame, "Disk mass (g):", 1, 0.5, 0.5, 0.75)

	# Length area

	l_cyl = Param_block(parameters_frame.frame, "Cylinder length (cm):", 1, 0.75, 0, 0.25)
	l_thread = Param_block(parameters_frame.frame, "Thread length (cm):", 1, 0.75, 0.5, 0.75)

	"""END OF PARAMETERS FRAME"""


	"""INITIAL CONDITIONS"""

	conditions_frame = MyFrame()
	conditions_frame.set_frame(main_frame, 0.02, 0.215, 0.45, 0.06)
	conditions_frame.set_label("Initial conditions", 0.25)

	z_0 = Param_block(conditions_frame.frame, "Coordinate:", 0, 0.25, 0, 0.5, 0.5)
	v_0 = Param_block(conditions_frame.frame, "Velocity:", 0, 0.5, 0, 0.5, 0.5)

	direct_label = tk.Label(conditions_frame.frame, text="Direction:", font=(general_font, 16), bg=bg_color, fg=second_color)
	direct_label.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5)

	dir_var = tk.StringVar()

	direct_radio_up = tk.Radiobutton(conditions_frame.frame, text="Up", font=(general_font, 14), variable=dir_var, value='up')
	direct_radio_up.place(relx=0.75, rely=0.5, relwidth=0.125, relheight=0.5)
	direct_radio_down = tk.Radiobutton(conditions_frame.frame, text='Down', font=(general_font, 14), variable=dir_var, value='down')
	direct_radio_down.place(relx=0.875, rely=0.5, relwidth=0.125, relheight=0.5)


	"""END OF INITIAL CONDITIONS"""

	"""CONTROL PANEL"""

	control_frame = MyFrame()
	control_frame.set_frame(main_frame, 0.02, 0.295, 0.45, 0.06)
	control_frame.set_label("Controls", 0.25)

	entries = [m_disk.field, m_ax.field, r_disk.field,
	r_ax.field, l_cyl.field, l_thread.field, z_0.field, v_0.field, direct_radio_up, direct_radio_down]

	start_command = lambda: controls.start(start_button.button, stop_button.button, [m_disk.field.get(), m_ax.field.get(), r_disk.field.get(),
	r_ax.field.get(), l_cyl.field.get(), l_thread.field.get(), z_0.field.get(), v_0.field.get(), str(dir_var.get())], entries)
	stop_command = lambda: controls.stop(start_button.button, stop_button.button)

	start_button = Control_button(control_frame.frame, "Start", start_command, 0.3, 0.1)
	stop_button = Control_button(control_frame.frame, "Stop", stop_command, 0.65, 0.1)

	"""END OF CONTROL PANEL"""


	"""GRAPH 1"""

	graph1_frame = MyFrame()
	graph1_frame.set_frame(main_frame, 0.02, 0.41, 0.45, 0.55)
	graph1_frame.set_label("Time dependence", Width=1, Height=0.1)

	pic1 = tk.Frame(graph1_frame.frame, bg='white')
	pic1.place(relx=0,rely=0.1, relwidth=1, relheight=0.9)

	controls.show_time_dep(pic1)

	"""END OF GRAPH 1"""


	"""GRAPH 2"""

	graph2_frame = MyFrame()
	graph2_frame.set_frame(main_frame, 0.53, 0.41, 0.45, 0.55)
	graph2_frame.set_label("Phase portrait", Width=1, Height=0.1)

	pic2 = tk.Frame(graph2_frame.frame, bg='white')
	pic2.place(relx=0,rely=0.1, relwidth=1, relheight=0.9)

	controls.show_portrait(pic2)

	"""END OF GRAPH 2"""
	

	"""VALUES TABLE"""

	table_frame = MyFrame()
	table_frame.set_frame(main_frame, 0.53, 0.075, 0.45, 0.28)
	table_frame.set_label("Result data", Width=1, Height=0.1)

	pic3 = tk.Frame(table_frame.frame, bg='white')
	pic3.place(relx=0,rely=0.1, relwidth=1, relheight=0.9)

	controls.show_table(pic3)

	"""END OF VALUES TABLE"""



