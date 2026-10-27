from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil, sys

base=Path(__file__).resolve().parent
source=json.loads((base/'source-assets.json').read_text())
group=sys.argv[1]
items=sorted([a for a in source if a['groupKey']==group],key=lambda a:a['index'])
assert len(items)==20,(group,len(items))
target=base/'assets'/group; target.mkdir(parents=True,exist_ok=True)
sheet=Image.new('RGB',(1280,1200),'#FEFBF4'); draw=ImageDraw.Draw(sheet)
audit=[]
for i,a in enumerate(items):
 p=Path('C:/Users/Sarva/Downloads')/a['downloadFilename']
 im=Image.open(p); im.load()
 assert im.size==(1264,1264),(a['id'],im.size)
 assert im.format=='PNG',(a['id'],im.format)
 dest=target/a['filename']; shutil.copyfile(p,dest)
 assert dest.read_bytes()==p.read_bytes()
 digest=hashlib.sha256(dest.read_bytes()).hexdigest()
 audit.append({'id':a['id'],'filename':a['filename'],'groupKey':group,'width':im.width,'height':im.height,'mimeType':'image/png','bytes':dest.stat().st_size,'sha256':digest})
 thumb=im.convert('RGB'); thumb.thumbnail((224,224))
 x=i%5*256+16; y=i//5*300+12
 sheet.paste(thumb,(x,y)); draw.text((x,y+236),group+' / '+str(i+1).zfill(2),fill='#074D4D')
assert len({a['sha256'] for a in audit})==20
sheet.save(base/'evidence'/('contact-'+group+'.png'))
(base/'evidence'/('audit-'+group+'.json')).write_text(json.dumps({'count':20,'uniqueHashes':20,'sourceBytesPreserved':True,'files':audit},indent=2))
print(json.dumps({'group':group,'count':20,'dimensions':[1264,1264],'uniqueFiles':20,'totalBytes':sum(a['bytes'] for a in audit)}))
