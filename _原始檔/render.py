import asyncio, os, sys
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=sys.argv[1] if len(sys.argv)>1 else D+'/out'
os.makedirs(OUT,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome')
        pg=await b.new_page(viewport={'width':432,'height':900},device_scale_factor=2.5)
        await pg.goto('file://'+D+'/page.html'); await pg.wait_for_timeout(800)
        await pg.evaluate('document.fonts.ready')
        ids=await pg.eval_on_selector_all('section','els=>els.map(e=>e.id)')
        for i in ids:
            await pg.locator('#'+i).screenshot(path=f'{OUT}/{i}.png')
        pass
        await b.close(); print(ids)
asyncio.run(main())
