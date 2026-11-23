import subprocess,json,os,shutil
from concurrent.futures import ThreadPoolExecutor
M="/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/01_廣告投放/旅行機票日曆/毛片/"
FPS=15
# name: (src, t0, t1, speed, cy)
C={
 'g1_tear':  (M+'丁丁_Log_0912_調色對齊麻豆/C0124.mp4', 10.0, 13.6, 1.0, 0.45),  # v14 改中文版
 'g2_flip':  (M+'大C_B/影片檔_調色對齊麻豆/C3680.mp4', 38.5, 48.5, 1.4, 0.60),  # v14 改中文版
 'g3_write': (M+'阿寧_毛片/IMG_4482.MOV', 44.0, 52.0, 2.0, 0.55),
 's07_tree': (M+'大C_B/影片檔_調色對齊麻豆/C3673.mp4', 9.0, 17.0, 2.0, 0.55),
 's08_page': (M+'丁丁_Log_0912_調色對齊麻豆/C0123.mp4', 3.0, 9.6, 1.4, 0.55),
}
def dims(src):
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height:stream_side_data=rotation:stream_tags=rotate','-of','json',src]))
    s=j['streams'][0]; w,h=s['width'],s['height']
    rot=0
    for sd in s.get('side_data_list',[]) or []:
        if 'rotation' in sd: rot=int(sd['rotation'])
    if abs(rot)==90: w,h=h,w
    return w,h
def run(item):
    n,(src,t0,t1,sp,cy)=item
    w,h=dims(src); ch=round(w*5/4); y=min(max(round(cy*h-ch/2),0),h-ch)
    od=f'gif/clips/{n}'; shutil.rmtree(od,ignore_errors=True); os.makedirs(od)
    pre='colorspace=all=bt709:iall=bt2020:itrc=bt709:format=yuv420p,' if 'IMG_4482' in src else 'scale=in_color_matrix=bt709:out_color_matrix=bt709,'
    vf=f'{pre}setpts=PTS/{sp},fps={FPS},crop={w}:{ch}:0:{y},scale=1080:1350:flags=lanczos,eq=saturation=1.45:contrast=1.05'
    subprocess.run(['ffmpeg','-v','error','-ss',str(t0),'-t',str(t1-t0),'-i',src,'-vf',vf,'-q:v','2',f'{od}/%03d.jpg'],check=True)
    return n,(w,h),len(os.listdir(od))
import sys
sel=sys.argv[1:] or list(C)
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(run,[(k,C[k]) for k in sel]): print(r)
