import asyncio,sys
from playwright.async_api import async_playwright
async def main(url,out):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
        pg=await b.new_page(locale='en-US',user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',viewport={'width':1400,'height':1000})
        await pg.goto(url,wait_until='domcontentloaded')
        await pg.wait_for_timeout(7000)
        open(out+'.txt','w').write(pg.url+'\n'+await pg.inner_text('body'))
        open(out+'.html','w').write(await pg.content())
        await pg.screenshot(path=out+'.png')
        await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2]))
