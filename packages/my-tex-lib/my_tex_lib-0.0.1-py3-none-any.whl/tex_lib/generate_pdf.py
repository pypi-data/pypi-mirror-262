import subprocess

tex_file = "table_image"

try:
    subprocess.check_call(["pdflatex", f"{tex_file}.tex"])
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

subprocess.call(['rm', f'{tex_file}.log'])
subprocess.call(['rm', f'{tex_file}.aux'])