from generator import generate_table, make_document, generate_image
with open('/Users/nikitakocherin/workspace/python_course/hw_2/table_image.tex', 'w') as f:
    s = generate_table([[1, 2, 3, 4], [1, 2, 3, 4]])
    i = generate_image('spb_st_isaacs_2.jpg')
    s = s + i
    s = make_document(s)
    f.write(s)