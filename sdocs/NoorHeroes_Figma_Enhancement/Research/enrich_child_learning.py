from pathlib import Path
import json,re
P=Path(__file__).parent
d=json.loads((P/'child-learning.json').read_text(encoding='utf-8'))
fig=json.loads((P.parent/'Evidence/figma-screens.json').read_text(encoding='utf-8'))['screens']
site=json.loads((P.parent/'Evidence/current-site-screens.json').read_text(encoding='utf-8'))['screens']
features={x['feature']:x for x in d['features']}
ALIASES={
'Child Home (composite screen)':['Html → Body'],
'Stories Library (Landing)':['Stories Library'],
'Story Detail':['Story Detail — Desert Night'],
'Story Player — Video':['Story Player — Bedtime Mode'],
'Story Player — Audio':['Audio Bedtime Player'],
'Bedtime Mode Player Variant':['Story Player — Bedtime Mode'],
'Moral Summary Card ("Noor says...")':['Moral Summary & Bedtime Reflection'],
'Audio Bedtime Player (main screen)':['Audio Bedtime Player'],
'Dua / Calm-Reflection Ending Card':['Dua Bedtime Reflection Card'],
'Quran Learning Home / Skill Tree Map':['Quran Learning Home - Skill Tree Map'],
'Quran Learning Home (Skill Tree Map)':['Quran Learning Home - Skill Tree Map'],
'Surah Learning (Ayah-by-Ayah Practice)':['Surah Learning - Ayah Practice'],
'Surah Learning':['Surah Learning - Ayah Practice'],
'AI Pronunciation Feedback Screen':['AI Pronunciation Feedback'],
'Dua Learning Landing (Category List)':['Dua Categories'],
'Dua Card Detail (Arabic/Transliteration/Translation/Audio)':['Dua Card Detail'],
'Recall Quiz Question Screen':['Recall Quiz Question'],
'Habit Builder — Today\'s Checklist':["Habit Builder — Today's Checklist"],
'Streak State Detail (AtRisk/Broken/Recovery messaging)':['Streak State Detail — Warm Recovery'],
'Noor Garden — Personal View':['Noor Garden (Personal & Family)'],
'Noor Garden — Family View':['Noor Garden (Personal & Family)'],
'Quiz Question Screen — Multiple Choice':['Quiz Question Screen'],
'Per-Answer Explanation Overlay':['Per-Answer Explanation Overlay'],
'Quiz Completion Result Screen (shared, generic)':['Quiz Completion & Mastery Result'],
'Games Hub (tile grid landing)':['Games Hub'],
'Session Completion Screen (generic wrapper, reuses A.9\'s "strengths + next step" framing where applicable)':['Game Session Completion'],
'Rewards Hub / Wallet (landing)':['Rewards Wallet'],
'Achievement Store (catalog browse)':['Achievement Store'],
'Family Board (private, multi-child families)':['Family Board'],
'Avatar Screen (3D preview + owned grid + locked teasers)':['Avatar Customization'],
'Locked Item Detail — Unlock Criteria View':['Locked Item Detail - Desert Caravan Cloak'],
}
ENHANCED={'A2':'Child Home Dashboard','A3':'Stories & Bedtime Hub','A4':'Stories & Bedtime Hub','A5':'Quran & Arabic Learning','A6':'Dua Learning Studio','A7':'Habit Builder & Sunnah Tracker','A8':'Quiz Completion & Mastery Result','A9':'Quiz Completion & Mastery Result','A10':'Skill-Reinforcement Games Hub','A11':'Rewards & Avatar Hub','A12':'Avatar Studio & Character Evolution'}
SITE_ALIAS={'A2':['Home'],'A3':['Stories','Story Detail','Player','Choice','Moral Card','Complete'],'A4':['Audio Player','Sleep Timer','Bedtime Dua'],'A5':['Skill Tree','Surah Practice','Feedback'],'A6':['Dua Categories','Dua Card','Dua Quiz'],'A7':['Habit Checklist','Streak Recovery','Noor Garden'],'A8':['Quiz Question','Quiz Complete'],'A9':['Quiz Result'],'A10':['Games Hub','Game Complete'],'A11':['Rewards Wallet','Achievements','Achievement Store','Family Board'],'A12':['Avatar','Locked Item','Evolution']}
LAYOUT={
'A2':'Preserve bounded vertical Home and the exact FR-1 section priority. Header and mission carry strongest hierarchy; separate resume rails without duplicated content. Same-screen habit rows update independently. Conditional bedtime card is absent outside the window. Keep child Home free of billing.',
'A3':'Library retains category rails and filter affordances; Detail orders cover/synopsis/governance tags before episode rows and relevant stories. Player uses immersive media area and reachable overlay controls, never distort aspect ratio. Completion follows reward → moral → optional quiz → next learning.',
'A4':'Use low-light calm-theme tokens and restrained contrast while preserving readable text. Cover/title/verified source precede scrubber and large play controls; timer/speed/download/episode controls remain secondary. Selector sheets use simple vertically stacked options, not dense wheels. Ending shows verified calm reflection without XP counters.',
'A5':'Retain spatial skill path with a linear accessible reading alternative. Verse-practice layout gives verified Arabic highest visual weight, independent translation/transliteration controls and per-ayah audio/conditional recorder. Exercises focus on one bounded task, partial hint and accessible alternatives to drag/tracing.',
'A6':'Dua detail simultaneously includes exact Arabic, transliteration, translation and audio; do not collapse these behind taps. Keep source citation visible. Favorite and Mark as Learned remain distinct; recall quiz availability reflects learned status. Categories use metadata-driven icons/order.',
'A7':'Checklist orders configured habits under date/streak summary and large targets. Dhikr receives a distinct large circular counter with decrement/reset alternatives. Garden imagery shows cumulative growth; family view is aggregate only. Recovery uses warm invitation and avoids visual failure/shame.',
'A8':'All five question types share progress/question/answer/hint skeleton. Keep answer cards large and spaced; explanation is a bottom sheet with correct restatement, explanation and Next regardless of correctness. Sequence has tap-to-place alternative, audio transcript and image alt-text.',
'A9':'Strengths precede exactly one concrete Next Step. Review Mistakes, Try Again and Continue have equal visual weight; omit Review Mistakes when none exist. Never expose raw mastery/confidence scores. Offline saved screen avoids provisional result claims.',
'A10':'Two-column mobile game grid grouped/filterable by domain; Daily Quiz is pinned near top. Age/learning tier is informational, server-selected. Game completion preserves calm participation reward and explicit Play Again/Done; no automatic endless rounds.',
'A11':'Clearly separate XP level/progression from spendable Noor Heroes Points. Wallet shows deterministic reasons, badge preview, three daily missions and weekly challenge. Store prices use points only with text. Family Board is aggregate only; owned items, purchase confirmation and shortfall must be distinguishable.',
'A12':'Preview above slot-segmented inventory; Outfits/Glow/Accessories retain selection/equipped states. Locked criteria remain visible. Rotation has tappable alternatives. Locked preview is reversible and never persistent; keep existing approved assets without uploads.'}

def norm(s):return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def match1(r):
    names=ALIASES.get(r['name'],[])
    # Html Body requires explicit known mobile Frame 1 Home node.
    if r['feature']=='A2' and r['name'].startswith('Child Home'):return next((x for x in fig if x['id']=='1096:1090'),None)
    if r['id']=='A9-01':return next((x for x in fig if x['id']=='1106:3444'),None)
    if r['id']=='A5-01':return next((x for x in fig if x['id']=='1100:2'),None)
    exact=[x for x in fig if x.get('reference')=='Frame 1' and (x['name'] in names or norm(x['name'])==norm(r['name']))]
    if exact:return exact[0]
    for x in fig:
        if x.get('reference')!='Frame 1':continue
        if len(norm(x['name']))>10 and (norm(x['name']) in norm(r['name']) or norm(r['name']) in norm(x['name'])):return x
    return None

def screen_states(r):
    name=r['name'].lower(); f=r['feature']; out=['Default as described in cited source']
    if any(k in name for k in ['library','hub','wallet','avatar screen','category','skill tree']):out+=['Source-specified skeleton loading','Cached offline view; only locally available actions enabled','Source-specified empty content if applicable']
    if 'player' in name:out+=['Loading/buffering','Playing / Paused','Withdrawn media safe stop','Downloaded offline playback','Completed / calm ending according to active context']
    if any(k in name for k in ['question','quiz','exercise','match','ordering','tracing','word']):out+=['Answer selected where submission required','Submitting / explanation shown','Media loading or graceful skip when relevant','Cached-bank offline / resume at saved index']
    if 'recorder' in name or 'pronunciation' in name:out+=['Parent-disabled / microphone denied listen-only fallback','Recording / processing','Confidence-aware feedback or reference self-assessment']
    if 'locked' in name:out+=['Criteria not met','Preview active without persistent equip','Deprecated unlock criteria unavailable']
    if 'purchase' in name or 'store' in name:out+=['Owned item','Confirming claim','Insufficient points with earned-activity suggestion','Already claimed idempotent outcome','Success with inventory ownership; equip may retry separately']
    if f in ['A8','A9'] and ('result' in name or 'completion' in name):out+=['All correct (no Review Mistakes)','Some incorrect with supportive review','Server-confirmed reward versus pending offline state','Mastery threshold accent only when confirmed','Bedtime calm/reduced-motion variant']
    if 'garden' in name or 'family board' in name:out+=['New/seedling','Growing / flourishing or aggregate goal progress','Confirmed family milestone','No per-sibling comparison']
    if 'checklist' in name:out+=['Partial / all complete today','Mercy Day protected','Offline saving independently per row','No configured habits','Ramadan conditional checklist']
    return out

out=[]
ACTION_OVERRIDES={
'A2-01':[('Mission card','Relevant assigned Story/Quran/Quiz/Habit activity'),('Continue Learning','Saved content position'),('Continue Watching','Story Player at saved media position'),('Daily Quiz','A8 Daily Quiz unless completed today'),('Habit checkbox','Update this Home row and XP/streak in place'),('Search','B13 Search'),('Notification bell','B17 Child Notifications'),('Weekly Challenge','A11 Weekly Challenge Detail'),('Milestones','A11 Achievements / Wallet'),('Bedtime Corner','A4 Audio Bedtime Player'),('Islamic Fact','B18 Fact Detail')],
'A2-21':[('Retry','Home; retain friendly retry if no connectivity')],
'A3-01':[('Story card','Story Detail'),('Filter','Category Filter Panel'),('Downloads category','B15 Downloads scoped to Stories')],
'A3-03':[('Unlocked episode / Continue','Correct Story Player format at furthest saved position'),('Locked episode','Show exact server-provided prerequisite; stay on Detail'),('Tier-gated card','C19 Parent Gate then C24 Subscription'),('Favorite','Optimistic favorite toggle; queue retry'),('Download','B15 manifest checks then progress'),('Related story','That Story Detail')],
'A3-07':[('Play/Pause','Toggle playback'),('Captions','Toggle caption visibility'),('Settings','Caption/Audio-Track/Quality Settings Sheet'),('Seek','Seek within permitted furthest-unlocked point'),('Back','Story Detail; preserve progress')],
'A3-10':[('Scripted choice option','Continue playback with approved deterministic branch; debounce duplicate taps')],
'A4-01':[('Play/Pause','Toggle playback; background media continues when permitted'),('Seek','Scrub playable downloaded/media range'),('Speed','Playback Speed Selector'),('Timer','Sleep Timer Selector'),('Download','B15 Downloads initiation'),('Episodes','Episode List Sheet'),('Next / Previous','Correct episode subject to sequential unlock and offline availability')],
'A4-04':[('Duration option','Player with parent-bounded timer active'),('Until episode ends','Player with episode-ending timer'),('Cancel','Player with previous timer unchanged')],
'A5-01':[('Ready/Learning/Practicing node','Correct Surah/Arabic/Tajweed exercise'),('Locked node','Display prerequisite without launching'),('Needs Refresh node','Gentle relevant review session'),('Placement check','Placement Check'),('Mode selector','Mode Selector Sheet')],
'A5-02':[('Answer option','Save answer and move to next placement question'),('Submit','Refresh Skill Tree with recommended/provisional state'),('Start from beginning','Skill Tree beginning path without requiring placement success'),('Retry','Resubmit placement without losing answers')],
'A5-04':[('Ayah audio / slow play','Reference playback for that ayah'),('Translation toggle','Show/hide versioned translation'),('Transliteration toggle','Show/hide only where lesson design permits'),('Record','Rationale / OS microphone request only if parent allows; otherwise listen-only'),('Hint','Progressive Hint Overlay'),('Mark practiced','Record evidence and update practice state')],
'A5-05':[('Start/Stop recording','Capture then processing; never save raw child audio by default'),('Cancel','Surah practice / caller; discard buffer'),('Continue after processing','Confidence-aware feedback or reference self-assessment')],
'A6-03':[('Listen','Single active audio playback with read-along'),('Favorite','B14 favorite toggle'),('Mark as Learned','Self-assessed learned status; enable recall entry after confirmation'),('Practice Recall Quiz','A8 DuaRecall only when learned'),('Download','B15 Dua download; always free-tier')],
'A7-01':[('Configured habit checkbox','Optimistic in-place check-in with tap-time child/date context'),('Dhikr habit','Dhikr Counter'),('Good deed','Category Selector'),('Fasting','Fasting Tracker only when parent-enabled'),('View Streak History','Streak Calendar'),('Open Noor Garden','Personal Noor Garden')],
'A7-03':[('Tap to count','Increment with gentle haptic; batch sync'),('Decrement','Decrease count without gesture requirement'),('Reset','Explicit reset confirmation behavior requires approved copy'),('Pronunciation audio','Verified reference audio'),('Target change','Preserve actual count against new target')],
'A8-08':[('Next','Next question; then missed-item retry or completion')],
'A8-10':[('Begin retry set','Only missed questions or approved close variants; bounded retry round')],
'A9-01':[('Review Mistakes','Review only missed items and explanations; no new scored attempt'),('Try Again','Fresh quiz/practice attempt with new attempt id'),('Continue','Originating consuming feature; no penalty')],
'A9-04':[('Continue / Back','Existing complete result; do not issue rewards again')],
'A10-01':[('Skill-area chip','Filtered game grid'),('Daily Quiz tile','Shared A8 Daily Quiz'),('Game tile','Game manifest loading then appropriate play wrapper')],
'A10-09':[('Play Again','New bounded game session'),('Done','Exact launch caller Home / Rewards / Games Hub')],
'A11-01':[('Transaction row','Transaction Detail'),('Badge Shelf / See all','Achievements'),('Weekly Challenge','Weekly Challenge Detail'),('Daily Mission','Required activity'),('Achievement Store','Points-only store'),('Family Board','Aggregate private Family Board')],
'A11-19':[('Confirm purchase','Atomic points debit and owned inventory grant; then Avatar Inventory'),('Already claimed','Show original idempotent success with no second debit'),('Earn more','Approved earning activities when shortfall'),('Cancel','Item Detail; no debit')],
'A12-01':[('Rotate arrows / drag','Rotate preview with accessible alternative'),('Slot category','Outfits / Glow / Accessories grid'),('Owned item','Owned Item Detail'),('Locked item','Locked Item Detail')],
'A12-04':[('Equip / Unequip','Optimistic slot-specific update; server reconcile; Avatar preview'),('Cancel','Avatar without changing state')],
'A12-06':[('Preview','Non-persistent locked-item try-on'),('Go to Activity','Exact unlocking activity from server criteria'),('Dismiss','Avatar with actual equipped state restored')],
}
for r in d['screens']:
    if r.get('scope')!='child mobile':continue
    if r['type'] in ['component','transition'] and not any(w in r['name'] for w in ['Overlay','Recorder','Rationale','Hint']):continue
    if r['type']=='state' and not any(w in r['name'] for w in ['Feedback Screen','Self-Assessment Screen','Moral Summary','Completion / Reward','Safe-Stop','Ending Card','Goodnight Idle','Full-Screen Retry','Purchase Confirmation','Archived Challenge','Good Deed Optional Note']):continue
    if 'reuses type-specific' in r['name']:continue
    f=features[r['feature']]; ref=match1(r); enh=next((x for x in fig if x.get('reference')=='Frame 2' and x['name']==ENHANCED[r['feature']]),None)
    # Similar rich hub is visual pattern only, never exact screen counterpart.
    site_name=next((n for n in SITE_ALIAS[r['feature']] if norm(n) in norm(r['name']) or (ref and norm(n) in norm(ref['name']))),None)
    site_ref=next((s for s in site if s['name']==site_name),None)
    if not site_ref and ref:
        site_ref=next((s for s in site if norm(s['name'])==norm(ref['name'])),None)
    words=set(norm(r['name']).split())-{'screen','state','detail','the','and','shared','generic'}
    selected=[x for x in f['functional_requirements'] if words & set(norm(x['text']).split())]
    if not selected:selected=f['functional_requirements'][:2]
    ux=[]
    for k,t in f['sections'].items():
        if not k.startswith('2.'):continue
        for m in re.finditer(r'(?ms)^#### Screen: ([^\n]+)\n(.*?)(?=^#### Screen:|^###|\Z)',t):
            if words & set(norm(m.group(1)).split()):ux.append(m.group(0))
    actions=[]
    for dest in re.split(r'\s/\s|,\s(?=[A-Z])',r.get('destinations','')):
        if dest.strip() and dest not in ['N/A','Back']:actions.append({'element':dest.strip(),'trigger':'Tap the corresponding source-defined control','precondition':'Active correct child session; relevant content/permission/unlock state satisfied per cited requirements','behavior':dest.strip(),'destination':dest.strip(),'validation':'Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability','back_cancel':'Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved','unavailable':'Disabled or source-specific explanation when permission/unlock/content requirements fail'})
    if site_ref:
        controls=[e.get('text') or e.get('label') for e in site_ref.get('elements',[]) if e.get('tag')=='BUTTON']
    else:controls=[]
    if r['id'] in ACTION_OVERRIDES:
        actions=[{'element':label,'trigger':'Tap','precondition':'Screen-specific availability from cited requirements; correct active child and source content','behavior':dest,'destination':dest,'validation':'Use applicable source states; server data authoritative; retain per-screen gates and offline constraints','back_cancel':'Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects','unavailable':'Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass'} for label,dest in ACTION_OVERRIDES[r['id']]]
    rec={'id':r['id'],'feature':r['feature'],'name':r['name'],'type':'overlay' if any(w in r['name'] for w in ['Overlay','Recorder','Rationale','Hint']) or r['type']=='overlay' else 'screen','feature_order':len([x for x in out if x['feature']==r['feature']])+1,'prd_path':r['prd_path'],'prd_section':r['prd_section'],'requirements':[x['id'] for x in selected],'purpose':f"Enable {r['name']} in the established {r['feature']} journey. Entry: {r.get('entry_points')}. Required outcome: {r.get('destinations')}.",'previous':r.get('entry_points'),'next':r.get('destinations'),'actions':actions,'source_controls':controls,'states':screen_states(r),'layout_enhancements':LAYOUT[r['feature']],'exact_content':ref.get('texts',[]) if ref else [],'current_site_content':site_ref.get('text') if site_ref else None,'content_status':'Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.' if ref else 'BLOCKED for exact approved copy: no exact Frame 1 counterpart verified. Do not fabricate copy, Arabic, educational items, user data or stats.','frame1':{'id':ref['id'],'name':ref['name'],'url':'https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id='+ref['id'].replace(':','-'),'mapping':'Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked'} if ref else None,'frame2':{'id':enh['id'],'name':enh['name'],'mapping':'Related enhanced feature hub for visual patterns only; not an exact screen equivalent','styles':enh.get('styles')} if enh else None,'current_mobile_screen':site_ref['name'] if site_ref else None,'screenshot_candidates':r.get('source_screen_paths',[]),'selected_verbatim_sections':ux+[x['text'] for x in selected],'feature_state_sources':r.get('applicable_state_source'),'flow_source':r.get('flow_and_order_notes'),'blueprint_paths':r.get('blueprint_paths',[]),'conflict_ids':[x['id'] if isinstance(x,dict) else x for x in r.get('conflicts',[])],'reference_gaps':[] if ref else ['Required layout has no verified exact source-frame match; access exact approved content before execution.']}
    out.append(rec)
(P/'enriched-child-learning-screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'screens_and_overlays':len(out),'frame1_mapped':sum(bool(x['frame1']) for x in out),'site_mapped':sum(bool(x['current_mobile_screen']) for x in out),'by_feature':{k:sum(x['feature']==k for x in out) for k in features}},indent=2))
