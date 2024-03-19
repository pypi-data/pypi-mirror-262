from generator import generate_table, make_document
with open('/Users/nikitakocherin/workspace/python_course/hw_2/table.tex', 'w') as f:
    s = generate_table([[1, 2, 3, 4], [1, 2, 3, 4]])
    s = make_document(s)
    f.write(s)