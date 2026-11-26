import json, os, shutil, html
from data import *
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "docs")
E = html.escape
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..600,0..100;1,9..144,300..500,0..100&family=Instrument+Sans:wght@400;600&display=swap" rel="stylesheet">'
JS_HOURS = {0: None, 1: None, 2: [1020, 1260], 3: [1020, 1260], 4: [1020, 1260], 5: [1020, 1320], 6: [1020, 1320]}
DAYROWS = [(2, "Tuesday", "5 – 9 PM"), (3, "Wednesday", "5 – 9 PM"), (4, "Thursday", "5 – 9 PM"), (5, "Friday", "5 – 10 PM"), (6, "Saturday", "5 – 10 PM"), (0, "Sunday", "Closed"), (1, "Monday", "Closed")]
SAME = [MAPS, OT, "https://www.instagram.com/13gypsies/", "https://www.facebook.com/121461971272353", "https://www.visitjacksonville.com/directory/13-gypsies/"]

def restaurant_ld():
    return {
      "@context": "https://schema.org", "@type": "Restaurant", "@id": BASE + "#restaurant",
      "name": NAME, "url": BASE, "image": [BASE + "img/hero-icons-wide.webp", BASE + "img/storefront.webp"],
      "description": "Intimate Spanish tapas restaurant in Riverside, Jacksonville, open since 2008. Seven tables, a scratch kitchen and house-made bread, cheese, sausage and cured meats, in a 1923 Spanish-style building by Henrietta Dozier.",
      "telephone": TEL, "servesCuisine": ["Spanish", "Tapas", "Mediterranean"],
      "address": {"@type": "PostalAddress", "streetAddress": ADDR1, "addressLocality": CITY, "addressRegion": REGION, "postalCode": ZIP, "addressCountry": "US"},
      "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
      "hasMap": MAPS,
      "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "17:00", "closes": "21:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday"], "opens": "17:00", "closes": "22:00"}],
      "acceptsReservations": True,
      "potentialAction": {"@type": "ReserveAction", "target": {"@type": "EntryPoint", "urlTemplate": OT}, "result": {"@type": "FoodEstablishmentReservation", "name": "Table at 13 Gypsies"}},
      "hasMenu": BASE + "menu.html",
      "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.5, "reviewCount": 462, "bestRating": 5},
      "founder": {"@type": "Person", "name": "Howard Kirk"},
      "employee": {"@type": "Person", "name": "Kevan Kimball", "jobTitle": "Chef"},
      "foundingDate": "2008",
      "paymentAccepted": "American Express, Discover, Mastercard, Visa",
      "sameAs": SAME,
    }

ICONS = {
 "tv": '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="6" y="12" width="36" height="24" rx="2"/><path d="M18 42h12M24 36v6M17 4l7 8 7-8"/></svg>',
 "laurel": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 42c-9-2-15-10-15-20M24 42c9-2 15-10 15-20"/><path d="M10 28c3 0 5 2 6 4M9 21c3 0 5 2 6 4M11 14c2 1 4 3 4 5M38 28c-3 0-5 2-6 4M39 21c-3 0-5 2-6 4M37 14c-2 1-4 3-4 5"/><circle cx="24" cy="20" r="5"/></svg>',
 "star": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 6l5.3 11.6 12.7 1.3-9.5 8.6 2.7 12.5L24 33.6l-11.2 6.4 2.7-12.5L6 18.9l12.7-1.3z"/></svg>',
 "ribbon": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="18" r="11"/><circle cx="24" cy="18" r="6"/><path d="M16 26l-5 15 7-3 4 6 3-12M32 26l5 15-7-3-4 6-3-12"/></svg>',
 "paper": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 10h28v28a4 4 0 0 0 4 4H12a4 4 0 0 1-4-4z"/><path d="M36 18h4v20a2 2 0 0 1-4 0M14 17h16M14 23h16M14 29h10"/></svg>',
}

def head(title, desc, path, extra_ld=None, preload=None):
    url = BASE + path
    lds = [restaurant_ld()] + ([extra_ld] if extra_ld else [])
    ld = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in lds)
    pre = preload or ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="restaurant"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/og.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#2A1C29">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png">
{pre}{FONTS}<link rel="stylesheet" href="style.css?v={V}">{ld}</head><body>'''

def header(page):
    home = "" if page == "home" else "index.html"
    cur = ' aria-current="page"' if page == "menu" else ""
    cls = "hdr" if page == "home" else "hdr always"
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="{cls}"><div class="wrap"><a class="mark" href="{home or '#top'}" aria-label="13 Gypsies, home"><b>13</b> Gypsies</a>
<nav class="nav" aria-label="Main"><a class="n-story" href="{home}#story">Story</a><a class="n-room" href="{home}#room">The Room</a><a class="n-private" href="{home}#private">Private</a><a class="n-visit" href="{home}#visit">Visit</a><a class="n-menu" href="menu.html"{cur}>Menu</a></nav>
<a class="btn" href="{OT}" target="_blank" rel="noopener">Reserve</a></div></header>'''

def footer(page):
    home = "" if page == "home" else "index.html"
    third = '<a href="menu.html">Menu</a>' if page != "menu" else '<a href="index.html">Home</a>'
    return f'''<footer class="ftr"><div class="wrap">
<div><a class="mark" href="{home or '#top'}"><b>13</b> Gypsies</a><p style="margin-top:18px">Spanish tapas from a scratch kitchen.<br>Riverside, Jacksonville, since 2008.</p></div>
<div><h3>Visit</h3><p><a href="{MAPS}" target="_blank" rel="noopener">{ADDR1}<br>{CITY}, {REGION} {ZIP}</a></p><p><a href="tel:{TEL}">{PHONE}</a></p></div>
<div><h3>Hours</h3><p>Tue – Thu · 5 – 9 PM</p><p>Fri – Sat · 5 – 10 PM</p><p>Sun – Mon · Closed</p></div>
<div><h3>Reserve</h3><p><a href="{OT}" target="_blank" rel="noopener">OpenTable</a></p><p><a href="tel:{TEL}">Call during service hours</a></p><p><a href="menu.html">The menu</a></p><p><a href="https://www.instagram.com/13gypsies/" target="_blank" rel="noopener">Instagram</a></p></div>
<div class="small"><span>© <span data-year>2026</span> 13 Gypsies · {ADDR1}, {CITY}, {REGION} {ZIP}</span><span>Design preview by RGWebD</span></div>
</div></footer>
<nav class="mbar" aria-label="Quick actions"><a href="{OT}" target="_blank" rel="noopener">Reserve</a><a href="tel:{TEL}">Call</a>{third}</nav>
<script>window.__HOURS={json.dumps(JS_HOURS)};window.__HOL={json.dumps(HOLIDAYS)};</script><script src="main.js?v={V}" defer></script></body></html>'''

def tile(slug, label, alt, hidden=False):
    ah = ' aria-hidden="true"' if hidden else ""
    altv = "" if hidden else E(alt)
    return f'<li{ah}><figure class="tile"><div class="ph"><img src="img/dish-{slug}.webp" alt="{altv}" width="560" height="560" loading="lazy" decoding="async"></div><figcaption>{E(label)}</figcaption></figure></li>'

def marquee(items, rev=False):
    a = "".join(tile(*x) for x in items) + "".join(tile(*x, hidden=True) for x in items)
    return f'<div class="mq{" rev" if rev else ""}"><ul class="mq-track">{a}</ul></div>'

def home():
    hours_rows = "".join(f'<tr data-dow="{d}"><th scope="row">{n}</th><td>{h}</td></tr>' for d, n, h in DAYROWS)
    creds = [
      ("tv", "Diners, Drive-Ins &amp; Dives", "As seen on Food Network · 2010"),
      ("laurel", "Best Tapas", "Folio Weekly · Best of Jax 2015"),
      ("star", "4.9 on OpenTable", "From 691 diner reviews"),
      ("ribbon", "Diners’ Choice", "OpenTable · Best Value, Jacksonville"),
      ("paper", "Florida Times-Union", "Romantic restaurants · 2026"),
    ]
    creds_html = "".join(f'<li class="cred">{ICONS[i]}<b>{t}</b><span>{s}</span></li>' for i, t, s in creds)
    preload = '<link rel="preload" as="image" href="img/hero-icons-tall.webp" media="(max-width:760px)"><link rel="preload" as="image" href="img/hero-icons-wide.webp" media="(min-width:761px)">'
    body = head("13 Gypsies · Spanish Tapas in Riverside, Jacksonville FL",
                "13 Gypsies: seven tables of Spanish tapas from a scratch kitchen at 887 Stockton St, Riverside, Jacksonville. House-made bread, cheese and chorizo since 2008. Reserve on OpenTable.",
                "", preload=preload)
    body += header("home")
    body += f'''<main id="main">
<section class="hero" id="top" aria-label="Welcome">
<picture><source media="(max-width:760px)" srcset="img/hero-icons-tall.webp"><img src="img/hero-icons-wide.webp" alt="The 13 Gypsies dining room wall: gilt-framed saints and icons around the chalkboard of house-made desserts" width="1500" height="1000" fetchpriority="high"></picture>
<div class="hero-in">
<h1>Spanish tapas · Riverside, Jacksonville</h1>
<p class="word" aria-label="13 Gypsies">13 <i>Gypsies</i></p>
<a class="btn light" href="{OT}" target="_blank" rel="noopener">Reserve a table</a>
<p class="meta"><span data-status>Tue – Sat from 5 PM</span> · {ADDR1}</p>
</div></section>

<section class="sec story" id="story" aria-labelledby="story-h"><div class="wrap">
<div class="narrow">
<p class="eyebrow rv">Since 2008 · Stockton Street</p>
<h2 id="story-h" class="rv">Out with the new,<br><i>in with the old.</i></h2>
<p class="lede rv">Seven tables, twenty seats and a kitchen that still kneads its bread by hand every morning. They own no mixers.</p>
<p class="rv">Chef Howard Kirk opened 13 Gypsies in 2008 to cook the simple Spanish food he grew up on. Chef Kevan Kimball runs the kitchen today, and almost everything is still made in house: sausage, cheese, cured meats, pickles, spice blends and fresh pasta. When a dish runs out, it’s gone for the night. First come, first eat.</p>
<blockquote class="quote rv"><p>“If you start with good ingredients, preparation is minimal and the end result is good, honest food.”</p><cite>The 13 Gypsies kitchen creed</cite></blockquote>
<ul class="facts rv"><li>7 tables</li><li>20 seats</li><li>Built 1923</li><li>Bread by hand, daily</li></ul>
</div>
<ul class="creds rv" aria-label="Recognition">{creds_html}</ul>
</div></section>

<section class="mq-sec" aria-labelledby="mq-h"><div class="wrap">
<div class="mq-head"><div><p class="eyebrow">Small plates, passed around</p><h2 id="mq-h">Across <i>the table</i></h2></div>
<p>Order a few, share everything. A few plates from the kitchen, photographed by guests at the table.</p>
<button class="mq-toggle" type="button" aria-pressed="false">Pause</button></div></div>
<div class="mq-wrap">{marquee(MARQUEE_A)}{marquee(MARQUEE_B, rev=True)}</div>
<div class="wrap"><p class="mq-note">The menu changes often. <a href="menu.html">See the dishes on the menu</a>.</p></div>
</section>

<section class="sec" id="dine" aria-labelledby="dine-h"><div class="wrap">
<p class="eyebrow rv">The evening</p>
<h2 id="dine-h" class="rv">How dinner <i>works</i></h2>
<div class="formats">
<div class="fmt rv"><span class="n">I</span><h3>Tapas, hot &amp; cold</h3><p>Spanish small plates with a wandering Mediterranean streak, made for passing. Most tables order several and share.</p><span class="price">Every plate under $20</span></div>
<div class="fmt rv"><span class="n">II</span><h3>Daily offerings</h3><p>A risotto of the day, and dry-cured meat from the house chamber with grilled peasant bread.</p><span class="price">Ask what’s on tonight</span></div>
<div class="fmt rv"><span class="n">III</span><h3>Bring a bottle</h3><p>The list leans Spanish and the beer is Florida-local, or bring your own wine.</p><span class="price">$15 corkage</span></div>
<div class="fmt rv"><span class="n">IV</span><h3>Housemade desserts</h3><p>Tres leches and a mason jar cheesecake, written on the board by the icon wall.</p><span class="price">Allow <em class="tbc">[about 1½ – 2 hours]</em></span></div>
</div>
<p class="notes-line rv"><span><strong>Last seating</strong> 90 minutes before close</span><span><strong>Dress</strong> casual</span><span><strong>Gluten-free</strong> options</span></p>
</div></section>

<section class="sec paper" id="room" aria-labelledby="room-h"><div class="wrap split">
<figure class="ph rv"><img src="img/room-arched-window.webp" alt="Tables by the arched front window over the original black-and-white mosaic tile floor" width="1200" height="1600" loading="lazy" decoding="async"><figcaption>The front window and the original 1923 floor tile.</figcaption></figure>
<div>
<p class="eyebrow rv">The room</p>
<h2 id="room-h" class="rv">A 1923 corner <i>on Stockton</i></h2>
<p class="lede rv">A two-story Spanish-style building designed by Henrietta Dozier, Jacksonville’s only female architect in the early twentieth century.</p>
<p class="rv">Inside: the original floor tile, gilt-framed saints and icons, a Last Supper in silver relief, and a handful of sidewalk tables out front. Small, close and a little lively, the way a neighborhood bistro should be.</p>
</div></div></section>

<section class="sec dark" id="private" aria-labelledby="private-h"><div class="wrap split flip">
<figure class="ph rv"><img src="img/private-last-supper.webp" alt="A silver-relief Last Supper in a gilt frame beneath a tiled 13 Gypsies sign, above a wooden table" width="1100" height="1467" loading="lazy" decoding="async"><figcaption>The Last Supper, above one of the seven tables.</figcaption></figure>
<div>
<p class="eyebrow rv">Private dining</p>
<h2 id="private-h" class="rv">The whole room, <i>yours</i></h2>
<p class="lede rv">Book the restaurant for one all-inclusive flat rate: food, drinks, room, tax and gratuity.</p>
<p class="rv">Rehearsal dinners, holiday parties, birthdays. Every party is planned on the phone with the team. Catering is available too.</p>
<ul class="kv rv">
<li><span>Seats</span><span>Up to 20 in the dining room <em class="tbc">[confirm max party size]</em></span></li>
<li><span>Seatings</span><span><em class="tbc">[seating times]</em></span></li>
<li><span>Rate</span><span>Flat, all-inclusive <em class="tbc">[$ per guest]</em></span></li>
</ul>
<div class="ctas rv"><a class="btn light" href="tel:{TEL}">Call {PHONE}</a></div>
</div></div></section>

<section class="sec dark reserve" id="reserve" aria-labelledby="reserve-h" style="border-top:1px solid rgba(251,248,242,.12)"><div class="wrap">
<p class="eyebrow rv">Reservations</p>
<h2 id="reserve-h" class="rv">Your table <i>awaits</i></h2>
<p class="lede rv">With seven tables, it fills fast. Book on OpenTable, or call during service hours and talk to a person. Reservations aren’t taken by email or voicemail.</p>
<div class="ot-box rv"><div class="ot-frame" data-ot="{OT_RID}"><a class="btn" href="{OT}" target="_blank" rel="noopener">Reserve on OpenTable</a></div>
<p class="ot-fallback">Booking window: <em class="tbc">[how far ahead tables open]</em> · Prefer the phone? <a href="tel:{TEL}">{PHONE}</a></p></div>
<div class="ctas rv"><a class="btn light" href="{OT}" target="_blank" rel="noopener">Reserve on OpenTable</a><a class="btn line-light" href="tel:{TEL}">Call {PHONE}</a></div>
<p class="rating-line rv">4.9 on OpenTable · 691 reviews</p>
<ul class="reviews">
<li class="rv"><blockquote><p>“Our favorite Jacksonville dining experience! The Tres Leches cake is one of the best restaurant desserts we’ve ever had!”</p><cite>Karly · OpenTable · Nov 2026</cite></blockquote></li>
<li class="rv"><blockquote><p>“Great bottles for great prices, really flavorful shareables you can’t find anywhere else in the area, and a very cozy setting.”</p><cite>Owen · OpenTable · Oct 2026</cite></blockquote></li>
<li class="rv"><blockquote><p>“One of the best restaurants in Jacksonville! We love the gnocchi.”</p><cite>Holly · OpenTable · Nov 2026</cite></blockquote></li>
</ul>
</div></section>

<section class="sec" id="visit" aria-labelledby="visit-h"><div class="wrap">
<p class="eyebrow rv">Visit</p>
<h2 id="visit-h" class="rv">Find <i>us</i></h2>
<div class="visit-grid">
<div class="rv">
<p class="addr">{ADDR1}<br>{CITY}, {REGION} {ZIP}</p>
<p style="margin:0;color:var(--muted)">Riverside, at Stockton &amp; College, just off I-10</p>
<p class="status" data-status>Tue – Sat from 5 PM</p>
<table class="hours"><caption class="sr">Opening hours</caption>{hours_rows}</table>
<div class="ctas"><a class="btn" href="{OT}" target="_blank" rel="noopener">Reserve</a><a class="btn ghost" href="{MAPS}" target="_blank" rel="noopener">Directions</a><a class="btn ghost" href="tel:{TEL}">Call</a></div>
</div>
<figure class="ph rv" style="margin:0"><img src="img/storefront.webp" alt="The 13 Gypsies storefront: black awning, Tapas &amp; Vino Panaderia lettering and red sidewalk chairs" width="1600" height="1200" loading="lazy" decoding="async"></figure>
</div>
<ul class="pol">
<li class="rv"><h3>Dress code</h3><p>Casual. In their words: “Come in shorts and a t-shirt, we don’t care, this is your place.”</p></li>
<li class="rv"><h3>Wine &amp; corkage</h3><p>Spanish wines and Florida beer. Bring your own bottle for a $15 corkage fee.</p></li>
<li class="rv"><h3>Parking</h3><p>Street parking on Stockton and the nearby blocks.</p></li>
<li class="rv"><h3>Last seating</h3><p>An hour and a half before closing. Items can sell out, since everything is made in house.</p></li>
<li class="rv"><h3>Access</h3><p>Wheelchair-accessible entrance, seating and restroom. A few sidewalk tables outside.</p></li>
<li class="rv"><h3>Holidays</h3><p>Hours may change around Thanksgiving and other holidays. Please call to confirm.</p></li>
</ul>
</div></section>
</main>'''
    body += footer("home")
    return body

def menu():
    chips = '<button class="chip" type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button class="chip" type="button" data-cat="{k}" aria-pressed="false">{E(t)}</button>' for k, t, _ in MENU)
    secs = ""
    ld_secs = []
    for k, t, items in MENU:
        lis = ""
        ld_items = []
        for it in items:
            nm, desc = it[0], it[1]
            b = ' <span class="badge" title="Featured on Diners, Drive-Ins and Dives, 2010">Seen on Triple D</span>' if len(it) > 2 else ""
            lis += f'<li class="item"><h3><span class="nm">{E(nm)}</span>{b}</h3><p>{E(desc)}</p></li>'
            ld_items.append({"@type": "MenuItem", "name": nm, "description": desc})
        secs += f'<section class="msec" data-cat="{k}" id="m-{k}" aria-labelledby="h-{k}"><h2 id="h-{k}">{E(t)}</h2><ul class="items">{lis}</ul></section>'
        ld_secs.append({"@type": "MenuSection", "name": t, "hasMenuItem": ld_items})
    ld = {"@context": "https://schema.org", "@type": "Menu", "name": "13 Gypsies dinner menu", "url": BASE + "menu.html", "inLanguage": "en", "hasMenuSection": ld_secs}
    body = head("Menu · 13 Gypsies Spanish Tapas, Jacksonville",
                "The 13 Gypsies tapas menu: cold and hot small plates, Roman-style gnocchi, house-made chorizo and ricotta, daily risotto and housemade desserts. Riverside, Jacksonville.",
                "menu.html", extra_ld=ld)
    body += header("menu")
    body += f'''<main id="main">
<section class="mhero"><div class="wrap">
<p class="eyebrow">The menu</p><h1 style="font-size:clamp(46px,7vw,92px)">Tapas, <i style="color:var(--gilt-d)">mostly Spanish</i></h1>
<p class="lede" style="color:var(--ink)">Hot and cold small plates, a risotto of the day and meat cured in the house chamber.</p>
<p>The menu changes often and dishes sell out, so call for tonight’s offerings. Every plate is under $20.</p>
<div class="ctas"><a class="btn" href="{OT}" target="_blank" rel="noopener">Reserve a table</a><a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a></div>
</div></section>
<div class="mtools"><div class="wrap"><div class="chips" role="group" aria-label="Filter by course">{chips}</div>
<label class="sr" for="q">Search the menu</label><input id="q" class="search" type="search" placeholder="Search: chorizo, gnocchi…" autocomplete="off"></div></div>
<div class="wrap" id="menu-list">{secs}
<p class="empty" hidden>Nothing matches that. Try another word, or call {PHONE} to ask what’s on tonight.</p>
<p class="mnote">Dishes as listed on 13 Gypsies’ OpenTable menu (last updated April 2022) and the dessert board in the dining room. Prices aren’t shown because they may have changed. The Florida Times-Union (Feb 2026) notes nothing on the menu costs $20. Please tell your server about allergies. Consuming raw or undercooked meats, poultry, seafood, shellfish or eggs may increase your risk of foodborne illness.</p>
</div>
</main>'''
    body += footer("menu")
    return body

def notfound():
    body = head("Page not found · 13 Gypsies", "This page doesn’t exist. Head back to 13 Gypsies, Spanish tapas in Riverside, Jacksonville.", "404.html")
    body = body.replace('href="style.css', 'href="/13gypsies-v3/style.css').replace('href="favicon', 'href="/13gypsies-v3/favicon').replace('href="apple-touch', 'href="/13gypsies-v3/apple-touch')
    body += f'''<main id="main" class="sec" style="min-height:80vh;display:flex;align-items:center"><div class="wrap narrow">
<p class="eyebrow">404</p><h1 style="font-size:clamp(46px,7vw,88px)">This plate <i style="color:var(--gilt-d)">ran out.</i></h1>
<p class="lede">First come, first eat. The page you wanted isn’t here.</p>
<div class="ctas"><a class="btn" href="/13gypsies-v3/">Back to 13 Gypsies</a><a class="btn ghost" href="/13gypsies-v3/menu.html">See the menu</a><a class="btn ghost" href="{OT}">Reserve</a></div>
</div></main></body></html>'''
    return body

def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w").write(home())
    open(os.path.join(OUT, "menu.html"), "w").write(menu())
    open(os.path.join(OUT, "404.html"), "w").write(notfound())
    shutil.copy(os.path.join(ROOT, "style.css"), OUT)
    shutil.copy(os.path.join(ROOT, "main.js"), OUT)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url><url><loc>{BASE}menu.html</loc></url></urlset>\n')
    open(os.path.join(OUT, "llms.txt"), "w").write(f"""# 13 Gypsies

> Intimate Spanish tapas restaurant in Riverside, Jacksonville, Florida, open since 2008. Seven tables, twenty seats, a scratch kitchen (bread kneaded by hand daily; house-made sausage, cheese, cured meats, pickles, spice blends and pasta) in a 1923 Spanish-style building designed by Henrietta Dozier.

- Address: {ADDR1}, {CITY}, {REGION} {ZIP} (Stockton St at College St, off I-10)
- Phone: {PHONE} (reservations by phone during service hours or OpenTable; not by email or voicemail)
- Reservations: {OT}
- Hours: Tue-Thu 5-9 PM; Fri-Sat 5-10 PM; Sun-Mon closed. Last seating 90 minutes before close.
- Chef: Kevan Kimball. Founder: Chef Howard Kirk.
- Policies: casual dress; BYO wine $15 corkage; street parking; wheelchair accessible; private buyouts at an all-inclusive flat rate (call).
- Recognition: Diners, Drive-Ins and Dives ("Globetrottin'", 2010); Folio Weekly Best of Jax 2015 Best Tapas; OpenTable 4.9 (691 reviews); Google 4.5 (462 reviews).

## Pages
- [Home]({BASE}): story, the room, private dining, reservations, hours and policies
- [Menu]({BASE}menu.html): tapas menu (names and descriptions; menu changes often)
""")

if __name__ == "__main__":
    main()
    print("built")
