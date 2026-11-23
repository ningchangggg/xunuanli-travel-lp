import sys,glob
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+'/s*.png')); ims=[Image.open(f).convert('RGB') for f in fs]
W=ims[0].width; o=Image.new('RGB',(W,sum(i.height for i in ims)),'white'); y=0
for i in ims: o.paste(i,(0,y)); y+=i.height
o.save(sys.argv[2],quality=90); print(o.size)
