import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
        pg=await b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
        await pg.goto('https://share.google/I422FPPY7QHbYuOhg',wait_until='domcontentloaded')
        await pg.wait_for_timeout(6000)
        print(pg.url)
        t=await pg.inner_text('body')
        print(t[:4000])
        await pg.screenshot(path='research_google.png')
        await b.close()
asyncio.run(main())
