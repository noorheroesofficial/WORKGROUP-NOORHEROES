$root=(Get-Location).Path
$out='sdocs/NoorHeroes_Figma_Enhancement/Research'
function Section($text,$start,$end){$a=$text.IndexOf($start);if($a -lt 0){return ''};$b=$text.IndexOf($end,$a+$start.Length);if($b -lt 0){$b=$text.Length};return $text.Substring($a,$b-$a).Trim()}
$features=@();$records=@();$md=[System.Collections.Generic.List[string]]::new()
$md.Add('# Parent mobile research — C19–C26')
$md.Add('Documentation-only research. PRD mobile sections are transcribed below to preserve exact requirements. Section 1.18 inventories contain components, overlays and variants as well as independent screens; do not turn each row into a new screen. Figma/site inspection is handled separately. Image paths are candidates until collectively inspected; only three images were individually visually inspected in this research pass. All source folders remain unchanged.')
$files=Get-ChildItem 'PRD_Documents/Parent Area In-App (19-26)' -Filter 'Feature*'
foreach($f in $files){
$text=Get-Content $f.FullName -Raw
$id=[regex]::Match($f.Name,'C\d+').Value
$slug=$f.BaseName.Replace('Feature_','')
$prd=$f.FullName.Substring($root.Length+1).Replace('\','/')
$bpdir='Development_Blueprints/'+$slug
$bps=@(Get-ChildItem $bpdir -Recurse -Filter '*.md' | Where-Object {$_.FullName -match '\\KMP\\|00-screen-to-code'} | ForEach-Object { @{path=$_.FullName.Substring($root.Length+1).Replace('\','/');text=(Get-Content $_.FullName -Raw)} })
$mobile=Section $text '## 1. Product Requirements' '## 3. Backend Requirements'
$android=Section $text '## 6. Android Requirements' '## 7. Android AI'
$qa=Section $text '## 13. QA Requirements' '## 14. Marketing'
$fr=@([regex]::Matches((Section $text '### 1.7' '### 1.8'),'(?m)^\*\*FR-(\d+)\*\*\s+(.+)') | ForEach-Object { @{id=($id+'-FR-'+$_.Groups[1].Value);requirement=$_.Groups[2].Value} })
$inventory=Section $text '### 1.18' '### 1.19'
$paths=@();foreach($bp in $bps){$paths+=@([regex]::Matches($bp.text,'Screens/Mobile App/[^`\r\n|]+\.png')|ForEach-Object{$_.Value})};$paths=@($paths|Sort-Object -Unique)
$feature=@{feature=$id;prd=$prd;mobile_sections=$mobile;android=$android;qa=$qa;functional_requirements=$fr;blueprints=$bps;image_candidates=$paths}
$features+=$feature
$md.Add("`n## $id — $prd`n")
$md.Add("Blueprints read for research extraction: "+(($bps|ForEach-Object{$_.path}) -join '; '))
$md.Add('Coverage: every FR below retained verbatim; all §1 states and §2 UX behavior retained, alongside Android §6 and QA §13. Blueprint image numbering is not journey numbering. PRD image-generation examples are recommendations/examples, not automatically approved source copy.')
$md.Add($mobile);$md.Add($android);$md.Add($qa)
foreach($line in ($inventory -split "`n")){
if($line -notmatch '^\|\s*\d+\s*\|'){continue}
$c=@($line.Trim().Trim('|').Split('|')|ForEach-Object{$_.Trim()})
$type=if($c[2] -match 'variant'){ 'state' }elseif($c[2] -match 'Modal|Component|System'){ 'overlay' }else{'screen'}
$records+=@{feature=$id;name=$c[1];type=$type;source_type=$c[2];prd=$prd;section='§1.18 row '+$c[0]+'; §1.7; §2; §6; §13';source_screen_paths=$paths;source_path_status='Feature-level candidate paths from blueprint, not an asserted one-to-one visual match';entry=$c[3];destinations=$c[4];exact_verified_copy_fields=@();copy_status='Read PRD feature.mobile_sections and inspected-image ledger; uninspected source image copy unresolved';behavior_source_feature=$id;states_source='§1.10–1.15 and §2.2 retained in feature.mobile_sections';order_notes='Within feature PRD table order; conditional branches, shared gates and components must not be linearized';conflicts=@()}
}
}
$conflicts=@(
'P-C24-01: Inspected Plan Comparison-01.png Free Family Starter says Up to 2 children; C24 FR-1 says 1 active child. Source image also offers Limited AI questions (5/day), absent from FR-1 plan list. Preserve evidence and resolve before execution.',
'P-C21-01: Inspected Delete Child Warning-01.png adds typed AISHA confirmation and only-warning footer. C21 §2.2 specifies equally sized Cancel/Permanently Delete, serious tone, no artificial delay; name typing is absent from PRD. Approval needed on retaining extra friction/copy.',
'P-C21-02: C25 FR-8 points to C21 FR-8 step 7 for account deletion cancellation; actual C21 FR-8 governs plan capacity. C26 links full account deletion into C21, but C21 has only child-deletion screens. Full account deletion warning, 7-day countdown, pending access policy and support-cancellation destination need authoritative reconciliation, not invention.',
'P-C26-01: C22 AI history is flags/safety events only (FR-5/13); C26 history is write-time-redacted input/output summaries with model_version/policy_result/expires_at (FR-6/7). Treat distinct scoped views or seek approval for merge; do not silently present full history in safety-only report.',
'P-C21-03: Blueprint refers to Add:Edit Child-01/02.png; actual filesystem uses Add_Edit Child-01/02.png. Use actual paths.',
'P-C26-02: Blueprint boilerplate suggests XP particles/Islamic illustrations/runtime camera-microphone-storage permissions on all mapped screens. PRD privacy/deletion/security surfaces do not require these; specificity and sober parent register take precedence.',
'P-C24-02: Android-focused landing label Manage on Play Store must become actual platform-specific store management affordance on iOS; iOS equivalent behavior is supported by FR-3 App Store purchase reference but exact copy requires source verification.',
'P-C25-01: QA §13 reuses child-notification binding/reminder cases and says 11 edge cases, while C25 §1.10 lists 8 parent support cases. Retain parent cases and shared B17 dependency; do not invent parent journey screens from stale QA wording.'
)
$images=@(
@{path='Screens/Mobile App/Subscription/Plan Comparison-01.png';inspected=$true;copy=@('Choose Your Plan','Start with a 7-day free trial. Cancel anytime.','Monthly','Annual','Current Plan','Free Family Starter','Perfect for trying out','$0.00 /month','Up to 2 children','Basic stories library','Essential duas & habits','Limited AI questions (5/day)','Offline mode','Premium stories','Advanced rewards & games','Unlimited AI guidance');visual='Cream surface, dark serif headings, teal selected billing segment and rounded plan outline, outlined capacity badge, green check and grey crossed-out unavailable feature rows.'},
@{path='Screens/Mobile App/Child Management/Delete Child Warning-01.png';inspected=$true;copy=@("Delete Aisha’s Profile?",'Deleted data cannot be recovered. This action is permanent.',"All of Aisha’s learning progress, achievements, and saved content will be permanently deleted. This cannot be undone.",'Type AISHA to confirm:','Type name here','Cancel','Permanently Delete','⚠️ This is your only warning. There is no undo.');visual='Sober off-white surface, small emoji avatar, red warning card, typed-name field, equally placed cancel/delete controls; delete grey disabled until name matching is implied but actual behavior is not observed.'},
@{path='Screens/Mobile App/Privacy/Consent Log-01.png';inspected=$true;copy=@('Consent Log','Required consents cannot be withdrawn while you have an active account. You can withdraw Optional consents at any time.','REQUIRED CONSENTS','Terms of Service & Privacy Policy','Granted','Required','Last changed Jun 12, 2025','Required to use NoorHeroes. Covers data handling, user rights, and platform rules.','Child Data Processing',"Required processing of your child's learning data to provide the service.",'Age Verification','You confirmed the child using this profile is under 13.','OPTIONAL CONSENTS');visual='Cream surface, bold sans headings, pale blue information banner, white grouped consent cards, teal Granted badges, blue Required tags and information icons. Date is a source fixture, not current user data.'}
)
$md.Add("`n## Verified image ledger`n")
foreach($im in $images){$md.Add('### '+$im.path);$md.Add($im.visual);$md.Add('Exact visually transcribed source strings (fixture names/dates preserved only as source evidence):');foreach($c in $im.copy){$md.Add('- '+$c)}}
$md.Add("`n## Cross-source conflicts and approval decisions`n");foreach($c in $conflicts){$md.Add('- '+$c)}
$md.Add("`n## Execution coverage and limitations`n")
$md.Add('8 PRD product/UX/Android/QA section sets and all feature KMP/visual blueprint sources extracted. Three image files visually inspected; all other PNG content/layers/interactions remain unverified in this research pass and must be inspected collectively before Figma execution. Figma nodes, components, constraints, site navigation, animations and exact remaining screen copy are deliberately not asserted. All FRs are recorded in parent.json.functional_requirements; associate them with owning screen plus cross-cutting gates/state rather than treating backend-only constraints as separate screens. Source fixtures never authorize fabricated statistics or religious text. Back behavior beyond listed exits remains a recommendation requiring reconciliation with current flow.')
@{features=$features;records=$records;inspected_images=$images;conflicts=$conflicts;limitations=@('Figma and site inspected by coordinating agent separately','Only three individual PNGs visually inspected here','Candidate image maps are feature-level; no assumed frame-to-screen match','PRD source copy examples are distinct from verified approved Figma copy')} | ConvertTo-Json -Depth 12 | Set-Content ($out+'/parent.json') -Encoding utf8
$md -join "`n`n" | Set-Content ($out+'/parent.md') -Encoding utf8
Write-Output ('Features: '+$features.Count+'; records: '+$records.Count+'; FRs: '+(($features|ForEach-Object{$_.functional_requirements.Count}|Measure-Object -Sum).Sum))
