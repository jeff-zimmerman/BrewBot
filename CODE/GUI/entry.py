from tkinter import *
from threading import *
import time

from record.pos_entry import entry
from record.record_exceptions import CloseRecord


class entryFrame(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.stop_event = Event()
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.start_record_button = Button(self, text='Start Recording', bg='green', command=self.record)
        self.start_record_button.pack()

        self.record_position_event = Event()
        self.record_position_button = Button(self, text='Record Position', command=self.record_position_event.set)
        self.record_position_button.pack()

        self.stop_record_event = Event()
        self.stop_record_button = Button(self, text='Stop Recording', command=self.stop_record_event.set)
        self.stop_record_button.pack()

    def record(self):

        self.record_position_button['text'] = 'Record Start'
        self.start_record_button['bg'] = 'red'
        def thread(Parent=self):
            try:
                entry(Parent)
            except CloseRecord:
                self.record_position_button['text'] = 'Record Start'
                self.start_record_button['bg'] = 'green'
                print('goodbye')

        t_record = Thread(target=thread)
        t_record.start()

    def say_hi(self):
        def thread():
            for x in range(10):
                if self.stop_event.is_set():
                    self.stop_event.clear()
                    break
                print(f'\r{time.time()} Hi there, everyone!', end='')
                time.sleep(1)
            print(f'\nGoodbye!')

        t_say_hi = Thread(target=thread)
        t_say_hi.start()

    def stop_thread(self):
        self.stop_event.set()



if __name__ == '__main__':
    root = Tk()
    app = entryFrame(root)
    app.mainloop()



