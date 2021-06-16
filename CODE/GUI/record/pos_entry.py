try:
	from pyfirmata import Arduino, util, time  # imports pyfirmata if intalled. If not, installs it and imports it
	from pathlib import Path
	from .record_exceptions import CloseRecord

except:
	import pip

	pip.main(['install', 'pyfirmata'])
	from pyfirmata import Arduino, util, time
	from pathlib import Path
	from .record_exceptions import CloseRecord

'''end of setup'''

board = Arduino('/dev/ttyACM0')  # tells pyfirmata what port to communicate with board over

iterator = util.Iterator(board)
iterator.start()  # sets up loop to talk to ard. Like what's in the void loop section of regular arduino ide
basepath = str(Path(__file__).parents[3])
record = open(basepath + '/RECORD/record_test.txt', 'w+')  # opens file to record positions and times in

V1 = board.get_pin('a:0:i')  # sets up pins for voltage from pot
V2 = board.get_pin('a:1:i')
V3 = board.get_pin('a:2:i')
servo1 = board.get_pin('d:3:s')
servo2 = board.get_pin('d:5:s')  # pins to servo
servo3 = board.get_pin('d:6:s')
button = board.get_pin('d:2:i')  # pins to button
time.sleep(.5)  # Shhhhhhhhh!


def entry(Parent):
	x = 1
	while True:
		print('\rRecording', end='')
		Voltage1 = V1.read()
		Voltage2 = V2.read()
		Voltage3 = V3.read()
		servo1.write(Voltage1 * 180)
		servo2.write(Voltage2 * 180)
		servo3.write(Voltage3 * 180)

		time_now = time.time()
		prev_time = time_now if 'time_interval' \
								'' not in locals() else prev_time  # need to declare the variable start_time to have something to reference (I don't think you actually need this)										#This is kinda a dummy variable to have the program only record one location per button press
		if Parent.record_position_event.is_set():  # If button is pressed and hasn't been let up since the last loop
			time_interval = (time_now - prev_time)
			prev_time = time_now
			string_time = str(f'{Voltage1 * 180}\t{Voltage2 * 180}\t{Voltage3 * 180}\t{time_interval}\n')
			# record.write(string_time) writes data to file
			print('\n' + string_time)  # restarts timer
			Parent.record_position_button['text'] = f'Record Position {x}'
			x += 1
			Parent.record_position_event.clear()

		if Parent.stop_record_event.is_set():  # this is what sets the time for a double click to stop recording (0.2s)
			record.close()  # closes file and exits program
			Parent.stop_record_event.clear()
			raise CloseRecord
