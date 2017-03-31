import sys


def get_fsstat_output(f):
    """
    Returns assignment-defined output (for unit tests) from `fsstat` output.


    :param f: open file-like object containing `fsstat` output
    :return: list of strings representing unit-testable output
    """
    result = []
    line = f.readline()
    while line:
        if line.startswith('Volume Label (Root Directory)'):
            pass
        elif line.startswith('METADATA INFORMATION'):
            line = f.readline()
            if not line.startswith('-'):
                sys.exit('invalid input')
            line = f.readline()
            if not line.startswith('Range:'):
                sys.exit('invalid input')
            line = f.readline()
            if not line.startswith('Root Directory:'):
                sys.exit('invalid input')
            line = f.readline().strip()
            if line != '':
                sys.exit('invalid input')
        else:
            result.append(line)
        line = f.readline()
    return result


def strip_all(lines):
    """Returns a copy of the list of lines where all lines have been strip()ped."""
    return [line.strip() for line in lines]


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        for line in get_fsstat_output(f):
            print(line, end='')
