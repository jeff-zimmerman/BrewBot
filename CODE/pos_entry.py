try:
	from pyfirmata import Arduino, util, time #imports pyfirmata if intalled. If not, installs it and imports it
except:
	import pip
	pip.main(['install', 'pyfirmata'])
	from pyfirmata import Arduino, util, time


'''end of setup'''

board = Arduino('/dev/ttyACM0') 					#tells pyfirmata what port to communicate with board over

iterator = util.Iterator(board)
iterator.start() 									#sets up loop to talk to ard. Like what's in the void loop section of regular arduino ide

record = open('record.txt', 'w+')					#opens file to record positions and times in 

V1 = board.get_pin('a:0:i')							#sets up pins for voltage from pot
V2 = board.get_pin('a:1:i')
V3 = board.get_pin('a:2:i')
servo1 = board.get_pin('d:3:s')	
servo2 = board.get_pin('d:5:s')						#pins to servo
servo3 = board.get_pin('d:6:s')	
button = board.get_pin('d:2:i')					#pins to button
time.sleep(.5)										#Shhhhhhhhh! 

start_time = time.time()							#need to declare the variable start_time to have something to reference (I don't think you actually need this)
checker = True										#This is kinda a dummy variable to have the program only record one location per button press
while (True):
	print ('Recording...\r')						#keep looping forever until double click
	Voltage1 = V1.read()								
	Voltage2 = V2.read()
	Voltage3 = V3.read()

	servo1.write(Voltage1*180)
	servo2.write(Voltage2*180)
	servo3.write(Voltage3*180)

	if (button.read() == 1 and checker):			#If button is pressed and hasn't been let up since the last loop
		if (time.time()-start_time <= 0.2):			#this is what sets the time for a double click to stop recording (0.2s)
			record.close()							#closes file and exits program
			exit(0)
		string_time = str('{}\t{}\t{}\t{}\n'.format(Voltage1*180, Voltage2*180, Voltage3*180, time.time() - start_time))		#this is how the data is entered into text file
		record.write(string_time)					#writes data to file
		checker = False								
		start_time = time.time()					#restarts timer

	if (button.read() == 0):
		checker = True								#resets dummy variable after you lef up the button so that it can record again