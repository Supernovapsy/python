import urllib
import re

characteristic_string = "and the next nothing is"

url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="

n = 90052
url_to_open = url + str(n)
text = urllib.URLopener().open(url_to_open).read()

while characteristic_string in text:
    n = re.search(characteristic_string + '(\s+\d+)', text).group(1)
    if not n:
        break
    url_to_open = url + str(n)
    text = urllib.URLopener().open(url_to_open).read()

print text