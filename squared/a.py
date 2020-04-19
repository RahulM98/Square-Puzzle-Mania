import os
from PIL import Image

level = 'easy'
os.mkdir('easy')
for img_no in range(1,23):
    img = Image.open('')
w,h = img.size
c = 1
for i in range(0,h,300):
    for j in range(0,w,300):
        a = img.crop((j, i, j+300, i+300))
        path = 'new/{}.png'.format(c)
        a.save(path)
        c+=1

