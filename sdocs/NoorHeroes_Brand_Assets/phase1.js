const page=await figma.getNodeByIdAsync('1299:2'); await figma.setCurrentPageAsync(page);
await Promise.all(['Regular','SemiBold','Bold'].map(style=>figma.loadFontAsync({family:'Poppins',style})));
const ids=[];const made=n=>{ids.push(n.id);return n}; const hex=h=>({r:parseInt(h.slice(0,2),16)/255,g:parseInt(h.slice(2,4),16)/255,b:parseInt(h.slice(4,6),16)/255});
const C={teal:'074D4D',ivory:'FEFBF4',gold:'D4A24C',ink:'1C2B33',paper:'FFFFFF'};
const existing=await figma.variables.getLocalVariablesAsync();
let collection=(await figma.variables.getLocalVariableCollectionsAsync()).find(c=>c.name==='NH V2 / Brand Assets');
if(!collection)collection=figma.variables.createVariableCollection('NH V2 / Brand Assets');
const vars={};for(const [key,value]of Object.entries(C)){let v=existing.find(v=>v.name===key&&v.variableCollectionId===collection.id);if(!v){v=figma.variables.createVariable(key,collection,'COLOR');v.scopes=['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'];v.setValueForMode(collection.defaultModeId,hex(value));}vars[key]=v;}
const paint=k=>[figma.variables.setBoundVariableForPaint({type:'SOLID',color:hex(C[k])},'color',vars[k])];
const styles=await figma.getLocalTextStylesAsync();const ts={};for(const [sz,weight]of [[14,'Regular'],[18,'Regular'],[24,'SemiBold'],[36,'SemiBold'],[48,'SemiBold'],[64,'SemiBold'],[80,'SemiBold']]){let s=styles.find(s=>s.name==='NH/Brand Assets/'+sz);if(!s){s=figma.createTextStyle();s.name='NH/Brand Assets/'+sz;s.fontName={family:'Poppins',style:weight};s.fontSize=sz;s.lineHeight={unit:'PERCENT',value:125};}ts[sz]=s.id;}
async function txt(parent,str,size=24,color='ink',width=1000){const t=made(figma.createText());t.fontName={family:'Poppins',style:'Regular'};await t.setTextStyleIdAsync(ts[size]);t.characters=str;t.fills=paint(color);t.textAutoResize='HEIGHT';t.resize(width,t.height);parent.appendChild(t);return t;}
function frame(parent,name,w,h,bg){const f=made(figma.createFrame());f.name=name;f.resize(w,h);f.fills=bg?paint(bg):[];parent.appendChild(f);return f;}
function comp(parent,name,w,h,bg){const f=made(figma.createComponent());f.name=name;f.resize(w,h);f.fills=bg?paint(bg):[];parent.appendChild(f);f.exportSettings=[{format:'PNG',suffix:'',constraint:{type:'SCALE',value:1}}];return f;}
function place(n,x,y){n.x=x;n.y=y;return n;}
async function title(section,heading,body){place(await txt(section,heading,64,'teal',5800),120,100);place(await txt(section,body,24,'ink',5700),120,205);}
function inst(parent,master,x,y,w){const n=made(master.createInstance());parent.appendChild(n);n.rescale(w/master.width);place(n,x,y);return n;}
async function crop(parent,name,source,bbox,w){const s=await figma.getNodeByIdAsync(source);const [x,y,x2,y2]=bbox;const scale=w/(x2-x);const f=frame(parent,name,w,(y2-y)*scale);f.clipsContent=true;const r=made(figma.createRectangle());r.name='Original artwork / aspect ratio locked';f.appendChild(r);r.resize(s.width*scale,s.height*scale);r.fills=JSON.parse(JSON.stringify(s.fills));place(r,-x*scale,-y*scale);return f;}
function mono(parent,master,color,name){const f=comp(parent,name,master.width,master.height);const mask=inst(f,master,0,0,master.width);mask.isMask=true;mask.maskType='ALPHA';const r=made(figma.createRectangle());f.appendChild(r);r.name='Palette tint / alpha preserved';r.resize(f.width,f.height);r.fills=paint(color);return f;}

const sections=await Promise.all(['1299:3','1299:4','1299:5','1299:6','1299:7'].map(id=>figma.getNodeByIdAsync(id)));
await title(sections[0],'NoorHeroes / Brand & App Assets','Source-controlled artwork • Android, iOS and marketing • 15 October 2026');
for(let i=0;i<8;i++){const n=await figma.getNodeByIdAsync(['1299:13','1299:14','1299:15','1299:16','1299:17','1299:18','1299:19','1299:20'][i]);n.locked=true;ids.push(n.id);place(await txt(sections[0],['01 / Transparent wordmark','02 / Teal full lockup','03 / Transparent full lockup','04 / Ivory full lockup','05 / Ivory monogram','06 / Teal monogram','07 / Transparent monogram','08 / Campaign visual reference'][i],24,'ink',1780),n.x,n.y-55);}
await title(sections[2],'Transparent logos','Original raster artwork • Genuine alpha • PNG masters • No logo font substitution');
const full=comp(sections[2],'NH/Brand/Logo/Full',1529,525);place(full,120,420);await crop(full,'Original full lockup','1299:15',[148,136,1677,661],1529);
full.description='Exact supplied image 3 alpha-bounds crop. Original pixels retained in nested image layer. PNG, not vector.';
const noTag=comp(sections[2],'NH/Brand/Logo/Without Tagline',1529,525);place(noTag,1900,420);
await crop(noTag,'Left original symbol','1299:15',[148,136,640,661],492);place(await crop(noTag,'Right original wordmark','1299:15',[725,312,1677,515],952),577,176);
const light=mono(sections[2],full,'ivory','NH/Brand/Logo/Monochrome Light');place(light,120,1200);const dark=mono(sections[2],full,'teal','NH/Brand/Logo/Monochrome Dark');place(dark,1900,1200);
for(const [m,x,y,bg]of [[full,120,2000,'ivory'],[light,1900,2000,'teal']]){const preview=frame(sections[2],'Contrast preview / '+bg,1650,700,bg);place(preview,x,y);inst(preview,m,60,85,1529);}
await title(sections[3],'App name / exact wordmark','Preserved lettering and spacing • Crops and compositions only • Editable layout; embedded artwork');
const word=comp(sections[3],'NH/Brand/Wordmark/Primary',1592,310);place(word,120,420);await crop(word,'Original wordmark','1299:13',[91,312,1683,622],1592);
const wordTag=comp(sections[3],'NH/Brand/Wordmark/With Tagline',952,325);place(wordTag,1900,420);await crop(wordTag,'Original wordmark and tagline','1299:15',[725,312,1677,637],952);
await title(sections[4],'NH monograms','Approved crescent + lantern + NH • The letterforms remain untouched');
const mark=comp(sections[4],'NH/Brand/Monogram/Primary',819,909);place(mark,120,420);await crop(mark,'Original monogram','1299:19',[217,135,1036,1044],819);
mark.description='Supplied image 7. No isolated NH or crescent-without-lantern source exists; those variants are intentionally not fabricated.';
const markLight=mono(sections[4],mark,'ivory','NH/Brand/Monogram/Monochrome Light');place(markLight,1100,420);
const markDark=mono(sections[4],mark,'teal','NH/Brand/Monogram/Monochrome Dark');place(markDark,2100,420);
for(const [bg,x]of [['teal',120],['ivory',1250]]){const tile=comp(sections[4],'NH/Brand/Monogram/Background '+bg,1024,1024,bg);place(tile,x,1600);inst(tile,mark,184,148,656);}
const horizontal=comp(sections[3],'NH/Brand/Lockup/Horizontal',1500,400);place(horizontal,120,1200);inst(horizontal,mark,0,0,340);inst(horizontal,word,440,105,1060);
const compact=comp(sections[3],'NH/Brand/Lockup/Compact',600,720);place(compact,1900,1200);inst(compact,mark,100,0,400);inst(compact,word,0,535,600);
await title(sections[1],'Android & iOS / icon masters','A · teal   B · ivory   C · transparent foreground   D · approved monogram only');
const iconMasters=[];for(const [bg,x]of [['teal',120],['ivory',1300]]){const c=comp(sections[1],'NH/AppIcon/iOS/'+bg,1024,1024,bg);place(c,x,420);inst(c,mark,184,148,656);c.description='1024px full-bleed opaque square. No baked corner radius. Import background + foreground into Icon Composer for current layered app icon workflow.';iconMasters.push(c);}
const iosFg=comp(sections[1],'NH/AppIcon/iOS/Foreground',1024,1024);place(iosFg,2480,420);inst(iosFg,mark,184,148,656);
for(const [bg,x]of [['teal',3660],['ivory',4840]]){const b=comp(sections[1],'NH/AppIcon/iOS/Background '+bg,1024,1024,bg);place(b,x,420);}
const androidFg=comp(sections[1],'NH/AppIcon/Android/Foreground',432,432);place(androidFg,120,1800);inst(androidFg,mark,130,120,172);
androidFg.exportSettings=[1,1.5,2,3,4].map((d,i)=>({format:'PNG',suffix:'-'+['mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi'][i],constraint:{type:'SCALE',value:d/4}}));
androidFg.description='108dp canvas at 4x. Artwork fits inside central 66dp diameter safe circle. Transparent foreground. No extra shadow.';
const androidMono=mono(sections[1],androidFg,'paper','NH/AppIcon/Android/Monochrome');place(androidMono,650,1800);androidMono.exportSettings=androidFg.exportSettings;
for(const [bg,x]of [['teal',1180],['ivory',1710]]){const b=comp(sections[1],'NH/AppIcon/Android/Background '+bg,432,432,bg);place(b,x,1800);b.exportSettings=androidFg.exportSettings;}
const legacy=[];for(const [bg,x]of [['teal',2240],['ivory',2570]]){const c=comp(sections[1],'NH/AppIcon/Android/Legacy '+bg,192,192,bg);place(c,x,1800);inst(c,mark,42,36,108);c.exportSettings=[48,72,96,144,192].map((s,i)=>({format:'PNG',suffix:'-'+['mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi'][i],constraint:{type:'WIDTH',value:s}}));legacy.push(c);}
for(const [bg,x]of [['teal',120],['ivory',850]]){const c=comp(sections[1],'NH/AppIcon/GooglePlay/'+bg,512,512,bg);place(c,x,2600);inst(c,mark,92,74,328);}
const safety=frame(sections[1],'Android / 108dp canvas and 66dp safe circle',432,432,'ivory');place(safety,1600,2600);inst(safety,androidFg,0,0,432);const e=made(figma.createEllipse());safety.appendChild(e);e.name='66dp safe circle / guide only';e.resize(264,264);place(e,84,84);e.fills=[];e.strokes=paint('teal');e.dashPattern=[8,8];
for(let i=0;i<2;i++){const preview=frame(sections[1],'Preview / '+['rounded square','circle'][i],432,432,i?'ivory':'teal');place(preview,2200+i*560,2600);preview.cornerRadius=i?216:96;preview.clipsContent=true;inst(preview,androidFg,0,0,432);}
for(let i=0;i<2;i++){const preview=frame(sections[1],'iOS rounded-square preview / '+i,256,256,i?'ivory':'teal');place(preview,3400+i*360,2600);preview.cornerRadius=58;preview.clipsContent=true;inst(preview,iconMasters[i],0,0,256);}
const masters={full:full.id,noTag:noTag.id,light:light.id,dark:dark.id,word:word.id,wordTag:wordTag.id,mark:mark.id,markLight:markLight.id,markDark:markDark.id,horizontal:horizontal.id,compact:compact.id,ios:iconMasters.map(n=>n.id),androidFg:androidFg.id,androidMono:androidMono.id};
return {createdNodeIds:ids,masters,sections:sections.map(s=>({id:s.id,name:s.name})),counts:{components:page.findAllWithCriteria({types:['COMPONENT']}).length}};

