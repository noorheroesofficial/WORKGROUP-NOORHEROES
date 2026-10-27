from pathlib import Path
import json,re,hashlib,urllib.parse
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'sdocs/NoorHeroes_Figma_Enhancement'
def read(p):return json.loads((OUT/p).read_text(encoding='utf-8'))
def write(p,s):
    dest=OUT/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(s.rstrip()+'\n',encoding='utf-8')
def ls(v):return v if isinstance(v,list) else ([] if not v else [v])
def bullets(v):return '\n'.join('- '+(json.dumps(x,ensure_ascii=False) if isinstance(x,dict) else str(x)).replace('\n','\n  ') for x in ls(v)) or '- Not supplied by this source; resolve before execution.'
def link(path,label=None,up=''):
    return '['+(label or Path(path).name)+']('+up+path.replace(' ','%20')+')'
def abslink(path,label=None):return '['+(label or Path(path).name)+'](<'+str(ROOT/path).replace('\\','/')+'>)'
def nodeurl(id):return 'https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id='+id.replace(':','-')
def fref(f):
    if not isinstance(f,dict) or not f.get('id'):return '**Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.'
    return '['+f.get('name','Unnamed')+']('+nodeurl(f['id'])+') — `'+f['id']+'`. '+f.get('mapping','')
fig=read('Evidence/figma-screens.json')['screens']
fmap={x['id']:x for x in fig}
site=read('Evidence/current-site-screens.json')['screens']
raw=[]
raw+=read('Research/onboarding-enriched.json')
raw+=read('Research/enriched-child-learning-screens.json')
raw+=read('Research/supporting-enriched.json')
raw+=read('Research/parent-enriched.json')
records=[];aliases=[]
aliasrules={
('C19','Who Is Learning (Profile Picker)'):('A1','Profile Picker'),
('C19','Profile Lock Verification (Pattern/PIN/Fingerprint)'):('A1','Child Lock Screen'),
('C23','Calm Rest Screen (limit reached)'):('C19','Calm Locked State'),
('C23','Bedtime Block Screen (new session attempt during bedtime)'):('C19','Bedtime Block Screen'),
('A3','Favorites List'):('B14','Favorites'),
('A3','Downloads Manager (Stories scope)'):('B15','Downloads'),
('A6','Favorites List (Dua-filtered view, shared component with A.3)'):('B14','Favorites'),
('A6','Downloads Manager (Dua scope, shared with A.16)'):('B15','Downloads'),
('A6','Search Results (Dua-scoped)'):('B13','Search Results'),
('A5','Islamic Fact Detail (Learn-tab linked)'):('B18','Islamic Fact Detail'),
('A5','Daily Quiz (Learn-tab instance)'):('A8','Quiz Question Screen — Multiple Choice'),
('A5','Quiz Per-Answer Explanation Overlay'):('A8','Per-Answer Explanation Overlay'),
('A5','Quiz Retry Set (mistakes)'):('A8','Retry Set Entry Screen'),
('A5','Quiz Results / Effort XP Reveal'):('A9','Quiz Completion Result Screen'),
('A8','Hint Overlay (cross-cutting, shared with A.5)'):('A5','Hint Overlay'),
('A7','Fasting Tracker (Ramadan/practice)'):('F36','Fasting Tracker'),
}
for x in raw:
    key=(x['feature'],x['name'])
    if key in aliasrules:
        aliases.append({'feature':x['feature'],'name':x['name'],'owner_feature':aliasrules[key][0],'owner_prefix':aliasrules[key][1],'source':x.get('prd',x.get('prd_path')),'section':x.get('section',x.get('prd_section'))});continue
    if x['type']=='component' and x['feature']!='F36':
        aliases.append({'feature':x['feature'],'name':x['name'],'owner_feature':'A2','owner_prefix':'Child Home','source':x.get('prd'),'section':x.get('section')});continue
    r=dict(x)
    r['prd']=x.get('prd',x.get('prd_path'))
    r['section']=x.get('section',x.get('prd_section','§1.7; §1.18; §2'))
    r['entry']=x.get('entry',x.get('previous','Contextual entry in source narrative'))
    r['destinations']=x.get('destinations',x.get('next',x.get('behavior','See source flow')))
    r['purpose']=x.get('purpose',x.get('behavior','Enhance '+x['name']+' within its established mobile journey.'))
    r['fields']=x.get('required_fields',x.get('content_fields',[]))
    r['actions']=x.get('actions',x.get('action_rules',x.get('behavior',r['destinations'])))
    r['layout']=x.get('layout_improvements',x.get('layout_enhancements',[]))
    r['source_paths']=x.get('source_screen_paths',x.get('screenshot_candidates',x.get('source_screens',[])))
    r['site_name']=x.get('site_reference',x.get('current_mobile_screen',(x.get('current_site') or {}).get('screen_name')))
    r['site_copy']=x.get('exact_site_copy',x.get('current_site_content',x.get('exact_current_site_copy','')))
    r['site_controls']=x.get('overlay_controls',x.get('site_elements',x.get('current_site_interactions',x.get('site_interactions',[]))))
    if not r['site_controls'] and r['site_name'] and 'overlay_controls' not in x:
        r['site_controls']=next((s.get('elements',[]) for s in site if s['name']==r['site_name']),[])
    r['copy']=x.get('exact_content',x.get('exact_copy',x.get('exact_verified_copy_fields',[])))
    r['order']=x.get('feature_order',x.get('order',len(records)))
    if r['feature']=='F36':
        seasonal=['Ramadan Prep / Countdown','Ramadan Home','Ramadan Journey Map','Night Recap','Ramadan Mission Detail','Ramadan Story Player','Fasting Tracker','Laylatul Qadr Reflection','Eid Countdown','Eid Home','Eid Reward Reveal','Eid Card Generator','Ramadan Complete Certificate','Post-Eid Keep the Habit','Parent Ramadan Settings','Parent Ramadan Dashboard','Family Ramadan Aggregate','Family Ramadan Report','Conversion Moment Card','Family Member Invite']
        r['order']=seasonal.index(r['name'])+1
    records.append(r)
# Missing independent destinations explicitly documented, without fabricated approved copy.
extra=[('C22','Full Activity Timeline','C20 §2.3 Activity Timeline Preview → See All; C22 inventory missing independent destination','Parent Dashboard activity See All','Selected child activity details; filters only if approved','Parent Dashboard / Per-Child Report'),('C26','Account Deletion Request and Confirmation','C26 §1.7 / §1.18 deletion entry; C25 support cancellation; referenced C21 deletion flow is broken','Privacy & Support → Delete Account','Authoritative impact summary, identity step-up, cancellation window and exact legal copy unresolved','Pending deletion status or invoking Privacy'),('C26','Pending Account Deletion and Cancellation','C25 account-deletion-cancellation support category; C26 cross-reference unresolved','Confirmed deletion request / returning authenticated family','Verified request status and permitted cancellation action; final retention/cancellation policy unresolved','Privacy & Support or signed-out completion')]
for feature,name,section,entry,fields,dest in extra:
    prd=next((ROOT/'PRD_Documents').rglob('Feature_'+feature+'_*.md'))
    records.append({'feature':feature,'name':name,'type':'screen','prd':str(prd.relative_to(ROOT)).replace('\\','/'),'section':section,'entry':entry,'destinations':dest,'purpose':'Account for a referenced destination missing a complete independent specification. **Execution blocked until the cross-source decision is approved.**','fields':[fields],'states':['Pending authoritative policy/copy; no invented production states'],'actions':['Back/cancel → invoking verified parent context. Final destructive or cancellation transition is unspecified and blocked.'],'layout':['Sober parent-only review layout; do not hide consequences or use persuasion.'],'source_paths':[],'site_name':None,'site_copy':'','site_controls':[],'copy':[],'frame1':None,'frame2':None,'order':999,'conflicts':['G-07'],'execution_status':'BLOCKED: incomplete authoritative destination specification'})
featureorder=['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','B13','B14','B15','B16','B17','B18','C19','C20','C21','C22','C23','C24','C25','C26','F36']
records.sort(key=lambda x:(featureorder.index(x['feature']),x['order']))
for i,r in enumerate(records,1):
    r['number']=i;r['slug']=re.sub(r'[^A-Za-z0-9]+','_',r['name']).strip('_')[:125];r['file']=f"Screen_Prompts/{i:03d}_{r['slug']}.md"
promptdir=OUT/'Screen_Prompts'
expected={Path(r['file']).name for r in records}
if promptdir.exists():
    for prior in promptdir.glob('*.md'):
        if re.match(r'^\d{3}_',prior.name) and prior.name not in expected:
            assert prior.resolve().parent==promptdir.resolve()
            prior.unlink()
def resolve(feature,prefix):return next((r for r in records if r['feature']==feature and r['name'].startswith(prefix)),None)
for a in aliases:
    owner=resolve(a['owner_feature'],a['owner_prefix']);a['owner_number']=owner['number'] if owner else None;a['owner_file']=owner['file'] if owner else None
write('Evidence/normalized-screen-records.json',json.dumps(records,ensure_ascii=False,indent=2))
write('Evidence/shared-surface-aliases.json',json.dumps(aliases,ensure_ascii=False,indent=2))
def motion(r):
    kind=r['type'];name=r['name'].lower()
    rows=[]
    if kind in ['overlay','component']:
        rows.append(['Open/close by defined control','Closed ↔ visible, opacity0→1; sheet bottom→rest only if sheet specified','200ms ease-out opening;160ms ease-in closing;no delay','Reversible; cancel closes and returns focus; navigate away closes','Instant show/hide','Open overlay / Close overlay; Move in from bottom only for actual sheet'])
    elif kind=='state':
        rows.append(['State response changes','Previous state→new labeled state; no decorative entrance','120ms dissolve;no delay','Interruptible; ignore stale completion after leaving','Instant replace with same labels','State variants via Change to or separately labeled scenario frames'])
    else:
        rows.append(['Approved forward/back action','Current frame→destination, preserving directional history','250ms ease-in-out;no delay','Reversible with Back; cancel pending animation when leaving','Instant navigation or ≤100ms dissolve','Navigate to + Dissolve; matched-layer Smart Animate only after layer-name/structure check'])
    if any(t in name for t in ['splash','reveal','celebration','completion','unlock']):
        rows.append(['Data-confirmed success or first entry','Hidden status→visible check/progress; splash logo opacity0→1 scale.98→1','400ms ease-out; splash≤1200ms; reward total≤2000ms;no mandatory wait','Skippable/interruptible; stop on leave; no reward repeats after resume','Static success/brand state','Smart Animate between matching states; After delay only for visual sequence, never server validation'])
    if 'listening' in name or 'recorder' in name:
        rows.append(['Permission granted and user starts recording','Idle→calm recording/listening indicator','600ms ease-in-out pulse, no stagger','Stop on Cancel, permission loss, interrupt or leave; never continue mic in prototype','Static Recording label','Interactive component recording/idle variants; simulated audio only'])
    if any(t in name for t in ['bedtime','qadr','goodnight']):
        rows.append(['Wind-down mode','Day styling→dim calm styling, no shimmer or celebration burst','150ms dissolve;no delay','Reversible on authorized mode change; stop on leave','Static calm state','Dissolve between calm variants; no looping decorative animation'])
    rows.append(['Press/release enabled control','Rest→pressed→rest; preserve hit area','100ms ease-out scale.96 (proposal);0ms delay','Release/cancel reverses; disabled has no activation','Color/border pressed feedback only','While pressing → Change to pressed; On click → approved action'])
    return '| Trigger | Start → end / direction | Timing | Interruption / leave | Reduced motion | Figma approach |\n|---|---|---|---|---|---|\n'+'\n'.join('| '+' | '.join(v)+' |' for v in rows)
def compactsource(r):
    if r['feature']=='A1':return ''
    if r['feature'].startswith('C') and r.get('selected_prd_ux_text'):return r['selected_prd_ux_text']
    p=ROOT/r['prd'];t=p.read_text(encoding='utf-8');name=r['name']
    ux=re.search(r'^## 2\..*?(?=^## 3\.|\Z)',t,re.M|re.S)
    t=ux.group(0) if ux else ''
    # Retain screen-specific specification where exact header exists; no guessed copy.
    heads=list(re.finditer(r'^#### (?:Screen[: —-]?\s*)?(.+)$',t,re.M))
    needle=set(re.findall(r'[a-z]{4,}',name.lower()))-{'screen','shared','generic','overlay','state','main','learning'}
    ranked=[]
    for j,h in enumerate(heads):
        words=set(re.findall(r'[a-z]{4,}',h.group(1).lower()));score=len(needle&words)
        if score>=min(2,len(needle)) and score>0:ranked.append((score,t[h.start():heads[j+1].start() if j+1<len(heads) else min(len(t),h.start()+8000)]))
    selected=max(ranked,key=lambda x:x[0])[1][:12000] if ranked else ''
    # Never mistake backend API paragraphs for a screen interaction definition.
    selected=re.split(r'^## |^### ',selected,maxsplit=1,flags=re.M)[0] if selected else ''
    return selected
def exact(r):
    parts=[]
    if r['site_copy']:parts.append('### Current mobile source — exact captured text\n\n```text\n'+r['site_copy']+'\n```')
    f=r.get('frame1');fid=f.get('id') if isinstance(f,dict) else None
    texts=fmap.get(fid,{}).get('texts',[])
    if texts:parts.append('### Frame 1 — exact layer text (separate source; differences need approval)\n\n```text\n'+'\n'.join(texts)+'\n```')
    elif r['copy']:parts.append('### Other verified source text / fields\n\n'+bullets(r['copy']))
    parts.append('### Requirement-driven fields and content roles\n\n'+bullets(r['fields']))
    if not r['site_copy'] and not texts and not r['copy']:parts.append('**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.')
    parts.append('Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.')
    return '\n\n'.join(parts)
for r in records:
    num=r['number'];feature=r['feature'];name=r['name'];prev=r['entry'];nxt=r['destinations']
    source=compactsource(r)
    conflicts=ls(r.get('conflict_ids',r.get('conflicts',[])))
    refs='\n'.join('- '+abslink(p) for p in r['source_paths'] if isinstance(p,str)) or '- Missing corresponding local screen reference.'
    act=r['actions'];actblock=bullets(act)
    states=bullets(r.get('states',[]))
    inline=r.get('inline_components_and_variants',[])
    blueprints=r.get('blueprint_paths',[])
    if not blueprints:
        dirs=list((ROOT/'Development_Blueprints').glob(feature+'_*'))
        if dirs:blueprints=[str(p.relative_to(ROOT)).replace('\\','/') for p in (dirs[0]/'KMP').glob('*.md')]
    state_sources=r.get('feature_state_sources') or {}
    extra_state='\n\n'.join(v for k,v in state_sources.items() if k in ['1.10','1.11','1.12','1.13','1.14','1.15'])
    if not extra_state and r.get('edge_case_source'):extra_state=r['edge_case_source']
    selected_reqs='\n\n'.join(s for s in ls(r.get('selected_verbatim_sections')) if isinstance(s,str) and s.startswith('**FR-'))
    motion_extra=r.get('motion_extra','')
    palette='Preserve existing seasonal skin: Ramadan deep navy, Qadr calm violet and Eid brighter celebratory palette as inspected in references; map approved seasonal token aliases and verify contrast. Do not force the regular cream background onto seasonal screens.' if feature=='F36' else 'Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors.'
    # Source state text is provided distinctly rather than pretending every feature state applies here.
    navigation='''For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.'''
    doc=f'''# Screen {num:03d} — {name}

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **{feature} — {name}**.
- Surface: **{r['type']}**. Number is controlled review order, not a forced linear user journey.
- Execution status: **{r.get('execution_status',r.get('content_status','Pending documentation approval and screen-specific source reconciliation'))}**.
- Journey entry / previous screen: {prev}.
- Next screen(s) / result: {nxt}.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: {abslink(r['prd'])}; **{r['section']}**.
- Current mobile reference: {'[NoorHeroes current preview](https://noorheroes.figma.site/) → selector **'+str(r['site_name'])+'**; exact text captured below.' if r['site_name'] else '**Missing independently mapped current-site screen.**'}
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: {fref(r.get('frame1'))}
- Frame 2 container: `1085:13003`; visual reference: {fref(r.get('frame2'))}
- Reference qualification: {r.get('mapping_note',r.get('reference_gaps',r.get('frame2_status','Any feature-hub mapping is visual-only; compare exact screen identity before execution.')))}.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
{refs}
- Blueprint alignment:
{bullets([abslink(p) for p in blueprints])}
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: {bullets(conflicts) if conflicts else 'No screen-specific ID supplied; still check global G-01–G-10 and source content differences.'} See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

{r['purpose']}

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

{selected_reqs or 'The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.'}

## 4. Exact content specification

{exact(r)}

## 5. Visual enhancement instructions

{bullets(r['layout'])}

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- {palette} Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

{states}

{('Owning inline components / variants (do not create unrelated standalone routes):\n'+bullets(inline)) if inline else ''}

Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

{extra_state or 'Use the linked PRD §1.10–1.15 and the independently mapped states above; unspecified messages remain blocked.'}

</details>

## 7. Interactions and navigation

{actblock}

{navigation}

Verified current-preview controls, retained to prevent omitted clickable elements:

{bullets(r['site_controls'])}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

{source or 'No independently named per-screen UX subsection exists. The PRD screen inventory entry, feature click-target table and functional requirements remain the authority; use research evidence and resolve unmatched targets before execution.'}

</details>

## 8. Motion and animation specification

{motion(r)}

{bullets(motion_extra) if motion_extra else ''}

Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/{num:03d}/{r['slug']}/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/{r['slug']}`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] {feature} behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
- [ ] Every captured product control has an approved trigger, precondition, destination/state and cancel/back result; no unresolved control is silently wired.
- [ ] Applicable states are visibly reviewable; retry/draft/permission-denial/resume behavior matches the cited rules. No irrelevant states were added.
- [ ] All body text/background pairs≥4.5:1 and large text≥3:1; status has text/icon, not color alone.
- [ ] Touch targets≥44×44; no clipped text or action overlap at320/360/390/420 widths or200% text scaling; Arabic/Urdu RTL tested with numeral exceptions.
- [ ] Motion timing/interruptibility matches section8; reduced motion retains all feedback; navigation is immediately available.
- [ ] Reference IDs and any new working-node IDs recorded; original and unrelated nodes unchanged.
- [ ] Sample data/price/religious verification provenance is identified; missing legal/localized/educational content blocks execution rather than being fabricated.
- [ ] Default and relevant alternate states captured as evidence and compared; screen approved by user before proceeding.

## 11. Review and correction instructions

Implement only this screen and its necessary local dependencies after approval. Do not modify unrelated screens or source frames. Report inaccessible references, missing requirements and unmatched controls. List changes, exact-copy comparison and acceptance checks performed, with evidence and created node IDs. Record unresolved questions. **Stop and wait for my review and approval before moving to another screen.**
'''
    write(r['file'],doc)
# Ordered screen index and screen-to-source matrix.
inventory=['# Screen inventory and controlled review order','', 'Numbers follow the documented feature/journey review sequence. Alternate branches, overlays and system states are labeled; they are not mandatory steps in a single linear path. Source inventory tables frequently use filename order, which is not user encounter order. The global navigation document controls routing.','']
matrix=['# Requirement-to-screen reference matrix','','PRD → current mobile reference → Frame1 → Frame2 → enhancement → individual prompt. Missing means no independently verified correspondence; a feature-level screenshot candidate is not an exact match. Exact FR obligations are retained separately in the requirement register.','', '| Prompt | Requirement source | Existing mobile | Frame1 | Frame2 visual | Proposed enhancement |','|---|---|---|---|---|---|']
last=None
for r in records:
    if last!=r['feature']:
        inventory+=['## '+r['feature'],'','| Review # | Surface | Type | Entry / branch | Exit / result |','|---|---|---|---|---|'];last=r['feature']
    clean=lambda v:str(v).replace('|',' / ').replace('\n',' ')
    inventory.append(f"| {r['number']:03d} | {link(r['file'],r['name'])} | {r['type']} | {clean(r['entry'])} | {clean(r['destinations'])} |")
    matrix.append('| '+' | '.join([link(r['file'],f"{r['number']:03d} {r['name']}"),abslink(r['prd'],r['feature'])+' '+r['section'],clean(r['site_name'] or 'Missing'),fref(r.get('frame1')),fref(r.get('frame2')),clean(' '.join(str(v) for v in ls(r['layout'])))])+' |')
inventory+=['','## Shared surfaces and contextual aliases','','These are mapped to an owning prompt, preserving caller context and return path rather than generating conflicting duplicate screens.','', '| Source context | Owner prompt |','|---|---|']
for a in aliases:inventory.append('| '+a['feature']+' / '+a['name']+' | '+(link(a['owner_file'],f"{a['owner_number']:03d}") if a['owner_file'] else '**Unresolved owner**')+' |')
write('02_SCREEN_INVENTORY_AND_ORDER.md','\n'.join(inventory));write('03_REQUIREMENT_TRACEABILITY_MATRIX.md','\n'.join(matrix)+'\n\nSee [every-FR register](10_REQUIREMENT_COVERAGE_REGISTER.md), [shared aliases](Evidence/shared-surface-aliases.json) and [exact extraction](Evidence/figma-screens.json).')
index=['# NoorHeroes — Figma enhancement documentation','','**Phase: documentation for review only. No Figma designs created, edited, moved or deleted.** Prepared 13 October 2026, Asia/Kolkata. All generated files are isolated under `sdocs/NoorHeroes_Figma_Enhancement/`.','',f"The package contains **{len(records)} independently reviewable prompts** (screens, owned overlays, and explicitly labeled state surfaces). Numbering is review order; conditional user navigation follows the source flows. Prompts with missing copy, conflicting requirements or proposed surfaces are blocked until the relevant decision is approved.",'','## Review documents','']
docs=['01_SOURCE_AUDIT_AND_ACCESSIBILITY.md','02_SCREEN_INVENTORY_AND_ORDER.md','03_REQUIREMENT_TRACEABILITY_MATRIX.md','04_EXISTING_VS_ENHANCED_DESIGN_AUDIT.md','05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md','06_GLOBAL_NAVIGATION_AND_PROTOTYPE_ARCHITECTURE.md','07_MOTION_AND_ANIMATION_GUIDELINES.md','08_ACCESSIBILITY_RESPONSIVENESS_AND_EDGE_CASES.md','09_OPEN_QUESTIONS_AND_APPROVALS.md','10_REQUIREMENT_COVERAGE_REGISTER.md','11_CURRENT_CONTROL_RECONCILIATION.md','99_FINAL_VALIDATION_CHECKLIST.md']
index+=['- '+link(d,d.replace('_',' ').removesuffix('.md')) for d in docs]
index+=['','## Evidence and source research','','- [Figma exact-copy and structural extraction](Evidence/figma-screens.json)','- [Current mobile catalogue / exact DOM copy](Evidence/current-site-screens.json)','- [Ramadan20 mobile exact-copy previews](Evidence/current-site-ramadan.json)','- [Source manifest](Evidence/source-manifest.json)','- [Onboarding requirements records](Research/onboarding-enriched.json)','- [Child learning audit](Research/child-learning.md)','- [Supporting/seasonal audit](Research/supporting.md)','- [Parent audit](Research/parent.md)','','## Screen-by-screen execution sequence','','Review source/decision documents first; approve global tokens/working area; resolve each screen’s blocking copy/flow conflicts; then execute exactly one prompt, compare references and evidence, correct, and approve before the next. Start with Splash after its references and shared gates are settled. Branch screens are reviewed in their listed group; prototype routes depend on actual user state, not numeric successor.','']
last=None
for r in records:
    if last!=r['feature']:index+=['','### '+r['feature'],''];last=r['feature']
    index.append(f"- {r['number']:03d}. {link(r['file'],r['name'])} — {r['type']}")
write('00_MASTER_INDEX.md','\n'.join(index))
print({'prompts':len(records),'aliases':len(aliases),'features':len(set(r['feature'] for r in records))})
