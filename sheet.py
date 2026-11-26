import sys,glob
from PIL import Image,ImageDraw
files=sorted(glob.glob(sys.argv[1]))
out=sys.argv[2]; per=int(sys.argv[3]) if len(sys.argv)>3 else 20
for k in range(0,len(files),per):
    chunk=files[k:k+per]; W=5; T=300
    sheet=Image.new('RGB',(W*T,((len(chunk)+W-1)//W)*(T+24)),'white'); d=ImageDraw.Draw(sheet)
    for i,f in enumerate(chunk):
        try: im=Image.open(f).convert('RGB')
        except: continue
        im.thumbnail((T,T)); x=(i%W)*T; y=(i//W)*(T+24)
        sheet.paste(im,(x,y)); d.text((x+4,y+T+4),f.split('/')[-1][:40],fill='black')
    sheet.save(f'{out}_{k//per}.jpg',quality=80)
    print(f'{out}_{k//per}.jpg')
