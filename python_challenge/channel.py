import zipfile
import re
from sys import argv
from sys import stdout

z = zipfile.ZipFile(argv[1])

characteristic_string = "Next nothing is"

n = 90052

while True:
    file_name = str(n) + ".txt"
    text = z.getinfo(file_name).comment
    stdout.write(text)
    t = open(file_name).read()
    search = re.search(characteristic_string + '\s+(\d+)', t)
    if search:
        n = search.group(1)
    else:
        break
