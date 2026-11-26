import asyncio,re,json,sys
from playwright.async_api import async_playwright
async def main(url,tag):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
        pg=await b.new_page(locale='en-US',user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',viewport={'width':1400,'height':1000})
        urls=set()
        pg.on('response',lambda r: urls.add(r.url) if ('scontent' in r.url or 'fbcdn' in r.url or 'yelpcdn' in r.url or 'cdninstagram' in r.url) else None)
        await pg.goto(url,wait_until='domcontentloaded'); await pg.wait_for_timeout(7000)
        for sel in ['div[aria-label="Close"]','[aria-label="Close"]']:
            try: await pg.click(sel,timeout=2000)
            except: pass
        for i in range(10): await pg.mouse.wheel(0,1500); await pg.wait_for_timeout(700)
        open(f'research/{tag}.txt','w').write(pg.url+'\n'+await pg.inner_text('body'))
        h=await pg.content(); open(f'research/{tag}.html','w').write(h)
        await pg.screenshot(path=f'research/{tag}.png')
        json.dump(sorted(urls),open(f'research/{tag}_imgs.json','w'),indent=0)
        print(tag,len(urls)); await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2]))
