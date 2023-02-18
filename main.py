import mido
from mido import MidiFile


def list_select(selections: list[str], name: str):
    if len(set(selections)) == 1:
        return selections[0]

    for i, selection in enumerate(selections):
        print(f"{i + 1}. {selection}")

    index = int(input(f"select {name}: "))
    return selections[index - 1]


def main():
    outputs: list[str] = mido.get_output_names()
    inputs: list[str] = mido.get_input_names()
    output = list_select(outputs, "midi output")
    input_dev = list_select(outputs, "midi input")
    output_port = mido.open_output(output)
    input_port = mido.open_input(input_dev)

    # for msg in MidiFile('for_elise_by_beethoven.mid').play():
    #     print(msg)
    #     input()

    myiter = iter(MidiFile('for_elise_by_beethoven.mid').play())
    for msg in input_port:
        print("input:", msg)
        outmsg = next(myiter)
        
        outmsg.time = 0
        output_port.send(outmsg)
        print("output:", outmsg)


if __name__ == "__main__":
    main()
