import mido
from mido import MidiFile


def list_select(selections: list[str], name: str):
    if len(set(selections)) == 1:
        return selections[0]

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
        while True:
            if outmsg.is_meta:
                self.i += 1
            elif outmsg.type == 'program_change':
                msgs.append(outmsg)
                self.i += 1
            elif outmsg.type == 'note_on':
                # outmsg.time = 0
                msgs.append(outmsg)
                to_find.add(outmsg.note)
                self.i += 1
            elif outmsg.type == 'note_off':
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
        chunk = next(myiter)
        for outmsg in chunk:
            output_port.send(outmsg)


if __name__ == "__main__":
    main()
