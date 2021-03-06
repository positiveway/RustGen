def gen_enum(file):
    with open(file) as input_file:
        content = input_file.readlines()

    header = content[0].strip()
    type_name = header.split(' {')[0].split(' ')[-1]

    ident = ' ' * 4

    with open('output.txt', mode='w+') as output_file:
        output_file.write(f'fn match_{type_name.lower()}({type_name.lower()}:&{type_name}) -> &str{{\n')
        output_file.write(ident + f'match {type_name.lower()} {{\n')

        for line in content[1:-1]:
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            element_name = line.split('=')[0].strip()
            output_file.write(ident * 2 + f'{type_name}::{element_name} => "{element_name}",\n')

        output_file.write(ident + '}\n')
        output_file.write('}\n')


def gen_go_map(file):
    with open(file) as input_file:
        content = input_file.readlines()

    with open('output.txt', mode='w+') as output_file:
        pairs = []
        type_name = content[0].strip().split('::')[0]
        if type_name == 'Button':
            type_name = 'Btn'

        for line in content:
            line = line.strip()
            line = line.split('::')[1]
            line = line.split('=>')
            con_to, con_from = line[0], line[1]
            con_to = con_to.strip()
            con_from = con_from.strip()[1:-2]
            pairs.append([con_from, con_to])

        output_file.write('const (\n')

        ident = ' ' * 4
        for ind, pair in enumerate(pairs):
            _, con_to = pair
            con_to_type = type_name + con_to
            con_to_low = con_to[0].lower() + con_to[1:]
            if ind == 0:
                line = f'{con_to_type} string = "{con_to_type}"'
            else:
                line = f'{con_to_type} = "{con_to_type}"'
            output_file.write(ident + line + '\n')
        output_file.write(')\n')

        output_file.write('\n')

        output_file.write(f'var {type_name}Map = map[string]string' + '{\n')
        for pair in pairs:
            con_from, con_to = pair
            con_to_type = type_name + con_to
            output_file.write(ident + f'"{con_from}": {con_to_type},\n')

        output_file.write('}\n')


def gengo():
    with open(file) as input_file:
        content = input_file.readlines()

    with open('output.txt', mode='w+') as output_file:
        for line in content:
            if not line:
                continue
            line = line.split(':')
            angle, dir = line
            dir = dir.strip()[1:-2]
            output_file.write(f'{angle}: Zone{dir},\n')


def fillSpaces(string):
    maxlen = len("DownRight") + 1
    return string + " " * (maxlen - len(string))


def reverse_layout():
    with open(file) as input_file:
        content = input_file.readlines()

    dirs = ['Right', 'UpRight', 'Up', 'UpLeft', 'Left', 'DownLeft', 'Down', 'DownRight']
    dirpairs = []
    for dir1 in dirs:
        for dir2 in dirs:
            dirpairs.append((dir1, dir2))

    layout = {}

    with open('output.txt', mode='w+') as output_file:
        for line in content:
            line = line.strip()
            if not line:
                continue
            prefix = ''
            if line.startswith(';'):
                prefix = ';'
                line = line[1:]

            letter, left, right = line.split(', ')
            letter, left, right = letter.strip(), left.strip(), right.strip()
            layout[(left, right)] = prefix + letter

        for pair in dirpairs:

            letter = layout.get(pair, "None")
            prefix = ""
            if letter.startswith(';'):
                prefix = ';'
                letter = letter[1:]

            left, right = pair
            left = prefix + left
            left, right = fillSpaces(left), fillSpaces(right)
            line = '| '.join([left, right, letter])
            output_file.write(f'{line}\n')


def replace_separators():
    with open(file) as input_file:
        content = input_file.readlines()

    with open('output.txt', mode='w+') as output_file:
        for line in content:
            line = line.replace('|', '&', 1)
            line = line.replace('|', ':', 1)
            output_file.write(f'{line}')


if __name__ == '__main__':
    file = 'input.txt'
    replace_separators()
