import asyncio,re,json
from playwright.async_api import async_playwright
URL="https://www.google.com/maps/place/13+Gypsies/@30.315061,-81.6891814,17z/data=!3m1!4b1!4m6!3m5!1s0x88e5b77e70ce003f:0x64ff0fd11cca072a!8m2!3d30.315061!4d-81.6891814!16s%2Fg%2F1hc1bsvmt?hl=en"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
        pg=await b.new_page(locale='en-US',user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',viewport={'width':1400,'height':1000})
        urls=set()
        pg.on('response',lambda r: urls.add(r.url) if 'googleusercontent' in r.url else None)
        await pg.goto(URL,wait_until='domcontentloaded'); await pg.wait_for_timeout(6000)
        # hours
        for lab in await pg.query_selector_all('[aria-label]'):
            a=await lab.get_attribute('aria-label')
            if a and ('Tuesday' in a or 'hours' in a.lower()): print('ARIA:',a[:600])
        # about tab
        try:
            await pg.click('button[role=tab]:has-text("About")'); await pg.wait_for_timeout(3000)
            print('ABOUT:\n',(await pg.inner_text('div[role=main]'))[:3000])
        except Exception as e: print('about err',e)
        try:
            await pg.click('button[role=tab]:has-text("Overview")'); await pg.wait_for_timeout(2000)
            await pg.click('button[aria-label^="See photos"], button:has-text("See photos")'); await pg.wait_for_timeout(4000)
            for i in range(25):
                await pg.mouse.move(300,500); await pg.mouse.wheel(0,2500); await pg.wait_for_timeout(700)
        except Exception as e: print('photo err',e)
        html=await pg.content()
        for m in re.findall(r'https://lh[0-9]\.googleusercontent\.com/[^"\'\)\s&;]+',html): urls.add(m)
        await pg.screenshot(path='research/gphotos.png')
        json.dump(sorted(urls),open('research/gurls.json','w'),indent=0)
        print(len(urls))
        await b.close()
asyncio.run(main())
