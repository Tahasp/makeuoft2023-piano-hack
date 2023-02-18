import mido


def list_select(selections: list[str], name: str):
    if len(selections) == 1:
        return selections[0]

    for i, selection in enumerate(selections):
        print(f"{i + 1}. {selection}")

    index = int(input(f"select {name}: "))
    return selections[index - 1]


def main():
    outputs: list[str] = mido.get_output_names()
    inputs: list[str] = mido.get_input_names()
    output = list_select(outputs, "midi output")
    input = list_select(outputs, "midi output")
    output_port = mido.open_output(output)
    input_port = mido.open_input(input)


if __name__ == "__main__":
    main()
