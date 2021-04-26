
import re
import sys

from CodeLog import CodeTrace

# Can set default verbose when instance is created
ct = CodeTrace(quiet=True)


class Proccess:
    regex = ""
    default_scape = ['\\', '[', '(', ')', '+', '$', '^', '*', '?', '.']

    def __init__(self):
        ct.log('Processor instance created')

    @ct.code_tracer(quiet=True)
    def create_pattern(self, str):
        matches = re.findall(r'(.*?)(\%{[0-9SG]{0,5}\})', str, re.M)
        pattern = ''
        if matches:
            for m in matches:
                literal = self.scape_metas(m[0])
                subpattern = self.sub_format(m[1])
                if not subpattern:
                    ct.log('Cannot create pattern')
                else:
                    pattern += literal + subpattern
        pattern += ''
        self.regex = pattern
        return pattern

    @ct.code_tracer()
    def scape_metas(self, str):
        res = ''
        for char in str:
            res += char if char not in self.default_scape else '\\'+char
        return res

    @ct.code_tracer()
    def sub_format(self, sequence):
        normal_pattern = '([a-zA-Z0-9\s]*?)'
        space_pattern = '([a-zA-Z]+(\s[a-zA-Z]*){0,%s})'
        greedy_pattern = '([a-zA-Z0-9\s]*?)'
        if 'S' in sequence:
            spaces = sequence.split('S')[1][:-1]
            return space_pattern % (spaces)
        elif 'G' in sequence:
            return greedy_pattern
        else:
            return normal_pattern


    @ct.code_tracer(quiet=True)
    def run(self, line):
        ct.log('Processing line', line, self.regex)
        m = re.search(self.regex, line)
        if m:
            ct.log('Found:', m.group(0))
            return m.group(0)
        else:
            return None


if __name__ == '__main__':
    proc = Proccess()

    proc.create_pattern(' '.join(sys.argv[1:]))
    for line in sys.stdin:
        print(proc.run(line))
