def make_document(s):
    a = ''
    a += '\\documentclass{article}\n'
    a += '\\usepackage{graphicx}\n'
    a += '\\graphicspath{ {./images/} }'
    a += '\\begin{document}\n'
    a += s
    a += '\\end{document}'
    return a

def generate_table(arr):
    s = ''
    t = len(arr[0])
    s += '\\begin{tabular}{ '
    s += '| '
    for i in range(t):
        s += 'c | '
    s += '}\n'
    for i in range(len(arr)):
        s += '\t'
        for j in range(len(arr[i])):
            s += str(arr[i][j])
            if j != len(arr[i]) - 1:
                s += ' & '
        if i != len(arr) - 1:
            s += ' \\\\\n'
        else:
            s += '\n'
    s += '\\end{tabular}\n'
    return s

def generate_image(image):
    s = ''
    s += f'\\includegraphics[scale=0.15]{{{image}}}\n'
    return s