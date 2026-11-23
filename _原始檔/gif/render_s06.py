import asyncio, os, json
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
info=json.load(open(D+'/gif/s06_days.json')); OUT=D+'/gif/secframes/s06'; os.makedirs(OUT,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome')
        pg=await b.new_page(viewport={'width':432,'height':900},device_scale_factor=2.5)
        await pg.goto('file://'+D+'/page.html'); await pg.wait_for_timeout(800); await pg.evaluate('document.fonts.ready')
        for n,i in enumerate(info):
            d=f"{i['d']:03d}"
            await pg.evaluate("""([d,lead])=>new Promise(r=>{const s=document.querySelector('#s06');s.querySelector('.lead').textContent=lead;
              const a=s.querySelector('#pf'),b=s.querySelector('#pb');let c=0;const done=()=>{if(++c==2)requestAnimationFrame(()=>requestAnimationFrame(r))};
              a.onload=done;b.onload=done;a.src='img/p'+d+'_1.jpg';b.src='img/p'+d+'_2.jpg';})""",[d,i['lead']])
            await pg.locator('#s06').screenshot(path=f'{OUT}/{n:03d}.png')
        await b.close()
asyncio.run(main())
