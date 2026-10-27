from pathlib import Path
import re, json

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
PRD=ROOT/'PRD_Documents'/'Child App (1-12)'
FEATURE_DIRS={2:'Home',3:'Stories',4:'Bedtime Audio',5:'Learn',6:"Du'as",7:'Habits',8:'Quiz Engine',9:'Quiz Engine',10:'Games',11:'Rewards',12:'Avatar'}
INSPECTED=['Home/Home-01.png','Learn/Skill Tree-01.png','Stories/Story Detail-01.png','Bedtime Audio/Audio Player.png',"Du'as/Dua Card-01.png",'Habits/Habit Checklist-01.png','Quiz Engine/Quiz Question-01.png','Games/Games Hub-01.png','Rewards/Rewards Wallet-01.png','Avatar/Avatar-01.png']

def section(t,n):
    m=re.search(r'(?m)^#{2,3} '+re.escape(n)+r'\.?\s[^\n]*',t)
    if not m:return ''
    level=len(m.group(0).split(' ')[0])
    nxt=re.search(r'(?m)^#{2,'+str(level)+r'} ',t[m.end():])
    return t[m.start():m.end()+nxt.start() if nxt else len(t)].strip()

def numbered_sections(t):
    return {m.group(1):section(t,m.group(1)) for m in re.finditer(r'(?m)^#{2,3} (\d+(?:\.\d+)?)\.?\s',t)}

CONFLICTS=[
 {'id':'CL-10','affected':'Story offline sequential unlock','sources':['A3 §1.10 edge 1','Development_Blueprints/A3_Stories_Module/KMP/02-story-detail-episode-unlock-presentation.md'],'finding':'PRD permits immediate local next-episode unlock after offline completion; blueprint forbids client-side unlock computation and relies only on cached server state.','recommendation':'Approve a signed/package-provided unlock policy or clarify which behavior applies; do not silently suppress offline progression or invent entitlement logic.'},
 {'id':'CL-11','affected':'Arabic Letters exercise inventory','sources':['A5 §1.7 FR-6','A5 §1.18 rows 8–11'],'finding':'FR requires contextual form matching and harakah sound pairing absent from the four-screen inventory.','recommendation':'Add two independently reviewable exercise prompts or obtain explicit mapping to existing mode variants; flag absent screenshots.'},
 {'id':'CL-12','affected':'Bedtime ending after window boundary','sources':['A3 §1.10 edge 6','Development_Blueprints/A3_Stories_Module/KMP/05-bedtime-mode-player-experience.md'],'finding':'PRD holds visual/narration mode at story start but re-evaluates ending at completion; blueprint launch-time boolean risks holding both.','recommendation':'Approve distinct launch-theme and completion-ending context so entering bedtime mid-story yields calm reflection without theme flicker.'},
 {'id':'CL-01','affected':'Rewards Wallet / Daily Missions','sources':['A2 §1.7 FR-4','A11 §1.7 FR-10','Screens/Mobile App/Rewards/Rewards Wallet-01.png'],'finding':'Verified screenshot says 3 of 4 done; PRD daily missions are three/day.','recommendation':'Preserve source screenshot; obtain approval for requirement-driven enhanced variant with three daily missions and validated sample data. Do not silently change copy.'},
 {'id':'CL-02','affected':'Quiz Completion Result','sources':['A9 §2.1','A9 §2.2 image-generation prompt','Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/02-quiz-completion-result-screen.md'],'finding':'UX and blueprint demand equal-weight actions; image prompt assigns filled gold primary to Continue.','recommendation':'Seek approval for equal visual weight per normative UX/blueprint; preserve exact action labels.'},
 {'id':'CL-03','affected':'Home / Games entry','sources':['A2 §1.7 FR-1','A10 §2.3'],'finding':'A10 names Home Trending Games rail, absent from A2 fixed ten-section priority.','recommendation':'Do not add an eleventh Home section; approve mapping Games entries within existing recommendation section or clarify requirements.'},
 {'id':'CL-04','affected':'Rewards rules / Quiz completion','sources':['A8 §1.7 FR-5','A9 §1.7 FR-6','A11 §1.7 FR-7'],'finding':'A8 participation reward is accuracy-independent; A11 representative table specifies pass-quiz 100% and >=80% rewards.','recommendation':'Clarify whether A11 amounts are supplemental accuracy bonuses; no prototype may withhold base effort reward.'},
 {'id':'CL-05','affected':'Shared favorites, downloads, subscription, avatar references','sources':['A3 §1.18','A6 §1.7 FR-12','A7 §1.18'],'finding':'Legacy A.14 subscription, A.16 downloads, A.13 search and A.9 avatar references conflict with current C24, B15, B13, A12 IDs.','recommendation':'Use current feature-name destination mapping; record original references and corrected targets explicitly.'},
 {'id':'CL-06','affected':'Home first-day CTA','sources':['A2 §1.7 FR-15','A2 §7 Android prompt'],'finding':'FR uses Let’s start your first mission framing while implementation prompt names Start My First Mission.','recommendation':'Obtain exact approved CTA from original frame or content registry; neither phrase silently replaces existing source copy.'},
 {'id':'CL-07','affected':'Game Hub','sources':['Screens/Mobile App/Games/Games Hub-01.png'],'finding':'Default, Loading, Offline selectors are visible in reference screenshot; intended production controls versus preview fixture switches is unverified.','recommendation':'Document as reference state demonstration until original interaction inspection confirms purpose.'},
 {'id':'CL-08','affected':'Dua badge dismissal','sources':['A6 §1.18 row 11','Development_Blueprints/A6_Dua_Learning/KMP/04-dua-master-badge-progress-celebration.md'],'finding':'PRD inventory dismiss destination Achievements; KMP blueprint returns to Dua Card/Catalog caller.','recommendation':'Approval needed for dismissal versus optional View Achievements action; do not silently select destination.'},
 {'id':'CL-09','affected':'Sharing gate order','sources':['A3 §1.18 rows 20-21','A11 §1.18 rows 8-9','A11 §1.7 FR-12'],'finding':'Stories gate precedes approved preview; rewards inventory preview precedes gate but FR says generating card requires parent verification.','recommendation':'Clarify preview privacy and verification order; OS share remains blocked until parent verification.'}
]

features=[];records=[]
for p in sorted(PRD.glob('Feature_A*.md'),key=lambda p:int(re.search(r'Feature_A(\d+)_',p.name).group(1))):
    n=int(re.search(r'Feature_A(\d+)_',p.name).group(1))
    if n==1:continue
    t=p.read_text(encoding='utf-8-sig'); secs=numbered_sections(t); rel=p.relative_to(ROOT).as_posix()
    inventory=secs.get('1.18',''); frs=[{'id':f'A{n}-FR-{m.group(1)}','text':m.group(0).strip(),'source':rel+' §1.7','coverage':'Retained normative requirement; apply across this feature’s source inventory records. Backend/data-only rules constrain permitted sample data and prototype outcomes, not extra screens.'} for m in re.finditer(r'(?ms)^\*\*FR-(\d+)\*\*.*?(?=^\*\*FR-|\Z)',secs.get('1.7',''))]
    bdir=ROOT/'Development_Blueprints'/p.stem.removeprefix('Feature_')/'KMP'
    blueprints=[]
    for bp in sorted(bdir.glob('*.md')):
        bt=bp.read_text(encoding='utf-8-sig'); bs=numbered_sections(bt)
        selected={k:v for k,v in bs.items() if any(word in v.split('\n')[0].lower() for word in ['objective','business requirements','kmp requirements','offline','error handling','validation','localization','rtl','security','testing','verification'])}
        blueprints.append({'path':bp.relative_to(ROOT).as_posix(),'title':bt.splitlines()[0],'sections':selected})
    candidates=[x.relative_to(ROOT).as_posix() for x in sorted((ROOT/'Screens'/'Mobile App'/FEATURE_DIRS[n]).glob('*.png'))]
    inspected=[f'Screens/Mobile App/{x}' for x in INSPECTED if x.startswith(FEATURE_DIRS[n]+'/')]
    feature={'feature':f'A{n}','prd_path':rel,'full_prd_character_count':len(t),'sections':{k:v for k,v in secs.items() if k.startswith('1.') or k.startswith('2.') or k.startswith('6.') or k.startswith('13.')},'functional_requirements':frs,'blueprints':blueprints,'screen_reference_candidates':candidates,'visually_inspected':inspected}
    features.append(feature)
    for line in inventory.splitlines():
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells)<5 or not cells[0].isdigit():continue
        num,name,rawtype,entry,exit=cells[:5]
        if 'Admin' in name or 'internal use' in rawtype: scope='excluded admin/internal'
        elif 'Parent' in name or 'Parent Area' in rawtype:scope='mobile parent area; coordinate with parent audit'
        else:scope='child mobile'
        if 'variant' in rawtype.lower() or 'state' in name.lower():typ='state'
        elif any(k in rawtype.lower() for k in ['modal','sheet']):typ='overlay'
        elif 'component' in rawtype.lower():typ='component'
        elif 'transition' in rawtype.lower() or rawtype.startswith('N/A'):typ='transition'
        else:typ='screen'
        ux=[v for k,v in secs.items() if k.startswith('2.')]
        record={'id':f'A{n}-{int(num):02d}','feature':f'A{n}','name':name,'type':typ,'source_type':rawtype,'scope':scope,'prd_path':rel,'prd_section':f'§1.18 row {num}; §1.7; §2; §6; §13','source_screen_paths':candidates,'source_mapping_status':'Feature-cluster candidates only; no exact frame equivalence asserted. Screenshot absent from a named candidate is missing/unverified, not fabricated.','visually_inspected_paths':inspected,'exact_content_specification':ux,'content_status':'Exact source requirements preserved; quoted examples are illustrative and are not approved app fixture or verified religious catalog content. No canonical educational catalog is included in PRD. Preserve original frame copy until verified.','entry_points':entry,'destinations':exit,'behavior_and_actions_source':secs.get('2.3',''),'flow_and_order_notes':secs.get('1.16',''),'applicable_state_source':{k:secs.get(k,'') for k in ['1.10','1.11','1.12','1.13','1.14','1.15']},'states_scope_note':'These are feature-level state requirements; select screen-applicable cases when generating prompt, never attach all cases blindly.','requirements':frs,'blueprint_paths':[b['path'] for b in blueprints],'conflicts':[c for c in CONFLICTS if any(f'A{n} ' in str(s) or f'A{n}_' in str(s) for s in c['sources'])]}
        records.append(record)

# Explicit blueprint-only destination missing from the PRD inventory.
records.append({'id':'A9-BP-01','feature':'A9','name':'Offline Completion — Saved / Results Deferred','type':'screen','scope':'child mobile','prd_path':'PRD_Documents/Child App (1-12)/Feature_A9_Skill_Tree_Mastery_Engine.md','prd_section':'§1.14 / §6.7; blueprint K-04','source_screen_paths':[],'source_mapping_status':'Missing from named screenshot references; blueprint-required screen absent in §1.18 table.','exact_content_specification':['Saved! We’ll show your results when you’re back online'],'content_status':'Blueprint exact copy uses straight apostrophes in source; preserve literal source before execution.','entry_points':'Offline quiz completion before validated server result','destinations':'Originating context; deferred real Quiz Completion Result after connectivity and sync','behavior_and_actions_source':'Do not show raw/provisional mastery scores. Queue idempotent attempt; render real result only after sync. Avoid interrupting an unrelated active activity when deferred results arrive; interruption policy requires approval.','blueprint_paths':['Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/04-mastery-result-offline-handling-sync.md'],'conflicts':['Missing inventory row; deferred-navigation interruption behavior requires clarification.']})
for i,name in enumerate(['Arabic Letters — Contextual Form Matching (Isolated / Initial / Medial / Final)','Arabic Letters — Harakah Sound Pairing'],1):
    records.append({'id':f'A5-FR6-{i:02d}','feature':'A5','name':name,'type':'screen','scope':'child mobile','prd_path':'PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md','prd_section':'§1.7 FR-6; absent from §1.18 rows 8–11','source_screen_paths':[],'source_mapping_status':'Required mechanic missing from named screenshot inventory and not explicitly inventoried as a screen; proposed separate reviewable layout requires approved mapping.','exact_content_specification':['Use verified published letter forms, approved contextual words and phoneme/harakah audio only. PRD contains no complete exercise item content.'],'content_status':'Exact exercise catalog unavailable; no invented religious or Arabic strings.','entry_points':'Arabic Letters mode selector / scheduled node practice','destinations':'Per-answer teaching feedback; Skill Tree progress after bounded exercise','behavior_and_actions_source':'Partial progressive hints; accessible choice/tap alternative; evidence across multiple question forms and sessions required for mastery. No raw mastery score.','blueprint_paths':['Development_Blueprints/A5_Quran_Arabic_Learning/KMP/05-arabic-letters-learning-flow.md'],'conflicts':['CL-11: required mechanic absent from source screen inventory.']})

data={'audit_scope':'A2–A12 child learning and rewards; documentation only','source_review_status':'All feature files programmatically extracted; FRs, inventory, key UX and Android mapping plus all KMP objectives reviewed. Exact remaining product/Android/QA sections retained for downstream full review. Do not describe extraction as complete human inspection of every paragraph.','features':features,'screens':records,'conflicts':CONFLICTS}
(OUT/'child-learning.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# A2–A12 Child Learning Research Audit','', 'Documentation only. Original PRDs, blueprints, screenshots and Figma are unchanged.','', '## Review status and limits','',data['source_review_status'],'','Only the ten images listed below were visually inspected. Remaining screenshot paths are candidate inventories, not verified screen-to-frame mappings. Figma and hosted-mobile inspection are delegated to the parent audit. Religious screenshot content is existing reference content, not independently scholar-verified content.','']
md+=['- `Screens/Mobile App/'+x+'`' for x in INSPECTED]
md+=['','## Verified visual language','', 'Warm cream canvas, deep teal actions and selection, gold rewards/progress, serif display headings, rounded sans body, white rounded cards, neutral outline dividers and soft shadows. These are observations, not measured hex/font/radius tokens. Existing bottom navigation visibly reads Home / Learn / Stories / Rewards / Profile. Avatar has tap-based rotation alternatives. Dua Card shows Arabic/transliteration/translation/audio simultaneously. Story Detail includes scholar-review status, synopsis and resume CTA.','', '## Conflicts requiring explicit resolution','']
for c in CONFLICTS:md +=[f"### {c['id']} — {c['affected']}",'',c['finding'],'',f"Sources: {'; '.join(c['sources'])}",'',c['recommendation'],'']
for f in features:
    md +=[f"## {f['feature']} — {Path(f['prd_path']).stem}",'',f"PRD: `{f['prd_path']}`",'',f"Coverage: {len(f['functional_requirements'])} mandatory FR records; all preserved verbatim below. Feature has {sum(r['feature']==f['feature'] for r in records)} inventory records including components/states. Components and states must not inflate independently executed screen count.",'','### Existing screenshot candidates','']
    md +=['- `'+p+'`'+(' — visually inspected' if p in f['visually_inspected'] else ' — inventoried only') for p in f['screen_reference_candidates']]
    md +=['','### Complete normative functional coverage','',f['sections'].get('1.7',''),'','### Ordered source inventory','',f['sections'].get('1.18',''),'','### Exact mobile UX and behavior sources','']
    for k,v in f['sections'].items():
        if k.startswith('2.') or k in ['1.9','1.10','1.11','1.12','1.13','1.14','1.15','1.16'] or k.startswith('6.') or k.startswith('13.'):md +=[v,'']
    md+=['### Corresponding KMP blueprint requirements','']
    for b in f['blueprints']:
        md +=[f"#### `{b['path']}`",'']
        for v in b['sections'].values():md +=[v.replace('## ','##### ',1),'']
md+=['## Independent completeness review','', '- A5 requires four Arabic Letters screens and six Quran game modes; Learn screenshot cluster names do not establish that all exist. Add requirement-driven prompts with missing-reference flags rather than assuming hidden frames.', '- A8 requires five independently reviewable question-type layouts; screenshot Quiz Question-01 only verifies multiple choice. Preserve separate sequence, true/false, image-match, audio-match prompt entries.', '- Share previews, item/transaction detail, achievement level, family goal, seasonal archive, placement check and saved/deferred results destinations must remain explicit even when absent from screenshot inventory.', '- Deduplicate shared quizzes, favorites, downloads, parent gate, hints, facts and badge modals by owning feature; maintain alias entries and exact originating-context return paths.', '- No A10 game mechanics can be invented for future catalog entries; six A5 modes are specified; generic game session is a wrapper requiring a manifest-specific mechanic reference.', '- No mandatory FR is discarded: backend/ledger/scholar-governance rules are retained as constraints on design/prototype fixture outcomes, not turned into fabricated child screens.', '- Full paragraph-level audit of every retained section and exact source-screen mapping remains a parent handover task; avoid certifying extraction as all PRD text reviewed.', '- Educational catalog strings and all uninspected screenshot exact content remain execution blockers for affected prompts; source-preserving duplication is possible only after original frame/copy access.']
(OUT/'child-learning.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'features':len(features),'records':len(records),'FRs':sum(len(f['functional_requirements']) for f in features),'blueprints':sum(len(f['blueprints']) for f in features),'output':str(OUT)},indent=2))
