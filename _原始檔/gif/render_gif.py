import asyncio, os, sys, subprocess, shutil
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR=D+'/gif/secframes'; os.makedirs(FR,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome')
        pg=await b.new_page(viewport={'width':432,'height':900},device_scale_factor=2.5)
        await pg.goto('file://'+D+'/page.html'); await pg.wait_for_timeout(800)
        await pg.evaluate('document.fonts.ready')
        items=await pg.eval_on_selector_all('[data-clip]','els=>els.map(e=>[e.closest("section").id,e.dataset.clip])')
        for sec,clip in items:
            od=f'{FR}/{sec}'; shutil.rmtree(od,ignore_errors=True); os.makedirs(od)
            files=sorted(os.listdir(f'{D}/gif/clips/{clip}'))
            for i,f in enumerate(files):
                url=f'gif/clips/{clip}/{f}'
                await pg.evaluate('''async ([c,u])=>{const im=new Image();im.src=u;await im.decode();document.querySelector(`[data-clip="${c}"]`).style.backgroundImage=`url(${u})`;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))}''',[clip,url])
                await pg.locator('#'+sec).screenshot(path=f'{od}/{i+1:03d}.png')
            print(sec,clip,len(files),flush=True)
        await b.close()
asyncio.run(main())
