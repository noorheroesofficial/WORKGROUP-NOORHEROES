from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, shutil

base=Path(__file__).resolve().parent
assets=base/'assets'; assets.mkdir(exist_ok=True)
manifest=json.loads((base/'manifest.json').read_text())
checks=[]
sheet=Image.new('RGB',(1280,1200),'#FEFBF4')
draw=ImageDraw.Draw(sheet)
for index,m in enumerate(manifest):
 source=Path('C:/Users/Sarva/Downloads')/m['downloadFilename']
 image=Image.open(source); image.load()
 assert image.size==(1264,1264),(source,image.size)
 assert image.format=='PNG',(source,image.format)
 destination=assets/m['filename']
 shutil.copyfile(source,destination)
 assert destination.read_bytes()==source.read_bytes()
 digest=hashlib.sha256(destination.read_bytes()).hexdigest()
 checks.append({'filename':m['filename'],'width':image.width,'height':image.height,'format':image.format,'sha256':digest,'bytes':destination.stat().st_size})
 x=(index%5)*256+16; y=(index//5)*300+12
 thumb=image.convert('RGB'); thumb.thumbnail((224,224))
 sheet.paste(thumb,(x,y)); draw.text((x,y+236),'Avatar '+str(index+1).zfill(2),fill='#074D4D')
assert len({c['sha256'] for c in checks})==20
sheet.save(base/'evidence/contact-sheet.png')
report={'image_count':len(checks),'unique_file_hashes':20,'all_dimensions':[1264,1264],'all_formats':'PNG','source_bytes_preserved':True,'files':checks}
(base/'evidence/asset-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
