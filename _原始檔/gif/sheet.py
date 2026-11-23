import subprocess,sys,os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageFont
src=sys.argv[1]; tag=sys.argv[2]; N=int(sys.argv[3]); t0=float(sys.argv[4]) if len(sys.argv)>4 else 0; t1=float(sys.argv[5]) if len(sys.argv)>5 else None
d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]).decode())
t1=t1 or d
ts=[t0+(t1-t0)*(i+0.5)/N for i in range(N)]
os.makedirs('gif/fr',exist_ok=True)
def g(a):
    i,t=a; o=f'gif/fr/{tag}_{i}.jpg'
    subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{t:.2f}','-i',src,'-frames:v','1','-vf','scale=-2:360','-q:v','4',o]); return o
with ThreadPoolExecutor(8) as ex: list(ex.map(g,enumerate(ts)))
ims=[Image.open(f'gif/fr/{tag}_{i}.jpg') for i in range(N)]
w,h=ims[0].size; cols=min(N,10); rows=(N+cols-1)//cols
sh=Image.new('RGB',(cols*w,rows*h)); dr=ImageDraw.Draw(sh); fnt=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',18)
for i,im in enumerate(ims):
    sh.paste(im,((i%cols)*w,(i//cols)*h)); dr.text(((i%cols)*w+3,(i//cols)*h+3),f'{ts[i]:.1f}',fill='yellow',font=fnt)
sh.save(f'gif/sheet_{tag}.jpg',quality=82); print(tag,d,(w,h))
