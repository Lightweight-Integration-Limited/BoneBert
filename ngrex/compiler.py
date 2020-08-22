from . import parser
from . import pattern

def compile_pattern(line):
    p = parser.yacc.parse(line)
    pattern.validate_names(p)
    return p

def load_patterns(filepath):
    f = open(filepath)
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line and not line.startswith("#")]
    patterns = [compile_pattern(line) for line in lines]
    return patterns


