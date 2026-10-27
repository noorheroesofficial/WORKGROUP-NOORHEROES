from pathlib import Path
import json, zipfile, hashlib

base=Path(__file__).resolve().parent
results=json.loads((base/'export-results.json').read_text())
audit=json.loads((base/'evidence/final-png-audit.json').read_text())
masters={m['id']:m for m in json.loads((base/'manifest.json').read_text())['manifest']}
assert len(results)==88 and len(audit['files'])==88
rows=['# PNG export index','', '88 files. Dimensions and transparency were checked against the manifest. Scale is relative to the source component.','', '| Filename | Use | Pixels | Background | Scale | Figma source |','|---|---|---:|---|---:|---|']
for r in sorted(results,key=lambda r:r['filename']):
 p=base/'exports'/r['filename']
 a=next(a for a in audit['files'] if a['filename']==r['filename'])
 assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']
 m=masters[r['id']]
 use='Android icon' if 'android' in p.name else 'iOS icon' if 'ios' in p.name else 'Store icon' if 'googleplay' in p.name else 'Social template' if 'social' in p.name else 'Platform cover' if 'cover' in p.name else 'App banner' if 'banner' in p.name else 'Brand identity'
 link='https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id='+r['id'].replace(':','-')
 rows.append(f"| {p.name} | {use} | {r['w']} × {r['h']} | {r['bg']} | {r['w']/m['w']:g}x | [{r['id']}]({link}) |")
(base/'EXPORTS.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
zip_path=base/'NoorHeroes-Brand-App-Assets.zip'
files=[base/'README.md',base/'EXPORTS.md',base/'manifest.json',base/'export-results.json',base/'evidence/final-png-audit.json']
files+=sorted((base/'exports').glob('*.png'))
files+=sorted((base/'evidence').glob('*.png'))
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files: z.write(p,p.relative_to(base).as_posix())
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.startswith('exports/') and n.endswith('.png')])==88
 for r in results:
  assert z.read('exports/'+r['filename'])==(base/'exports'/r['filename']).read_bytes()
print(json.dumps({'zip':str(zip_path),'pngs':88,'archive_entries':len(files),'bytes':zip_path.stat().st_size,'sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'archive_integrity':'passed'},indent=2))
