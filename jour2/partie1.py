# Exercice 1:

def read_one_line(filename: str) -> str:
    with open(filename, 'r') as file:
            first_line = file.readline()
            return first_line.strip() 
    
# Exercice 2:

def write_text(filename: str, text: str):
    try:
        with open(filename, 'w') as file:
            file.write(text)
    except:
        print("An error occured while writing the file")

# Exercice 3:

def copy_characters(input_file: str, output_file: str, nb: int):
    try:
        with open(input_file, 'r') as infile:
            content = infile.read(nb)

        with open(output_file, 'a') as outfile:
            outfile.write('\n' + content)
    except:
        print("An error occured while copying the file")

# Exercice 4:

def read_all_lines(filename: str) -> (list[str],list[str]):
    with open(filename, 'r') as file:
        lines = file.readlines()
    alternates_lines = lines[::2]
    return lines, alternates_lines