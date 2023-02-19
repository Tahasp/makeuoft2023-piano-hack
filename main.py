import mido
from mido import MidiFile
import threading

from mido.midifiles.midifiles import time


def list_select(selections, name):
    if len(set(selections)) == 1:
        return selections[0]

    # automatic casio selection
    for selection in selections:
        if selection.find("CASIO") >= 0:
            return selection

    for i, selection in enumerate(selections):
        print(f"{i + 1}. {selection}")

    index = int(input(f"select {name}: "))
    return selections[index - 1]


class SingleNoteReader:
    def __init__(self, max=0):
        self.i = 0
        self.file = list(MidiFile('for_elise_by_beethoven.mid'))

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):  # get the next music chunk
        msgs = []
        outmsg = self.file[self.i]

        to_find = set()
        time_so_far = 0
        slowness = 2
        while True:
            if outmsg.is_meta:
                self.i += 1
            elif outmsg.type == 'program_change':
                msgs.append(outmsg)
                self.i += 1
            elif outmsg.type == 'note_on':
                if len(to_find) == 0:
                    outmsg.time = 0
                else:
                    time_so_far += outmsg.time
                    outmsg.time = time_so_far * slowness
                outmsg.channel = 1
                msgs.append(outmsg)
                to_find.add(outmsg.note)
                self.i += 1
            elif outmsg.type == 'note_off':
                time_so_far += outmsg.time
                outmsg.time = time_so_far * slowness
                outmsg.velocity = 64
                outmsg.channel = 1
                msgs.append(outmsg)
                to_find.remove(outmsg.note)
                self.i += 1
                if len(to_find) == 0:
                    break
            else:
                print("ERROR: unsupported message type!!")

            if self.i >= len(self.file):
                break
            outmsg = self.file[self.i]
        return msgs


def runmsg(out_port, msg):
    time.sleep(msg.time)
    print(msg)
    out_port.send(msg)


def main():
    outputs: list[str] = mido.get_output_names()
    inputs: list[str] = mido.get_input_names()
    output = list_select(outputs, "midi output")
    input_dev = list_select(outputs, "midi input")
    output_port = mido.open_output(output)
    input_port = mido.open_input(input_dev)

    music = SingleNoteReader()
    # for i, chunk in enumerate(notes):
    #     print(f"chunk {i}")
    #     for note in chunk:
    #         print(note)
    #     input()

    myiter = iter(music)
    for inmsg in input_port:
        print("input:", inmsg)
        # output_port.send(inmsg)
        if inmsg.type == "note_on":
            chunk = next(myiter)
            for outmsg in chunk:
                if outmsg.type == "note_on" or outmsg.type == "note_off":
                    x = threading.Thread(target=runmsg, args=(output_port, outmsg,))
                    x.start()
                else:
                    output_port.send(outmsg)
                    print(outmsg)


if __name__ == "__main__":
    main()
