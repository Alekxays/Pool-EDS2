def read_one_line(filename: str) -> str:
    with open(filename, 'r') as file:
        first_line = file.readline()
    return first_line


def write_text(filename: str, text: str):
    with open(filename, "w") as file:
        file.write(text)
        file.close()


def copy_characters(input_file: str, output_file: str, nb: int):
    with open(input_file, "r") as infile:
        content = infile.read(nb)
    with open(output_file, "a") as outfile:
        outfile.write("\n" + content)

def read_all_lines(filename: str) -> (list[str], list[str]):
    with open(filename, 'r') as file:
        all_lines = file.readlines()
    lines_alternate = all_lines[::2]
    return (all_lines, lines_alternate)


