import re

class Node:
    @staticmethod
    def error(parser, message):
        raise Exception('parse error from {} at {}:{}: {}'.format(parser['filename'], parser['line'], parser['position'], message))
    @staticmethod
    def format(string):
        if not re.match(r'^\s*$', string) is None:
            return None
        integer_match = re.match(r'^\s(\d+)\s$', string)
        if not integer_match is None:
            return int(integer_match.group(1))
        float_match = re.match(r'^\s([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s$', string)
        if not float_match is None:
            return float(float_match.group(1))
        return string.strip()
    def __init__(self, parser):
        self.variables = []
        self.nodes = []
        if isinstance(parser, str):
            filename = parser
            parser = {'index': 0, 'line': 1, 'position': 1, 'filename': filename}
            with open(filename, 'r') as input_file:
                parser['data'] = input_file.read()
        state = 'root'
        name = ''
        variable = ''
        while parser['index'] < len(parser['data']):
            character = parser['data'][parser['index']]
            parser['index'] += 1

            # state machine
            if state == 'root':
                if character == '/':
                    state = 'before_comment'
                elif character == '}':
                    break
                elif not character.isspace():
                    state = 'name'
                    name = character
            elif state == 'before_comment':
                if character == '/':
                    state = 'comment'
                else:
                    Node.error(parser, 'expected /')
            elif state == 'comment':
                if character == '\n':
                    state = 'root'
            elif state == 'name':
                if character.isspace():
                    state = 'name_done'
                else:
                    name += character
            elif state == 'name_done':
                if character == '=':
                    state = 'variable'
                    variable = ''
                elif character == '/':
                    state = 'before_name_comment'
                elif character == '{':
                    self.nodes.append((name, Node(parser)))
                    state = 'root'
                elif not character.isspace():
                    Node.error(parser, 'expected =, { or a space')
            elif state == 'before_name_comment':
                if character == '/':
                    state = 'name_comment'
                else:
                    Node.error(parser, 'expected /')
            elif state == 'name_comment':
                if character == '\n':
                    state = 'after_name_comment'
            elif state == 'after_name_comment':
                if character == '{':
                    self.nodes.append((name, Node(parser)))
                    state = 'root'
                elif not character.isspace():
                    Node.error(parser, 'expected { or a space')
            elif state == 'variable':
                if character == '\n':
                    self.variables.append((name, Node.format(variable)))
                    state = 'root'
                elif character == '/':
                    state = 'before_variable_comment'
                else:
                    variable += character
            elif state == 'before_variable_comment':
                if character == '/':
                    self.variables.append((name, Node.format(variable)))
                    state = 'comment'
                else:
                    variable += '/'
                    variable += character
                    state = 'variable'
            else:
                raise Error('unknown state {}'.format(state))

            # update parser status
            if character == '\n':
                parser['line'] += 1
                parser['position'] = 1
            else:
                parser['position'] += 1
