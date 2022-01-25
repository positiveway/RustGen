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
            pairs.append([con_from,con_to])


        output_file.write('const (\n')

        ident = ' ' * 4
        for ind, pair in enumerate(pairs):
            _, con_to = pair
            con_to_type = type_name+con_to
            con_to_low = con_to[0].lower() + con_to[1:]
            if ind == 0:
                line = f'{con_to_type} string = "{con_to_type}"'
            else:
                line = f'{con_to_type} = "{con_to_type}"'
            output_file.write(ident+line+'\n')
        output_file.write(')\n')


        output_file.write('\n')

        output_file.write(f'var {type_name}Map = map[string]string' + '{\n')
        for pair in pairs:
            con_from, con_to = pair
            con_to_type = type_name+con_to
            output_file.write(ident+f'"{con_from}": {con_to_type},\n')

        output_file.write('}\n')



if __name__ == '__main__':
    file = 'input.txt'
    gen_go_map(file)
