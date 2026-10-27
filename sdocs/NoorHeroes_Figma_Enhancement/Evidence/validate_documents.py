from pathlib import Path
import json,re,hashlib
out=Path(__file__).resolve().parents[1];root=out.parents[1]
rs=json.loads((out/'Evidence/normalized-screen-records.json').read_text(encoding='utf-8'));manifest=json.loads((out/'Evidence/source-manifest.json').read_text(encoding='utf-8'))
errors=[];links=0
for r in rs:
 t=(out/r['file']).read_text(encoding='utf-8')
 if re.findall(r'^## (\d+)\.',t,re.M)!=[str(i) for i in range(1,12)]:errors.append([r['file'],'section structure'])
for p in out.rglob('*.md'):
 for a,b in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))\)',p.read_text(encoding='utf-8')):
  target=(a or b).split('#')[0].replace('%20',' ')
  if not target or re.match(r'^(https?:|app:|codex:)',target):continue
  dest=Path(target) if re.match(r'^[A-Za-z]:',target) else p.parent/target
  links+=1
  if not dest.exists():errors.append([str(p.relative_to(out)),'missing link',target])
changed=[m['path'] for m in manifest if hashlib.sha256((root/m['path']).read_bytes()).hexdigest()!=m['sha256']]
report={'prompts':len(rs),'prompt_files':len(list((out/'Screen_Prompts').glob('*.md'))),'numbering_contiguous':[r['number'] for r in rs]==list(range(1,len(rs)+1)),'local_links_checked':links,'errors':errors,'prd_hash_changes_since_manifest':changed,'aliases_without_owner':[a for a in json.loads((out/'Evidence/shared-surface-aliases.json').read_text(encoding='utf-8')) if not a['owner_file']]}
(out/'Evidence/document-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
