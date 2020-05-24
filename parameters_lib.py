from tkinter import messagebox

alright = True

def check_m_axle(m_axle):
	if m_axle == '' or float(m_axle) <= 0:
		return "M axle parameter is incorrect"
	return True

def check_m_disk(m_disk):
	if m_disk == '' or float(m_disk) <= 0:
		return "M disk parameter is incorrect"
	return True

def	check_r_axle(r_axle):
	if r_axle == '' or float(r_axle) <= 0:
		return "R axle parameter is incorrect"
	return True

def	check_r_disk(r_disk):
	if r_disk == '' or float(r_disk) <= 0:
		return "R disk parameter is incorrect"
	return True

def	check_cyl_length(cyl_length):
	if cyl_length == '' or float(cyl_length) <= 0:
		return "Cylynder length parameter is incorrect"
	return True

def	check_thr_length(thr_length):
	if thr_length == '' or float(thr_length) <= 0:
		return "Thread length parameter is incorrect"
	return True

def error_par(text):
	messagebox.showerror("Incorrect parameters", text)

def check_coord(coord, l):
	if coord == '' or float(coord) < 0:
		return "Initial coordinate is incorrect"
	return True

def check_vel(vel):
	if vel == '' or float(vel) < 0:
		return "Initial velocity is incorrect"
	return True

def check_dir(direct):
	if direct != 'up' and direct!= 'down':
		return "Set initial direction, man"
	return True

def error_cond(text):
	messagebox.showerror("Incorrect conditions", text)

def par_checker(m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length):
	global alright
	message = ''
	results = [check_m_axle(m_axle), check_m_disk(m_disk), check_r_axle(r_axle), 
	check_r_disk(r_disk), check_cyl_length(cyl_length), check_thr_length(thr_length)]
	for res in results:
		if type(res) == str:
			message += res + '\n'
	if message != '':
		alright = False
		error_par(message)

def cond_checker(coord, vel, direct, thr_l):
	global alright
	message = ''
	results = [check_coord(coord, thr_l), check_vel(vel), check_dir(direct)]
	for res in results:
		if type(res) == str:
			message += res + '\n'
	if message != '':
		alright = False
		error_cond(message)

def checker(m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length, coord, vel, direct):
	global alright
	print(m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length, coord, vel, direct)
	par_checker(m_disk, m_axle, r_disk, r_axle, cyl_length, thr_length)
	cond_checker(coord, vel, direct, thr_length)
	return alright

