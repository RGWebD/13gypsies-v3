(function(){
  var d=document, root=d.documentElement;
  var HOURS=window.__HOURS||{}, HOL=window.__HOL||{};
  var DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
  function nowNY(){
    var p=new Intl.DateTimeFormat("en-US",{timeZone:"America/New_York",year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",hour12:false,weekday:"short"}).formatToParts(new Date());
    var o={};p.forEach(function(x){o[x.type]=x.value});
    var wd=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].indexOf(o.weekday);
    var h=parseInt(o.hour,10)%24;
    return {dow:wd,min:h*60+parseInt(o.minute,10),date:o.year+"-"+o.month+"-"+o.day,y:+o.year,m:+o.month,d:+o.day};
  }
  function fmt(m){var h=Math.floor(m/60),mm=m%60,ap=h>=12?"PM":"AM";h=h%12||12;return h+(mm?":"+(mm<10?"0":"")+mm:"")+" "+ap}
  function addDays(n,k){var t=new Date(Date.UTC(n.y,n.m-1,n.d+k));return t.toISOString().slice(0,10)}
  function status(){
    var n=nowNY(), today=HOURS[n.dow], hol=HOL[n.date], out={cls:"",txt:""};
    // JS dow 0=Sun; HOURS keyed by JS dow
    if(today && n.min<today[1]){
      if(n.min>=today[0]){out.txt="Open now · until "+fmt(today[1]); out.cls="";}
      else {out.txt="Opens tonight at "+fmt(today[0]); out.cls="closed";}
      if(hol){out.txt+=" ("+hol+": hours might differ, please call)"; out.cls="unk";}
      return out;
    }
    for(var k=1;k<8;k++){
      var dw=(n.dow+k)%7, h=HOURS[dw];
      if(h){
        var label=k===1?"tomorrow":DAYS[dw];
        out.txt="Closed now · opens "+label+" at "+fmt(h[0]); out.cls="closed";
        var hd=HOL[addDays(n,k)]; if(hd) out.txt+=" ("+hd+": hours might differ)";
        return out;
      }
    }
    return out;
  }
  try{
    var s=status();
    d.querySelectorAll("[data-status]").forEach(function(el){
      el.innerHTML='<span class="dot '+s.cls+'" aria-hidden="true"></span>'+s.txt;
    });
    var nd=nowNY().dow;
    d.querySelectorAll(".hours tr[data-dow]").forEach(function(tr){if(+tr.dataset.dow===nd)tr.classList.add("today")});
  }catch(e){}

  // header + mobile bar
  var hdr=d.querySelector(".hdr"), mbar=d.querySelector(".mbar"), hero=d.querySelector(".hero");
  function onScroll(){
    var y=window.scrollY||0, lim=hero?hero.offsetHeight-80:0;
    if(hdr && !hdr.classList.contains("always")) hdr.classList.toggle("solid",y>lim);
    if(mbar) mbar.classList.toggle("show", hero? y>hero.offsetHeight*0.55 : y>120);
  }
  window.addEventListener("scroll",onScroll,{passive:true}); onScroll();

  // reveal
  var rvs=d.querySelectorAll(".rv");
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});
    rvs.forEach(function(el){io.observe(el)});
  } else rvs.forEach(function(el){el.classList.add("in")});

  // marquee pause toggle (button + tap on touch)
  var mqs=d.querySelector(".mq-wrap"), tg=d.querySelector(".mq-toggle");
  if(mqs&&tg){
    tg.addEventListener("click",function(){var p=mqs.classList.toggle("paused");tg.setAttribute("aria-pressed",p);tg.textContent=p?"Play":"Pause"});
    mqs.addEventListener("touchstart",function(e){if(e.target.closest(".mq")){var p=mqs.classList.toggle("paused");tg.setAttribute("aria-pressed",p);tg.textContent=p?"Play":"Pause"}},{passive:true});
  }

  // OpenTable widget, loaded near view
  var ot=d.querySelector("[data-ot]");
  if(ot){
    var load=function(){
      if(ot.dataset.done)return; ot.dataset.done=1;
      var w=ot.clientWidth>=700?"wide":"standard";
      var sc=d.createElement("script");
      sc.src="https://www.opentable.com/widget/reservation/loader?rid="+ot.dataset.ot+"&type=standard&theme="+w+"&color=1&dark=false&iframe=true&domain=com&lang=en-US&newtab=false&ot_source=Restaurant%20website";
      sc.async=true;
      var holder=d.createElement("div"); holder.className="ot-widget"; holder.appendChild(sc);
      ot.appendChild(holder);
      setTimeout(function(){ if(ot.querySelector("iframe")){ var b=ot.querySelector(".btn"); if(b) b.remove(); } },4000);
    };
    if("IntersectionObserver" in window){var io2=new IntersectionObserver(function(es){if(es[0].isIntersecting){load();io2.disconnect()}},{rootMargin:"600px"});io2.observe(ot)} else load();
  }

  // menu filters + search
  var chips=d.querySelectorAll(".chip"), q=d.querySelector(".search"), secs=d.querySelectorAll(".msec"), empty=d.querySelector(".empty"), tools=d.querySelector(".mtools"), list=d.querySelector("#menu-list");
  if(chips.length && list){
    var cur="all";
    d.querySelectorAll(".item h3 .nm, .item p").forEach(function(el){el.dataset.raw=el.textContent});
    function toResults(){
      var top=list.getBoundingClientRect().top+window.scrollY-(hdr?hdr.offsetHeight:0)-(tools?tools.offsetHeight:0)-8;
      if(window.scrollY>top+4){ window.scrollTo(0,top); requestAnimationFrame(function(){ if(Math.abs(window.scrollY-top)>4) window.scrollTo(0,top); }); }
    }
    function esc(s){return s.replace(/[&<>]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[c]})}
    function apply(scroll){
      var term=(q&&q.value||"").trim().toLowerCase(), shown=0;
      secs.forEach(function(sec){
        var okSec=cur==="all"||sec.dataset.cat===cur, any=0;
        sec.querySelectorAll(".item").forEach(function(it){
          var txt=it.textContent.toLowerCase(), ok=okSec&&(!term||txt.indexOf(term)>-1);
          it.hidden=!ok; if(ok){any++;shown++}
          it.querySelectorAll("[data-raw]").forEach(function(el){
            var raw=el.dataset.raw;
            if(term&&ok){var i=raw.toLowerCase().indexOf(term); el.innerHTML=i>-1?esc(raw.slice(0,i))+"<mark>"+esc(raw.slice(i,i+term.length))+"</mark>"+esc(raw.slice(i+term.length)):esc(raw)}
            else el.textContent=raw;
          });
        });
        sec.hidden=!any;
      });
      if(empty) empty.hidden=shown>0;
      if(scroll) toResults();
    }
    chips.forEach(function(c){c.addEventListener("click",function(){cur=c.dataset.cat;chips.forEach(function(x){x.setAttribute("aria-pressed",x===c)});apply(true)})});
    if(q){q.addEventListener("input",function(){apply(true)})}
  }

  // re-land on #anchors after fonts load
  if(location.hash && d.fonts && d.fonts.ready){d.fonts.ready.then(function(){var t=d.getElementById(location.hash.slice(1));if(t)t.scrollIntoView()})}

  var yr=d.querySelector("[data-year]"); if(yr) yr.textContent=new Date().getFullYear();
})();
