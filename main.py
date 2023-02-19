import mido
from mido import MidiFile
from mido.midifiles.midifiles import time
import threading

import tkinter as tk
from tkinter import HORIZONTAL, CENTER, BROWSE
import glob
import sys

# import RPi.GPIO as GPIO


def list_select(selections, name):
    if len(set(selections)) == 1:
        print(f"Autoselected {name}:", selections[0])
        return selections[0]

    # automatic casio selection
    for selection in selections:
        if selection.find("CASIO") >= 0:
            print(f"Autoselected {name}:", selection)
            return selection

    for i, selection in enumerate(selections):
        print(f"{i + 1}. {selection}")

    index = int(input(f"select {name}: "))
    return selections[index - 1]


class SingleNoteReader:
    def __init__(self, slowness=1, filename="./for-elise.mid"):
        self.i = 0
        self.file = list(MidiFile(filename))
        self.last_skip = 0
        self.one_note = False
        self.slowness = slowness

    def __iter__(self):
        self.i = 0
        return self

    def set_slowness(self, slowness):
        self.slowness = slowness

    def reset(self):
        self.i = 0

    def set_file(self, filename):
        self.i = 0
        self.file = list(MidiFile(filename))

    def __next__(self):  # get the next music chunk
        msgs = []
        outmsg = self.file[self.i]

        one_msg = False
        skip_so_far = self.last_skip
        while True:
            if outmsg.is_meta:
                self.i += 1
            elif outmsg.type == 'note_on':
                if one_msg and (skip_so_far != 0 or outmsg.time != 0):
                    self.last_skip = skip_so_far
                    break

                outmsg.time += skip_so_far
                if not self.one_note:
                    outmsg.time = 0
                outmsg.time *= self.slowness

                skip_so_far = 0
                msgs.append(outmsg)
                one_msg = True
                self.one_note = True
                self.i += 1
            elif outmsg.type == 'note_off':
                skip_so_far += outmsg.time
                self.i += 1
            else:
                msgs.append(outmsg)
                self.i += 1

            if self.i >= len(self.file):
                break
            outmsg = self.file[self.i]
        return msgs


HACKER_TYPE = True
MUSIC = SingleNoteReader()
OUTPORT = None


def runchunk(out_port, chunk, sleept):
    if sleept > 0:
        time.sleep(sleept)
    for note in chunk:
        out_port.send(note)


def set_volume(vol):
    global OUTPORT

    if OUTPORT is not None:
        msg = mido.Message("control_change", channel=0, control=7, value=vol)
        OUTPORT.send(msg)


def main():
    global HACKER_TYPE, MUSIC, OUTPORT

    outputs: list[str] = mido.get_output_names()
    inputs: list[str] = mido.get_input_names()
    output = list_select(outputs, "midi output")
    input_dev = list_select(outputs, "midi input")
    output_port = mido.open_output(output)
    input_port = mido.open_input(input_dev)

    OUTPORT = output_port

    music = SingleNoteReader()

    epsilon = 0.15
    next_n_epsilon = 0.05
    last_chunk_time = time.time()

    myiter = iter(MUSIC)
    nchunk = next(myiter)

    note_to_close = {}
    for inmsg in input_port:
        if not HACKER_TYPE:
            output_port.send(inmsg)
            continue

        now_time = time.time()
        if inmsg.type == "note_on":
            if now_time - last_chunk_time < epsilon:
                if now_time - last_chunk_time < next_n_epsilon:
                    print("input (CANCELLED):", inmsg)
                    continue
                print("input (POSTPONED):", inmsg)
                sleept = epsilon - now_time - last_chunk_time
            else:
                sleept = 0
            print("input:", inmsg)
            note_to_close[inmsg.note] = nchunk
            runchunk(output_port, nchunk, sleept)
            last_chunk_time = time.time()
            nchunk = next(myiter)
            for note in nchunk:
                if note.type == "note_on":
                    epsilon = note.time
                    next_n_epsilon = epsilon / 4
                    break
        elif inmsg.type == "note_off":
            chunk = note_to_close.get(inmsg.note)
            if not chunk:
                print("input (CANCELLED):", inmsg)
                continue
            print("input:", inmsg)
            for note in chunk:
                if note.type == "note_on":
                    newnote = mido.Message("note_off", channel=note.channel, note=note.note, velocity=note.velocity)
                    output_port.send(newnote)
            note_to_close.pop(inmsg.note)
            last_chunk_time = time.time()
        else:
            print("input:", inmsg)


#############
# UI
#############

def quit(win):
    win.destroy()
    win.quit()


def switch():
    global HACKER_TYPE

    HACKER_TYPE = not HACKER_TYPE


def set_slowness(slowf):
    global MUSIC
    MUSIC.set_slowness(float(slowf))


def onselect(evt):
    global MUSIC

    # Note here that Tkinter passes an event object to onselect()
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        MUSIC.set_file(value)
    except:
        pass


def run_display():
    global MUSIC

    win = tk.Tk()
    win.tk.call('tk', 'scaling', 2.0)

    width = win.winfo_screenwidth()
    height = win.winfo_screenheight()

    win.geometry("%dx%d" % (width,height))
    win.configure(bg="grey")

    # win.attributes('-fullscreen', True)
    win.title('Piano Specialist')

    label = tk.Label(win, text="Paino Specialist Menu")
    label.pack()

    button = tk.Button(text="Switch", width=10, height=20, bg="white", fg="blue", font=("Courier", 18), command=lambda: switch())
    button.place(x=0, y=0)

    button1 = tk.Button(text="Reset", width=10, height=20, bg="white", fg="blue", font=("Courier", 18), command=lambda: MUSIC.reset())
    button1.place(x=700, y=0)

    button2 = tk.Button(text="Quit", width=15, height=8, bg="cyan", fg="red", font=("Courier", 18), command=lambda: quit(win))
    button2.place(x=250, y=400)

    # s1 = tk.Scale(win, variable=v1, from_=0.5, to=2.5, orient=HORIZONTAL)
    s1 = tk.Scale(win, from_=0.5, to=2.5, digits=2, resolution=0.05,
                  orient=HORIZONTAL, sliderlength=60, length=300, width=50,
                  command=set_slowness)
    s1.set(1.0)

    l3 = tk.Label(win, text="Slowness", font=("Courier", 20))

    def s2():
        l2 = tk.Listbox(bg="white", height=5, font=("Courier", 20), selectmode=BROWSE)
        for i, song in enumerate(glob.glob("./*.mid")):
            l2.insert(i + 1, song)

        l2.place(x=250, y=250)
        l2.bind('<<ListboxSelect>>', onselect)

    b1 = tk.Button(win, text="Song List", command=s2, bg="yellow")
    b1.place(x=250, y=150)

    l1 = tk.Label(win)
    l1.pack()

    s1.pack(anchor=CENTER)
    l3.pack()

    win.mainloop()


# def detect_distance():
#     try:
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)

#         TRIG = 23
#         ECHO = 24
#         maxTime = 0.04

#         while True:
#             GPIO.setup(TRIG,GPIO.OUT)
#             GPIO.setup(ECHO,GPIO.IN)

#             GPIO.output(TRIG,False)

#             time.sleep(0.01)

#             GPIO.output(TRIG,True)

#             time.sleep(0.00001)

#             GPIO.output(TRIG,False)

#             pulse_start = time.time()
#             timeout = pulse_start + maxTime
#             while GPIO.input(ECHO) == 0 and pulse_start < timeout:
#                 pulse_start = time.time()

#             pulse_end = time.time()
#             timeout = pulse_end + maxTime
#             while GPIO.input(ECHO) == 1 and pulse_end < timeout:
#                 pulse_end = time.time()

#             pulse_duration = pulse_end - pulse_start
#             distance = pulse_duration * 17000
#             distance = round(distance, 2)

#             # print(distance)
#             if distance < 8:
#                 set_volume(127)
#             else:
#                 set_volume(80)
#     except:
#         GPIO.cleanup()


if __name__ == "__main__":
    pt = threading.Thread(target=run_display)
    pt.start()
    # pt2 = threading.Thread(target=detect_distance)
    # pt2.start()
    main()
