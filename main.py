import mido
from mido import MidiFile
from UI import run_display
from mido.midifiles.midifiles import time


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
    def __init__(self, slowness=1):
        self.i = 0
        # self.file = list(MidiFile("./Piano Sonata n08 op13 3mov ''Pathetique''.mid"))
        self.file = list(MidiFile("./for_elise_by_beethoven.mid"))
        self.last_skip = 0
        self.one_note = False
        self.slowness = slowness

    def __iter__(self):
        self.i = 0
        return self

    def set_slowness(self, slowness):
        self.slowness = slowness

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


def runchunk(out_port, chunk, sleept):
    if sleept > 0:
        time.sleep(sleept)
    for note in chunk:
        out_port.send(note)


def set_volume(out_port, vol):
    msg = mido.Message("control_change", channel=0, control=7, value=vol)
    out_port.send(msg)


def main():
    run_display()
    outputs: list[str] = mido.get_output_names()
    inputs: list[str] = mido.get_input_names()
    output = list_select(outputs, "midi output")
    input_dev = list_select(outputs, "midi input")
    output_port = mido.open_output(output)
    input_port = mido.open_input(input_dev)

    # vol = int(input("volume: "))
    # set_volume(output_port, vol)

    music = SingleNoteReader()

    epsilon = 0.15
    next_n_epsilon = 0.05
    last_chunk_time = time.time()

    myiter = iter(music)
    nchunk = next(myiter)

    note_to_close = {}
    for inmsg in input_port:
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


if __name__ == "__main__":
    main()
