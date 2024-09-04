def read_one_line(filename: str) -> str:
    with open(filename, 'r') as file:
            first_line = file.readline()
            return first_line.strip() 

def write_text(filename: str, text: str):
    try:
        with open(filename, 'w') as file:
            file.write(text)
    except:
        print("An error occured while writing the file")

def copy_characters(input_file: str, output_file: str, nb: int):
    try:
        with open(input_file, 'r') as infile:
            content = infile.read(nb)

        with open(output_file, 'a') as outfile:
            outfile.write('\n' + content)
    except:
        print("An error occured while copying the file")

def read_all_lines(filename: str) -> (list[str],list[str]):
    with open(filename, 'r') as file:
        lines = file.readlines()
    alternates_lines = lines[::2]
    return lines, alternates_lines
    

if __name__ == "__main__":
    file = "Day2/assets/random_phrases.txt"
    print(read_one_line(file))

    dossier = "Day2/Part 1/"
    file_name = "Test.txt"
    path_file = f"{dossier}/{file_name}"
    text = "Hello World"
    
    write_text(path_file, text)
    print(read_one_line(file_name))

    nb_caracteres = 100 

    copy_characters(file, path_file, nb_caracteres)
    print(f"Les {nb_caracteres} premiers caractères de {file} ont été copiés dans {path_file}.")

    lines, alternate_lines = read_all_lines(file)
    print(lines)
    print(alternate_lines)