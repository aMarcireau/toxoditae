class Node:
    def __init__(self, parser):
        if isinstance(parser, str):
            filename = parser
            parser = {'index': 0}
            with open(filename) as input:
                parser.data = input.read()
        
