import re
import sys


def highlight_pattern(pattern, line):
    highlighted_line = re.sub(pattern, f"\033[1;96;40m{pattern}\033[0m", line)
    return highlighted_line

def help():
    print("Usage: grep.py PATTERN [FILE...]")
    print("Print lines matching a pattern.")
    print("If no FILE is specified, read from standard input.")

def version():
    print("grep.py v1.0 -by : TBA5854")

def usage():
    print("Usage: grep.py PATTERN [FILE...]")
    print("Try 'grep.py --help' for more information.")

def no_args(pattern):
        for line in sys.stdin:
            if re.search(pattern, line):
                highlighted_line = highlight_pattern(pattern, line)
                print(highlighted_line, end="")

def invert_match(pattern, files):
    for file in files:
        with open(file) as f:
            for line in f:
                if not re.search(pattern, line):
                    highlighted_line = highlight_pattern(pattern, line)
                    print(highlighted_line, end="")
def count(pattern, files):
    for file in files:
        count = 0
        with open(file) as f:
            for line in f:
                if re.search(pattern, line):
                    count += 1
        print(f"{file}: {count}")

def file_with_matches(pattern, files):
    for file in files:
        with open(file) as f:
            for line in f:
                if re.search(pattern, line):
                    print(file)
                    break

def file_without_matches(pattern, files):
    c=0
    for file in files:
        with open(file) as f:
            for line in f:
                if re.search(pattern, line):
                    c=1
                    break
        if c==0:
            print(file)
        c=0

def word_match(pattern, files):
    for file in files:
        with open(file) as f:
            for line in f:
                if re.search(r"\b" + pattern + r"\b", line):
                    highlighted_line = highlight_pattern(pattern, line)
                    print(highlighted_line, end="")
def case_insensitive(pattern, files):
    for file in files:
        with open(file) as f:
            for line in f:
                if re.search(pattern, line, re.IGNORECASE):
                    highlighted_line = highlight_pattern(pattern, line)
                    print(highlighted_line, end="")
    
def context(pattern, files,n):
    for file in files:
        with open(file) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if re.search(pattern, lines[i]):
                    for i in [range(len(lines))][::-1]:
                        for i in range(n):
                            lower_bound = max(n - i, range(len(lines))[0])
                            upper_bound = min(n + i, range(len(lines))[-1])
                        for i in range(lower_bound, upper_bound + 1):
                            highlighted_line = highlight_pattern(pattern, lines[i])
                            print(highlighted_line, end="")

grep_options = {
    "": no_args,
    "-v": invert_match,
    "-c": count,
    "-l": file_with_matches,
    "-L": file_without_matches,
    "-w": word_match,
    "-i": case_insensitive,
    "-n": context,
}


def main():
    if len(sys.argv) <= 1:
        usage()
        sys.exit(1)
    options = {}
    files = []
    is_n=0
    for arg in sys.argv[1:]:
        if is_n:
            if arg.isnumeric():
                count_c=arg
                is_n=0
                print("Active")
                continue
            else:
                usage()
                sys.exit(1)
        if arg in grep_options:
            if arg =="-n":
                is_n=1
            options[arg] = grep_options[arg]
        else:
            files.append(arg)
    if len(options) > 1:
        print("Error: Invalid combination of options.")
        sys.exit(1)
    pattern = files.pop(0)
    if pattern:
        if options:
            if "-n"==sys.argv[1]:context(pattern=pattern,files=files,n=int(count_c))
            else:options[list(options.keys())[0]](pattern, files)
        else:
            no_args(pattern)
    else:
        help()

if __name__ == "__main__":
    main()
