from pathlib import Path
import sys
sys.path.insert(0,'C:/Users/Sarva/.codex/tmp/noorheroes-avatar-validation')
from collections import Counter
from PIL import Image
import json, hashlib, zipfile
import jsonschema

base=Path(__file__).resolve().parent
plan=json.loads((base/'generation-plan.json').read_text())
sources={a['id']:a for a in json.loads((base/'source-assets.json').read_text())}
nodes=json.loads((base/'figma-nodes.json').read_text())
frames={f['groupKey']:f for f in nodes['frames']}
audits={a['id']:a for g in plan['groups'] for a in json.loads((base/'evidence'/('audit-'+g['key']+'.json')).read_text())['files']}
avatars=[]
for p in plan['avatars']:
 s=sources[p['id']]; a=audits[p['id']]; f=frames[p['groupKey']]
 relative='assets/'+p['groupKey']+'/'+p['filename']
 path=base/relative
 image=Image.open(path); image.load()
 assert image.size==(1264,1264) and image.format=='PNG'
 alpha=image.convert('RGBA').getchannel('A').getextrema()
 assert alpha==(255,255),(path.name,alpha)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256']
 assert a['bytes']<=10485760
 node=f['imageNodeIds'][p['index']-1]
 url='https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id='+node.replace(':','-')
 canva='https://www.canva.com/M/'+s['canvaMediaId']+'?utm_source=OC-AaBlKrqBJJNF&utm_campaign=agent_connector_create_image_asset_opened'
 clothing=p['description'].split('Clothing: ',1)[1].split('. Pose:',1)[0]
 avatar={
  'id':p['id'],'ageGroup':p['groupKey'],'portrayedAge':p['portrayedAge'],'presentation':p['gender'],
  'displayLabel':p['groupLabel']+' / Avatar '+str(p['index']).zfill(2),
  'altText':'Soft 3D illustrated '+p['gender']+' character, intended age '+str(p['portrayedAge'])+', wearing '+clothing+'.',
  'style':'soft-3d-storybook',
  'source':{'provider':'Canva','mediaId':s['canvaMediaId'],'url':canva},
  'file':{'path':relative,'storageKey':'avatars/v2/age-wise/'+p['groupKey']+'/'+p['filename'],'mimeType':'image/png','width':1264,'height':1264,'bytes':a['bytes'],'sha256':a['sha256'],'background':'opaque warm ivory'},
  'figma':{'fileKey':'MR9935oQZACMjndzGIUgq5','frameId':f['id'],'nodeId':node,'url':url,'previewWidth':120,'previewHeight':120},
  'review':{'status':'agent-reviewed','ageAppearanceChecked':True,'cropChecked':True,'anatomyChecked':True,'duplicateChecked':True,'userApproval':'pending'}
 }
 avatars.append(avatar)
assert len(avatars)==80
assert Counter(a['ageGroup'] for a in avatars)=={'5_8':20,'8_10':20,'10_14':20,'14_18_plus':20}
for values in [[a['id'] for a in avatars],[a['source']['mediaId'] for a in avatars],[a['file']['sha256'] for a in avatars],[a['file']['storageKey'] for a in avatars]]:
 assert len(set(values))==80
old_audit=base.parent/'NoorHeroes_Avatar_Library/evidence/asset-audit.json'
if old_audit.exists():
 old_hashes={a['sha256'] for a in json.loads(old_audit.read_text())['files']}
 assert not old_hashes.intersection(a['file']['sha256'] for a in avatars)
metadata={'schemaVersion':'1.0.0','collectionId':'noorheroes-v2-age-wise','avatars':avatars}
jsonschema.Draft202012Validator(json.loads((base/'avatar-metadata.schema.json').read_text())).validate(metadata)
(base/'avatar-metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
lines=['# Avatar asset index','','All 80 original PNGs are 1264 × 1264. Each Figma image remains separately selectable.','','| Group | File | Intended portrayed age | Canva original | Figma image |','|---|---|---:|---|---|']
for a in avatars:
 lines.append('| '+a['ageGroup']+' | '+a['file']['path'].split('/')[-1]+' | '+str(a['portrayedAge'])+' | [Open generated image]('+a['source']['url']+') | ['+a['displayLabel']+']('+a['figma']['url']+') |')
(base/'ASSET-INDEX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
report={'count':80,'countsByGroup':dict(Counter(a['ageGroup'] for a in avatars)),'uniqueIds':80,'uniqueMediaIds':80,'uniqueFileHashes':80,'exactDuplicatesOfPrevious20':0,'allDimensions':[1264,1264],'allPng':True,'allOpaque':True,'metadataSchemaValidation':'passed','totalImageBytes':sum(a['file']['bytes'] for a in avatars)}
(base/'evidence/final-asset-audit.json').write_text(json.dumps(report,indent=2))
archive=base/'NoorHeroes-Age-Wise-Avatar-Library.zip'
files=sorted((base/'assets').rglob('*.png'))+[base/n for n in ['README.md','ASSET-INDEX.md','EXPORT-AND-STORAGE.md','avatar-metadata.json','avatar-metadata.schema.json','figma-nodes.json','generation-plan.json']]
files+=sorted(p for p in (base/'evidence').iterdir() if p.suffix in ['.png','.json'])
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(base).as_posix())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.startswith('assets/') and n.endswith('.png')])==80
 for a in avatars:assert hashlib.sha256(z.read(a['file']['path'])).hexdigest()==a['file']['sha256']
report.update(archiveBytes=archive.stat().st_size,archiveSha256=hashlib.sha256(archive.read_bytes()).hexdigest(),archiveIntegrity='passed')
(base/'evidence/package-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
