from pathlib import Path
from PIL import Image, ImageChops
import json, zipfile, hashlib, io
base=Path('sdocs/NoorHeroes_Brand_Assets')
results=json.loads((base/'export-results.json').read_text())
manifest=json.loads((base/'manifest.json').read_text())['manifest']
source_by_id={m['id']:m for m in manifest}
native={
'1301:426':'NH/Social/Announcement.png',
'1301:448':'NH/Social/Education.png',
'1301:470':'NH/Social/Launch.png',
'1301:492':'NH/Social/Profile/teal.png',
'1301:512':'NH/Cover/Content=Editable, Platform=YouTube.png',
'1301:524':'NH/Cover/Content=Clean, Platform=YouTube.png',
'1301:536':'NH/Cover/Content=Editable, Platform=Facebook.png',
'1301:548':'NH/Cover/Content=Clean, Platform=Facebook.png',
'1301:560':'NH/Cover/Content=Editable, Platform=LinkedIn Company.png',
'1301:572':'NH/Cover/Content=Clean, Platform=LinkedIn Company.png',
'1301:584':'NH/Cover/Content=Editable, Platform=X.png',
'1301:596':'NH/Cover/Content=Clean, Platform=X.png',
'1301:620':'NH/Cover/Content=Clean, Platform=Website Hero.png'}
with zipfile.ZipFile('C:/Users/Sarva/Downloads/NoorHeroes APP.zip') as z:
 for item in results:
  if 'error' not in item: continue
  member=native[item['id']]
  data=z.read(member)
  (base/'exports'/item['filename']).write_bytes(data)
  m=source_by_id[item['id']]
  item.update(w=m['w'],h=m['h'],bg=m['bg'],status='downloaded-native-figma-ui')
  del item['error']
with zipfile.ZipFile('C:/Users/Sarva/Downloads/NoorHeroes APP (1).zip') as z:
 for item in results:
  if item['id'] not in ['1300:116','1300:120']: continue
  kind='Foreground' if item['id']=='1300:116' else 'Monochrome'
  density=item['filename'].removesuffix('.png').split('-')[-1]
  member=f'NH/AppIcon/Android/{kind}-{density}.png'
  (base/'exports'/item['filename']).write_bytes(z.read(member))
  item['status']='downloaded-native-figma-ui-alpha-verified'
audit=[]
for item in results:
 p=base/'exports'/item['filename']
 im=Image.open(p); im.load()
 assert im.size==(item['w'],item['h']),(p.name,im.size)
 alpha=im.getchannel('A').getextrema() if 'A' in im.getbands() else (255,255)
 if item['bg'] in ['ivory','teal','original background']:
  # Rounded social/app banner backgrounds can have transparent corner pixels.
  if 'appicon-ios' in p.name and 'foreground' not in p.name: assert alpha==(255,255)
 if item['bg']=='transparent': assert alpha[0]==0,(p.name,alpha)
 audit.append(dict(filename=p.name,width=im.width,height=im.height,mode=im.mode,alpha=list(alpha),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
# Lossless export encoding: omit an entirely opaque alpha channel for iOS submission PNGs.
# This changes the PNG channel layout, never the artwork's RGB pixels.
ios_encoded=[]
for a in audit:
 if 'appicon-ios' in a['filename'] and 'foreground' not in a['filename']:
  p=base/'exports'/a['filename']; im=Image.open(p); before=im.convert('RGB').tobytes()
  rgb=im.convert('RGB'); rgb.save(p,format='PNG')
  assert Image.open(p).tobytes()==before
  a.update(mode='RGB',bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
  ios_encoded.append(p.name)
# Read-only alpha and visible-color comparison against supplied original crops.
checks=[]
for filename,source,bbox in [
 ('noorheroes-brand-logo-full.png','C:/Users/Sarva/Downloads/agent-photo-edit-ea275e1b-3e72-4bce-9868-e1d698d03f63.png',(148,136,1677,661)),
 ('noorheroes-brand-wordmark-primary.png','C:/Users/Sarva/Downloads/agent-photo-edit-aaf63375-f52f-41ef-b86e-22b4c7581133.png',(91,312,1683,622)),
 ('noorheroes-brand-monogram-primary.png','C:/Users/Sarva/Downloads/agent-photo-edit-1937acec-4ea1-44a3-97be-d898c4aef740.png',(217,135,1036,1044))]:
 actual=Image.open(base/'exports'/filename).convert('RGBA')
 original=Image.open(source).crop(bbox).convert('RGBA')
 alpha_diff=ImageChops.difference(actual.getchannel('A'),original.getchannel('A')).getextrema()
 # Ignore RGB hidden beneath alpha=0 when comparing visible content.
 diffs=[]
 for a,b in zip(actual.getdata(),original.getdata()):
  if a[3] and b[3]: diffs.append(max(abs(a[k]-b[k]) for k in range(3)))
 checks.append(dict(file=filename,alpha_max_error=alpha_diff[1],visible_rgb_max_error=max(diffs),visible_rgb_mean_error=sum(diffs)/len(diffs)))
report=dict(png_count=len(audit),dimension_mismatches=0,source_crop_comparisons=checks,ios_rgb_encodings=ios_encoded,files=audit)
(base/'evidence'/'final-png-audit.json').write_text(json.dumps(report,indent=2))
(base/'export-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))

