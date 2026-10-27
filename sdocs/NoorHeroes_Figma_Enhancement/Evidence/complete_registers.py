from pathlib import Path
import re,json,hashlib,urllib.parse,collections
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'sdocs/NoorHeroes_Figma_Enhancement'
def read(p):return json.loads((OUT/p).read_text(encoding='utf-8'))
def write(p,t):(OUT/p).write_text(t.rstrip()+'\n',encoding='utf-8')
def plink(r):return '['+f"{r['number']:03d} {r['name']}"+']('+r['file']+')'
def words(s):return set(re.findall(r'[a-z]{4,}',s.lower()))-{'screen','must','child','parent','shall','user','from','with','that','have','this','when','only','then','never','same','after'}
rs=read('Evidence/normalized-screen-records.json');manifest=read('Evidence/source-manifest.json');obs=read('Evidence/current-site-screens.json')['screens'];seasonal=read('Evidence/current-site-ramadan.json')
frs=[];chapters=[]
for p in sorted((ROOT/'PRD_Documents').rglob('Feature_*.md')):
    m=re.match(r'Feature_([ABCF]\d+)_',p.name)
    if not m:continue
    feature=m.group(1);t=p.read_text(encoding='utf-8');sec=re.search(r'^### 1\.7\b.*?(?=^### 1\.8\b|\Z)',t,re.M|re.S)
    if not sec:continue
    lines=re.split(r'(?=^\*\*FR-\d+\*\*)',sec.group(0),flags=re.M)
    candidates=[r for r in rs if r['feature']==feature]
    alias=[a for a in read('Evidence/shared-surface-aliases.json') if a['feature']==feature]
    for a in alias:
        if a['owner_number']:candidates += [r for r in rs if r['number']==a['owner_number']]
    if feature in ['F35','F37']:
        candidates=[r for r in rs if r['feature'] in (['A2','A5','B13','C22','C26'] if feature=='F35' else ['A1','C19','C23','C26'])]
    for line in lines:
        f=re.match(r'\*\*FR-(\d+)\*\*',line)
        if not f:continue
        req=line.strip();fw=words(req)
        ranked=sorted(candidates,key=lambda r:len(fw&words(r['name']+' '+str(r['fields'])+' '+str(r['actions']))),reverse=True)
        top=ranked[:3] if ranked else []
        data={'id':feature+'-FR-'+f.group(1),'feature':feature,'source':str(p.relative_to(ROOT)).replace('\\','/'),'section':'§1.7','text':req,'candidate_prompt_numbers':[r['number'] for r in top],'mapping_status':'Derived owning-screen candidates; full requirement retained; verify screen-specific acceptance before execution','cross_cutting':feature in ['F35','F37']}
        frs.append(data)
    chapters.append((feature,p,req if False else ''))
out=['# Every-functional-requirement coverage register','','Every FR in the mobile feature PRDs and mobile-impact F35/F37 architecture PRDs is retained verbatim below. No admin/web screen is generated. Exact source content is authority; derived candidate owners are transparent routing aids,not evidence that a prototype already implements the requirement. Nonvisual backend/privacy/security requirements remain production acceptance obligations and do not become invented app screens.','', 'Screen-specific prompt bodies retain mapped requirements and source state/edge excerpts. [Screen-reference matrix](03_REQUIREMENT_TRACEABILITY_MATRIX.md) provides existing-screen/Frame1/Frame2 provenance; [shared aliases](02_SCREEN_INVENTORY_AND_ORDER.md#shared-surfaces-and-contextual-aliases) retain contextual reuse.','']
last=None
for f in frs:
    if last!=f['feature']:
        out+=['## '+f['feature'],'', '['+Path(f['source']).name+'](<'+str(ROOT/f['source']).replace('\\','/')+'>) — §1.7.',''];last=f['feature']
    out+=['### '+f['id'],'',f['text'],'','Candidate owning surfaces: '+('; '.join(plink(r) for r in rs if r['number'] in f['candidate_prompt_numbers']) or '**No standalone mobile screen; cross-cutting constraint — verify affected existing journeys.**')+'.','', 'Coverage class: '+('Cross-cutting production architecture/security obligation; apply to cited existing UI without claiming prototype enforcement.' if f['cross_cutting'] else 'Requirement retained; screen/overlay/state or production constraint. Source-specific realization and exact copy remain subject to screen acceptance and open decisions.'),'']
write('10_REQUIREMENT_COVERAGE_REGISTER.md','\n'.join(out));write('Evidence/functional-requirements.json',json.dumps(frs,ensure_ascii=False,indent=2))
# Every observed control is accounted for; unresolved elements are deliberately blocked.
controls=[]
allobs=obs+seasonal
def owner(s):
    hits=[r for r in rs if r.get('site_name')==s['name'] or (r.get('current_site') or {}).get('screen_name')==s['name']]
    if hits:return hits[0]
    base=re.split(r' [—–�] ',s['name'])[0]
    basehits=[r for r in rs if r.get('site_name')==base]
    if basehits:return basehits[0]
    aliases={'Who is Learning?':'Profile Picker','Audio Player':'Story Player — Audio','Bedtime Player':'Audio Bedtime Player','Bedtime Dua':'Dua / Calm-Reflection','Calm Rest Screen':'Calm Locked State','Content Age Level':'Content Age Level Settings','Dua Quiz':'Recall Quiz Question','Explanation':'Per-Answer Explanation','Fact of the Day':'Islamic Fact Detail','Game Complete':'Session Completion','Habit Checklist':"Habit Builder — Today",'Moral Card':'Moral Summary','Notif. Preferences':'Notification Preferences','Premium Upsell':'Free-Plan Second-Child','Quiz Complete':'Quiz Completion / Effort','Quiz Result':'Quiz Completion Result','Results':'Quiz Completion Result','Complete':'Completion / Reward','Surah Practice':'Surah Learning'}
    aliases.update({"Du'as":'Dua Learning Landing','Learn':'Learn Tab Landing','Rewards':'Rewards Hub'})
    prefix=aliases.get(s['name'],aliases.get(base))
    return next((r for r in rs if prefix and r['name'].startswith(prefix)),None)
def behavior(s,e,r):
    label=(e.get('label') or e.get('text') or e.get('placeholder') or '').strip();low=label.lower();tag=e.get('tag')
    if e.get('disabled'):return 'Unavailable in captured state; no activation. Show source/PRD reason and corresponding enabled-state behavior.','State-specific availability'
    if tag in ['INPUT','TEXTAREA']:return 'Edit only this field; validate source-specific format; preserve draft; submit via owning form action.','Input behavior specified'
    if tag=='SELECT':return 'Choose approved option; update owning local state; do not imply saved server state until confirmed.','Selection behavior specified'
    if low in ['default','loading','offline','empty','empty state','error'] or 'preview gate' in low:return 'Design-review/demo control; classify under G-08; do not wire into product navigation.','Audit-only control'
    if 'go back' in low or low in ['←','back']:return 'Back to invoking route/overlay caller, preserving eligible draft/filter/child context.','Navigation rule'
    if low in ['close','cancel','not now'] or low.startswith('cancel '):return 'Cancel current operation/close current overlay; restore caller focus. A billing cancellation command uses the disclosed cancellation flow,not a generic dismiss.','Cancel rule; contextual confirmation'
    if low=='skip':return 'Intro Skip → Login/auth entry; other optional-step Skip returns owning approved continuation. Never skip login/required consent.','Navigation rule'
    if 'resend' in low:return 'Request OTP only when server-authoritative cooldown permits; show new pending/cooldown or failure fallback.','OTP rule'
    if 'wrong number' in low or 'edit number' in low:return 'Return identifier edit to invoking Login/Registration, preserving nonsensitive draft/consent context.','OTP rule'
    if low=='continue with google':return 'Simulate verified Google identity; new-family consent/onboarding or returning picker; real OAuth not connected.','Auth rule'
    if low in ['log in','login','sign in']:return 'Login → OTP or Google; returning-user route by authoritative verified state.','Auth rule'
    if 'search' in low and ('voice' in low or 'microphone' in low):return 'Require parent voice grant+OS microphone permission; listening/processing/clarification,then query results; cancel/deny falls back to text.','Voice rule'
    if 'heart' in low or 'favorite' in low or 'favourite' in low:return 'Toggle eligible content favorite in place; selected label/icon; sync/rollback/withdrawal per B14. Opening Favorites uses its dedicated list route.','Favorites contextual rule'
    if 'retry' in low or 'try again' in low:
        return ('Retry current quiz/practice using approved retry set or saved context; outside quiz retry the failed operation without duplicate record/reward.','Retry contextual rule')
    if 'review mistakes' in low:return 'Open shared Review Mistakes for current attempt only when mistakes exist; back returns result.','Result rule'
    if low in ['home','learn','stories','rewards','profile']:return 'Navigate to authenticated child '+label+' tab; preserve scoped child; parent-only destinations remain gated.','Child shell navigation'
    if 'settings' in low or 'controls' in low:return 'Open named settings/controls destination after parent verification when parent-only; retain caller and selected child.','Module destination; exact child/category confirm'
    if 'night ' in low and ('lantern' in low):return 'Eligible completed night→recap; tonight→mission; future night unavailable; preserve night ID and region campaign context.','Seasonal eligibility'
    if 'parent' in low and ('dashboard' in low or low=='parent'):return 'Fresh Child→Parent gate,then Dashboard or exact pending parent route; cancel returns child caller.','Parent gate rule'
    if 'read' in low and ('→' in label or low.startswith('read')):return 'Open exact versioned linked legal text; close returns form without changing grant.','Legal link; document identity must be confirmed'
    if 'download' in low and r and r['feature'] in ['B15','A3','A5','A6']:return 'Download action opens owning content download/status; cap/storage/expiry/Wi-Fi conditions checked. Clear-all requires dedicated confirmation.','Downloads contextual rule'
    # Match an explicit action authored in research rather than inventing a convenient destination.
    acts=(r or {}).get('actions',[])
    if isinstance(acts,list):
        for a in acts:
            if isinstance(a,dict):
                aname=str(a.get('element','')).lower()
                if aname and (aname in low or low in aname) and len(low)>2:
                    return str(a.get('behavior',a.get('destination',a.get('result',a)))),'Screen-specific authored action; verify source'
    return ('UNRESOLVED label-to-action binding. Owning-screen action contract: '+str([(a.get('element'),a.get('destination',a.get('behavior'))) if isinstance(a,dict) else a for a in (acts if isinstance(acts,list) else [acts])])[:700]+'. Select the exact matching action and confirm preconditions/destination before wiring; source click outcome unverified.') if r else 'UNRESOLVED owning surface and exact destination; block wiring until source is identified.','Open control mapping' 
for s in allobs:
    r=owner(s)
    for i,e in enumerate(s.get('elements',[]),1):
        b,status=behavior(s,e,r);controls.append({'screen':s['name'],'element_index':i,'element':e,'owner_number':r['number'] if r else None,'behavior':b,'status':status})
out=['# Current-preview control reconciliation','','Every captured button,input,select,link and textarea is retained below. Text extraction confirms presence,not the actual click destination. Standard/source-derived behaviors are specified; unmatched destinations are explicitly open and block wiring. No control is connected to a convenient unrelated screen. Religious/demo/sample controls require the source decision.','', 'This ledger does not contain an audit of undetected Figma click targets because no reactions were found in the inspected reference descendants. Original text layer names do not automatically identify interactive controls.','']
last=None
for c in controls:
    if last!=c['screen']:
        out+=['## '+c['screen'],'','| Element | Owner | Expected behavior / destination | Status |','|---|---|---|---|'];last=c['screen']
    e=c['element'];label=e.get('label') or e.get('text') or e.get('placeholder') or '(unlabeled control)';r=next((r for r in rs if r['number']==c['owner_number']),None)
    clean=lambda s:str(s).replace('|',' / ').replace('\n',' ')
    out.append('| '+clean(e['tag']+' '+label)+' | '+(plink(r) if r else '**Owner unresolved**')+' | '+clean(c['behavior'])+' | '+c['status']+' |')
write('11_CURRENT_CONTROL_RECONCILIATION.md','\n'.join(out));write('Evidence/control-ledger.json',json.dumps(controls,ensure_ascii=False,indent=2))
print({'functional_requirements':len(frs),'observed_controls':len(controls),'open_control_mappings':sum(c['status']=='Open control mapping' for c in controls),'unmapped_owner':sum(c['owner_number'] is None for c in controls)})
