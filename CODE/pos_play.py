try:
	from pyfirmata import Arduino, util, time #imports pyfirmata if intalled. If not, installs it and imports it
	import numpy as np
	import matplotlib.pyplot as plt
except:
	import pip
	pip.main(['install', 'pyfirmata'])
	from pyfirmata import Arduino, util, time
	import numpy as np
		

board = Arduino('/dev/ttyACM0') #tells pyfirmata what port to communicate with board over

iterator = util.Iterator(board)
iterator.start() 				#sets up loop to talk to ard. Like what's in the void loop section of regular arduino ide

servo1 = board.get_pin('d:3:s')	#assigns output pin
servo2 = board.get_pin('d:5:s')
servo3 = board.get_pin('d:6:s')
time.sleep(.5)					#shhhhhh it's sleeping

start_time = time.time()		#creates reference time

#function for creating list of harmonic motion. This models the start and end points of the servo as trough and peak of a sin wave
def harmonic(amp, time, steps):
	
	x = np.array([])
	for t in np.linspace(0, time, num = steps):
		x = np.append(x, 0.5*amp*np.cos((np.pi/(time))*t-np.pi)+0.5*amp)
	return(x)

def make_list(file, steps, accel=False):

	servo1_list, servo2_list, servo3_list, timing = [], [], [], [] #makes lists of positions and corresponding times they occured
	#reads lines from tab dilineated file into lists of all the positions and the time between them
	for line in open(file, 'r'):
		temp = line.strip().split('\t')
		servo1_list.append(float(temp[0]))
		servo2_list.append(float(temp[1]))
		servo3_list.append(float(temp[2]))
		timing.append(float(temp[-1]))

	#setup dicts and lists
	stepdict = {}
	steplist1, steplist2, steplist3, steptime = np.array([servo1_list[0]]), np.array([servo2_list[0]]), np.array([servo3_list[0]]), np.array([timing[0]/steps])
	#when accel = True
	if accel:
		for i in range(1, len(timing)):
			#makes list of all the positions to send to servo and times between them for each position listed
			amp1, amp2, amp3 = (servo1_list[i]-servo1_list[i-1]), (servo2_list[i]-servo2_list[i-1]), (servo3_list[i]-servo3_list[i-1])
			steplist1 = np.append(steplist1, (harmonic(amp1, timing[i], steps) + servo1_list[i-1]))
			steplist2 = np.append(steplist2, (harmonic(amp2, timing[i], steps) + servo2_list[i-1]))
			steplist3 = np.append(steplist3, (harmonic(amp3, timing[i], steps) + servo3_list[i-1]))
			steptime = np.append(steptime, [(timing[i-1]/steps) for x in range(steps)])
	#if accel=False, it does the same thing with a linear step size between each servo position.
	else:
		for i in range(1, len(timing)):
			stepsize1, stepsize2, stepsize3 = (servo1_list[i]-servo1_list[i-1])/steps, (servo2_list[i]-servo2_list[i-1])/steps, (servo3_list[i]-servo3_list[i-1])/steps
			w, x, y = servo1_list[i-1], servo2_list[i-1], servo3_list[i-1]
			try:
				for z in np.arange(servo1_list[i-1], servo1_list[i], stepsize1):
					w += stepsize1
					steplist1 = np.append(steplist1, w)
			except:
				steplist1 = np.append(steplist1, [servo1_list[i-1] for sames in range(steps)])
			try:	
				for z in np.arange(servo2_list[i-1], servo2_list[i], stepsize2):
					x += stepsize2
					steplist2 = np.append(steplist2, x)
			except:
				steplist2 = np.append(steplist2, [servo2_list[i-1] for sames in range(steps)])
			try:
				for z in np.arange(servo3_list[i-1], servo3_list[i], stepsize3):
					y += stepsize3
					steplist3 = np.append(steplist3, y)
			except:
				steplist3 = np.append(steplist3, [servo3_list[i-1] for sames in range(steps)])

			steptime = np.append(steptime, [(timing[i-1]/steps) for x in range(steps)])


	stepdict['steplist1'] = steplist1
	stepdict['steplist2'] = steplist2
	stepdict['steplist3'] = steplist3
	stepdict['steptime'] = steptime

	return (stepdict)

def move_all(stpdict):

	for i in range(len(stpdict['steptime'])):
		for key in stpdict.keys():
			if key == 'steplist1':
				servo1.write(int(stpdict[key][i]))
			elif key == 'steplist2':
				servo2.write(int(stpdict[key][i]))
			elif key == 'steplist3':
				servo3.write(int(stpdict[key][i]))

		time.sleep(stpdict['steptime'][i])


if __name__ == "__main__":

	steppo = make_list('record.txt', 50, accel = True)
	steppo2 = make_list('record.txt', 50, accel = False)
	time.sleep(5)
	move_all(steppo)

	return(0)