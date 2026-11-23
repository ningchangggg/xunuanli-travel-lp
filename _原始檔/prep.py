"""旅行機票日曆 v5 落地頁：照片裁切、內頁牆合成。輸出 img/。"""
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np, glob, os, random
Image.MAX_IMAGE_PIXELS=None
M="/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/01_廣告投放/旅行機票日曆/毛片/"
P=M+"麻豆_照片_0809/"; PG='pages/'; O='img/'
def crop_to(src, w, h, cx=0.5, cy=0.5, box=None, zoom=1.0, out=None, bright=1.0, q=88):
    im=Image.open(src).convert('RGB')
    if box: im=im.crop(box)
    W,H=im.size; r=w/h
    cw,ch=(W, W/r) if W/H < r else (H*r, H)
    cw/=zoom; ch/=zoom
    x=min(max(cx*W-cw/2,0),W-cw); y=min(max(cy*H-ch/2,0),H-ch)
    im=im.crop((round(x),round(y),round(x+cw),round(y+ch))).resize((w,h),Image.LANCZOS)
    if bright!=1.0:
        a=np.asarray(im).astype(np.float32)/255; a=a**(1/bright); im=Image.fromarray((a*255).clip(0,255).astype(np.uint8))
    im.save(O+out, quality=q); print(out, im.size)
# 首屏：IG 封面定稿同一張 247，4:5
crop_to(P+'單本旅行曆/2027煦暖曆系列_毛片-247.jpg',1080,1350,box=(960,1480,4160,5480),out='hero.jpg')
TD=M+'丁丁_Log_0912_調色對齊麻豆/_截圖/'; TB=M+'大C_B/影片檔_調色對齊麻豆/_截圖/'
# 四個情境 4:5（卡片內 400×500）
crop_to(TD+'C0135.jpg',480,600,cy=0.45,out='s1_trip.jpg')
crop_to(P+'旅行曆特寫/2027煦暖曆系列_毛片-327.jpg',480,600,cx=0.5,out='s2_history.jpg')
crop_to(M+'大C_B/照片/DSC09062.JPG',480,600,cx=0.62,out='s3_gift.jpg',bright=1.35)
crop_to('img/C3646_40.6_full.jpg',480,600,cx=0.47,cy=0.38,zoom=1.7,out='s4_xmas_v6.jpg')  # v6: 換成 C3646 40.6s 笑臉
# 全幅畫面
crop_to(TB+'C3673.jpg',1080,1350,cy=0.5,out='tear.jpg')
crop_to(TD+'C0123.jpg',1080,1350,cy=0.5,out='video.jpg')
crop_to(TD+'C0141.jpg',1080,1350,cy=0.45,out='desk.jpg')
crop_to(P+'五本旅行曆/2027煦暖曆系列_毛片-255.jpg',1080,1080,cy=0.62,out='five.jpg')
crop_to(P+'單本旅行曆/2027煦暖曆系列_毛片-216.jpg',1080,810,cy=0.55,out='spec.jpg')
crop_to(P+'二位模特兒與旅行曆/2027煦暖曆系列_毛片-417.jpg',600,600,cy=0.5,out='plan_two.jpg')
crop_to(P+'五本旅行曆/2027煦暖曆系列_毛片-260.jpg',600,600,cy=0.62,zoom=1.15,out='plan_five.jpg')
crop_to(P+'單本旅行曆/2027煦暖曆系列_毛片-228.jpg',600,600,cy=0.55,out='plan_one.jpg')
crop_to(P+'台灣模特兒與旅行曆/2027煦暖曆系列_毛片-290.jpg',600,600,cy=0.45,out='plan_mix.jpg')
# 內頁：去 3mm 出血
def trim(f, out, w=None):
    im=Image.open(f).convert('RGB'); W,H=im.size; m=round(W*8.5/555.6)
    im=im.crop((m,m,W-m,H-m))
    if w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.save(O+out,quality=90); return im
for k in (1,2): trim(PG+f'hi010_{k}.jpg', f'p0110_{k}.jpg', 1000)
# 內頁牆：深夜藍底，41 張登機牌散貼
fs=sorted(glob.glob(PG+'f*.jpg')); random.seed(7)
W,H=1080,1500; bg=Image.new('RGB',(W,H),(28,38,51)); 
noise=(np.random.RandomState(1).normal(0,5,(H,W,1))).repeat(3,2); bg=Image.fromarray((np.asarray(bg).astype(np.float32)+noise).clip(0,255).astype(np.uint8))
cols,rows=4,11; cw=W/cols*1.12; idx=list(range(len(fs))); random.shuffle(idx); k=0
for r in range(rows):
    for c in range(cols):
        if k>=len(idx): break
        im=trim(fs[idx[k]],'_tmp.jpg',int(cw*0.98)); k+=1
        ang=random.uniform(-7,7)
        a=im.convert('RGBA'); a=a.rotate(ang,expand=True,resample=Image.BICUBIC)
        sh=Image.new('RGBA',a.size,(0,0,0,0)); sh.putalpha(a.split()[3].point(lambda v:int(v*0.55))); sh=sh.filter(ImageFilter.GaussianBlur(9))
        x=int(c*W/cols - cw*0.06 + random.uniform(-14,14) + (r%2)*W/cols*0.35 - W/cols*0.2); y=int(r*H/rows*0.98 - 40 + random.uniform(-10,10))
        bg.paste(Image.new('RGB',a.size,(0,0,0)),(x+6,y+12),sh); bg.paste(a,(x,y),a)
os.remove(O+'_tmp.jpg'); bg.save(O+'wall.jpg',quality=88); print('wall',k)
