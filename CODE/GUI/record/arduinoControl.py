try:
    from pyfirmata import Arduino, util, time  # imports pyfirmata if intalled. If not, installs it and imports it
    from pathlib import Path
    from PyQt5.QtCore import *
    import threading

except:
    import pip

    pip.main(['install', 'pyfirmata'])
    from pyfirmata import Arduino, util, time
    from pathlib import Path
    from PyQt5.QtCore import *
    import threading

'''end of setup'''


class connectArduino(QObject):

    def __init__(self):
        super().__init__(parent=None)
        self.recordBtnState = False
        self.time_start = 0
        print('init')

    update_pos = pyqtSignal(list)
    connect_status = pyqtSignal(str)


    def initArduino(self):
        print('_initArduino')
        self.connect_status.emit('Connecting to Arduino')
        self.board = Arduino('/dev/ttyACM0')  # tells pyfirmata what port to communicate with board over
        self.connect_status.emit('Connected to Arduino')
        iterator = util.Iterator(self.board)
        iterator.start()
        # sets up loop to talk to ard. Like what's in the void loop section of regular arduino ide
        self.basepath = str(Path(__file__).parents[3])
        self.record = open(self.basepath + '/RECORD/record_test.txt',
                           'w+')  # opens file to record positions and times in

        self.V1 = self.board.get_pin('a:0:i')  # sets up pins for voltage from pot
        self.V2 = self.board.get_pin('a:1:i')
        self.V3 = self.board.get_pin('a:2:i')
        self.servo1 = self.board.get_pin('d:3:s')
        self.servo2 = self.board.get_pin('d:5:s')  # pins to servo
        self.servo3 = self.board.get_pin('d:6:s')
        self.button = self.board.get_pin('d:2:i')  # pins to button
        time.sleep(.5)  # Shhhhhhhhh!

        self.updatePos()

    def updatePos(self):
        while True:
            print('\rRecording', end='')
            Voltage1 = self.V1.read()
            Voltage2 = self.V2.read()
            Voltage3 = self.V3.read()
            self.servo1.write(Voltage1 * 180)
            self.servo2.write(Voltage2 * 180)
            self.servo3.write(Voltage3 * 180)
            pos = [x * 180 for x in [Voltage1, Voltage2, Voltage3]]

            if self.recordBtnState:
                pos = [x * 180 for x in [Voltage1, Voltage2, Voltage3]] + [time.time()-self.time_start]
                self.update_pos.emit(pos)
            else:
                self.update_pos.emit(pos)



        # time_now = time.time()
        # prev_time = time_now if 'time_interval' not in locals() else prev_time  # need to declare the variable start_time to have something to reference (I don't think you actually need this)										#This is kinda a dummy variable to have the program only record one location per button press
        #
        # if Parent.record_position_event.is_set():  # If button is pressed and hasn't been let up since the last loop
        #     time_interval = (time_now - prev_time)
        #     prev_time = time_now
        #     string_time = str(f'{Voltage1 * 180}\t{Voltage2 * 180}\t{Voltage3 * 180}\t{time_interval}\n')
        #     # record.write(string_time) writes data to file
        #     print('\n' + string_time)  # restarts timer
        #     Parent.record_position_button['text'] = f'Record Position {x}'
        #     x += 1
        #     Parent.record_position_event.clear()
        #
        # if Parent.stop_record_event.is_set():  # this is what sets the time for a double click to stop recording (0.2s)
        #     record.close()  # closes file and exits program
        #     Parent.stop_record_event.clear()
        #     raise CloseRecord
