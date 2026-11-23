import asyncio,os,math,shutil
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=D+'/gif/secframes/s03b'
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
N=30
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome'); pg=await b.new_page(viewport={'width':432,'height':900},device_scale_factor=2.5)
        await pg.goto('file://'+D+'/page.html'); await pg.wait_for_timeout(800); await pg.evaluate('document.fonts.ready')
        for i in range(N):
            t=i/N
            await pg.evaluate('''([t])=>{const x=document.querySelector('#s03b .xm');const w=x.offsetWidth;
              const s=x.querySelector('.sh'); const k=Math.min(t/0.5,1); s.style.left=(-120+(w+240)*k)+'px';
              x.querySelectorAll('.sp').forEach((e,j)=>{const ph=(t*2+j*0.37)%1; const o=ph<0.35?Math.sin(ph/0.35*Math.PI):0; e.style.opacity=o; e.style.transform=`scale(${0.4+o*0.9}) rotate(${ph*90}deg)`;});
              return new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))}''',[t])
            await pg.locator('#s03b').screenshot(path=f'{OUT}/{i+1:03d}.png')
        await b.close()
asyncio.run(main())
