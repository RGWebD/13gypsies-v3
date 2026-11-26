import asyncio,sys,json
from playwright.async_api import async_playwright
BASE=sys.argv[1]; TAG=sys.argv[2]
OUT='/workspace/13gypsies-v3/qa/'
async def run(p,bname,w):
    br=await getattr(p,bname).launch()
    h=844 if w==390 else 900
    ctx=await br.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
    res={}
    for page_name in ['','menu.html']:
        pg=await ctx.new_page(); errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto(BASE+page_name,wait_until='load'); await pg.wait_for_timeout(1200)
        title=await pg.title()
        if page_name=='':
            await pg.screenshot(path=f'{OUT}{TAG}_{bname}_{w}_hero.png')
        # scroll through
        H=await pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,500):
            await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(800)
        info=await pg.evaluate('''()=>{
          const ov=document.documentElement.scrollWidth>window.innerWidth+1;
          const wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>window.innerWidth+1 && !e.closest('.mq') && getComputedStyle(e).position!=='fixed' && r.width>0}).slice(0,5).map(e=>e.className||e.tagName);
          const broken=[...document.querySelectorAll('img')].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src);
          const srcs=[...document.querySelectorAll('img:not([aria-hidden])')].filter(i=>!i.closest('[aria-hidden=true]')).map(i=>i.currentSrc||i.src);
          const dup=srcs.filter((s,i)=>srcs.indexOf(s)!==i);
          const menu=[...document.querySelectorAll('.nav .n-menu')].map(a=>{const r=a.getBoundingClientRect();return r.width>0&&getComputedStyle(a).display!=='none'})[0];
          const small=[...document.querySelectorAll('p,li,td,th')].filter(e=>e.offsetParent&&parseFloat(getComputedStyle(e).fontSize)<16&&e.textContent.trim().length>40).length;
          const leak=/\\{[A-Z_]+\\}/.test(document.body.innerText);
          return {ov,wide,broken,dup,menu,small,leak};
        }''')
        res[page_name or 'home']=dict(title=title,errs=errs[:5],**info)
        await pg.screenshot(path=f'{OUT}{TAG}_{bname}_{w}_{page_name or "home"}_full.png',full_page=True)
        if page_name=='menu.html':
            # filter while scrolled
            await pg.evaluate('window.scrollTo(0,document.body.scrollHeight*0.7)'); await pg.wait_for_timeout(300)
            await pg.click('.chip[data-cat=dessert]'); await pg.wait_for_timeout(1200)
            vis=await pg.evaluate('''()=>{const s=document.querySelector('#m-dessert');const r=s.getBoundingClientRect();return r.top<window.innerHeight&&r.bottom>0}''')
            await pg.click('.chip[data-cat=all]'); await pg.wait_for_timeout(600)
            await pg.evaluate('window.scrollTo(0,document.body.scrollHeight*0.8)')
            await pg.fill('.search','gnocchi'); await pg.wait_for_timeout(1200)
            vis2=await pg.evaluate('''()=>{const it=[...document.querySelectorAll('.item')].find(i=>!i.hidden);const r=it.getBoundingClientRect();return r.top<window.innerHeight&&r.bottom>0}''')
            res['menu.html']['filter_visible']=vis; res['menu.html']['search_visible']=vis2
            bar=await pg.evaluate('''()=>[...document.querySelectorAll('.mbar a')].map(a=>a.getAttribute('href'))''')
            res['menu.html']['mbar']=bar
        await pg.close()
    # reduced motion
    ctx2=await br.new_context(viewport={'width':w,'height':900},reduced_motion='reduce')
    pg=await ctx2.new_page(); await pg.goto(BASE,wait_until='load'); await pg.wait_for_timeout(800)
    hid=await pg.evaluate('''()=>[...document.querySelectorAll('.rv')].filter(e=>parseFloat(getComputedStyle(e).opacity)<1).length''')
    res['reduced_hidden']=hid
    await br.close()
    return res
async def main():
    async with async_playwright() as p:
        allr={}
        for b in ['chromium','webkit']:
            for w in [390,1024,1440]:
                try: allr[f'{b}_{w}']=await run(p,b,w)
                except Exception as e: allr[f'{b}_{w}']=str(e)[:300]
        print(json.dumps(allr,indent=1))
asyncio.run(main())
