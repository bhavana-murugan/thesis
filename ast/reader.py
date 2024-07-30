# types
DEF = "def"
ARGS = "args"
ASSIGN = "="
ADD = "+"
LEAF = "leaf"

# chars
TAB = "\t"
BREAK_LINE = "\n"
BRACKET_START = "("
SPACE = " "


def get_tab_space_count(line):
    # tab space count
    l = 0
    tab_count = 0
    while (l < len(line)):
        if (line[l] == TAB):
            tab_count += 1
        if (line[l] == SPACE):
            tab_count += 0.25
        l += 1
        return tab_count


def read(name, *args):
   
   # to read the main file and fetching its data
    program = open(name, "r")
    program_string = program.read()


    char = program_string.find("def "+args[0].__name__)

    program_string = ""
    isStart = True
    if char != -1:
        program.seek(char)

        function_tab_count = 0
        while (True):
            line = program.readline()
            tab_count = get_tab_space_count(line)

            if isStart:
                function_tab_count = tab_count

            is_empty = len(line.rstrip()) == 0
            if (tab_count > function_tab_count or is_empty or isStart):
                isStart = False
                l = 0
                tab_count = 0
                if not is_empty:
                    program_string += line
            else:
                break
    return program_string, *args
