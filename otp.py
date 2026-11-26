import asyncio,re,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
        pg=await b.new_page(locale='en-US',user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',viewport={'width':1400,'height':1000})
        imgs=set()
        pg.on('response',lambda r: imgs.add(r.url) if 'otstatic.com' in r.url and 'photos' in r.url else None)
        await pg.goto('https://www.opentable.com/r/13-gypsies-jacksonville',wait_until='domcontentloaded'); await pg.wait_for_timeout(6000)
        try:
            await pg.click('text=See all 117 photos',timeout=5000)
        except Exception as e:
            await pg.click('text=+112 More',timeout=5000)
        await pg.wait_for_timeout(4000)
        for i in range(40):
            await pg.mouse.move(700,500); await pg.mouse.wheel(0,1200); await pg.wait_for_timeout(400)
        h=await pg.content()
        for m in re.findall(r'https://resizer\.otstatic\.com/v[23]/photos/[^"\'\s\\)]+',h): imgs.add(m)
        await pg.screenshot(path='research/ot_photos.png')
        json.dump(sorted(imgs),open('research/ot_imgs.json','w'),indent=0)
        print(len(imgs)); await b.close()
asyncio.run(main())
