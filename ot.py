import asyncio,re,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
        pg=await b.new_page(locale='en-US',user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',viewport={'width':1400,'height':1000})
        imgs=set()
        pg.on('response',lambda r: imgs.add(r.url) if 'resizer' in r.url or 'otstatic' in r.url and re.search(r'\.(jpg|jpeg|png|webp)',r.url) else None)
        await pg.goto('https://www.opentable.com/r/13-gypsies-jacksonville',wait_until='domcontentloaded'); await pg.wait_for_timeout(8000)
        for i in range(12): await pg.mouse.wheel(0,1500); await pg.wait_for_timeout(500)
        open('research/ot.txt','w').write(await pg.inner_text('body'))
        h=await pg.content(); open('research/ot.html','w').write(h)
        for m in re.findall(r'https://resizer\.otstatic\.com/v[23]/photos/[^"\'\s\\]+',h): imgs.add(m)
        json.dump(sorted(imgs),open('research/ot_imgs.json','w'),indent=0)
        print(len(imgs)); await b.close()
asyncio.run(main())
