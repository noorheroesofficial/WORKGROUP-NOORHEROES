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

const ex=await figma.getNodeByIdAsync('1299:11'),qa=await figma.getNodeByIdAsync('1299:12');
for(const [source,parent,bg,x,y]of [['1299:14','1299:5','Teal',120,3000],['1299:16','1299:5','Ivory',2100,3000],['1299:17','1299:7','Ivory',120,2900],['1299:18','1299:7','Teal',1550,2900]]){const s=await figma.getNodeByIdAsync(source);const sec=await figma.getNodeByIdAsync(parent);const c=comp(sec,'NH/Brand/'+(parent==='1299:5'?'Logo':'Monogram')+'/Original '+bg,s.width,s.height);place(c,x,y);c.fills=JSON.parse(JSON.stringify(s.fills));c.description='Exact supplied artwork with original '+bg+' background.';}
const word=await figma.getNodeByIdAsync('1300:57'),ws=await figma.getNodeByIdAsync('1299:6');
place(mono(ws,word,'ivory','NH/Brand/Wordmark/Monochrome Light'),120,2300);
place(mono(ws,word,'teal','NH/Brand/Wordmark/Monochrome Dark'),1900,2300);
await title(ex,'Export catalog','PNG assets linked to masters • Dimensions are output pixels • Raster logos are not SVG vectors');
const all=page.findAllWithCriteria({types:['COMPONENT']});const manifest=[];
for(let i=0;i<all.length;i++){const c=all[i];const row=frame(ex,'Export / '+c.name,1860,310,'ivory');row.cornerRadius=18;place(row,120+(i%3)*1980,420+Math.floor(i/3)*350);const scale=Math.min(200/c.width,220/c.height);const preview=made(c.createInstance());row.appendChild(preview);preview.rescale(scale);place(preview,24+(200-preview.width)/2,30+(220-preview.height)/2);preview.exportSettings=c.exportSettings.map(s=>({...s,constraint:{type:'WIDTH',value:Math.round(s.constraint.type==='WIDTH'?s.constraint.value:c.width*s.constraint.value)}}));
const name=(c.parent.type==='COMPONENT_SET'?c.parent.name+'/'+c.name:c.name).replace(/^NH\//,'noorheroes/');const file=name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-$/,'');
const bg=c.fills.length===0?'transparent':c.fills.some(f=>f.type==='IMAGE')?'original background':c.fills[0].color.r<.2?'teal':'ivory';
place(await txt(row,file,24,'teal',1500),270,36);place(await txt(row,Math.round(c.width)+' × '+Math.round(c.height)+' px · PNG · '+bg,18,'ink',1500),270,136);place(await txt(row,'Master '+c.id+' · '+c.exportSettings.length+' export size(s) · Editable copy properties',18,'ink',1500),270,188);
manifest.push({id:c.id,filename:file,w:Math.round(c.width),h:Math.round(c.height),bg,scales:c.exportSettings.map(s=>s.constraint.type==='WIDTH'?s.constraint.value/c.width:s.constraint.value)});
}
ex.resizeWithoutConstraints(6200,500+Math.ceil(all.length/3)*350);
await title(qa,'Quality check & specifications','Artwork integrity, alpha, sizing and handoff • 15 October 2026');
const notes=[
['Artwork integrity','Images 1–7 retain original raster pixels. Proportional sizing and cropping only. Monochrome uses the original alpha mask. Image 8 guides campaigns; its alternate wordmark is not substituted.'],
['Backgrounds','Teal #074D4D and ivory #FEFBF4 are sampled from the supplied backgrounds. JPEG gradients vary; original-background masters preserve those references exactly.'],
['Android','Adaptive: 108dp square, 432px at 4x. Central 66dp safe circle. Layer outputs: 108 / 162 / 216 / 324 / 432px. Legacy outputs: 48 / 72 / 96 / 144 / 192px.'],
['iOS','Opaque 1024px square masters plus separate foreground/background for Icon Composer. Corners are preview-only. Final .icon assembly and device appearance testing require Xcode.'],
['Social templates','Square 1080px; portrait 1080 × 1350; story 1080 × 1920. Working formats: Meta Help was inaccessible, so verify destination previews. Bracketed text requires approved copy.'],
['Platform covers','YouTube 2560 × 1440, center safe area about 1544 × 422. X 1500 × 500; top/bottom 60px may crop. Live LinkedIn Help: company cover 1512 × 256. Facebook 851 × 315 is provisional. Web 1920 × 640 is a design choice.'],
['Missing source variants','No isolated NH or crescent-without-lantern artwork was supplied. Withheld rather than fabricated. No original vector logo or font file was found; exact wordmark pixels are preserved.'],
['Validation boundary','Check structure, alpha and exported renders before handoff. App Store submission, actual launcher rendering and social upload previews are not tested. Lantern detail reduces at small sizes; simplification needs separate artwork approval.']];
for(let i=0;i<notes.length;i++){const b=frame(qa,notes[i][0],2820,340,'ivory');place(b,120+(i%2)*2950,420+Math.floor(i/2)*390);b.cornerRadius=20;place(await txt(b,notes[i][0],36,'teal',2660),60,40);place(await txt(b,notes[i][1],24,'ink',2660),60,112);}
const tiny=frame(qa,'Small-size and monochrome review',2800,500,'teal');place(tiny,120,2150);inst(tiny,await figma.getNodeByIdAsync('1300:68'),60,70,220);const ico=await figma.getNodeByIdAsync('1300:102');for(let i=0;i<4;i++){const size=[128,64,48,32][i];inst(tiny,ico,430+i*400,150,size);place(await txt(tiny,size+' px',24,'ivory',220),430+i*400,330);}
const yt=await figma.getNodeByIdAsync('1301:512');const mobile=frame(qa,'YouTube / mobile crop',1544,422);place(mobile,120,2900);mobile.clipsContent=true;inst(mobile,yt,-508,-509,2560);
const desktop=frame(qa,'YouTube / desktop crop',2560,422);place(desktop,120,3500);desktop.clipsContent=true;inst(desktop,yt,0,-509,2560);
const fb=frame(qa,'Facebook / narrow approximation',560,315);place(fb,3100,2900);fb.clipsContent=true;inst(fb,await figma.getNodeByIdAsync('1301:536'),-145,0,851);
const xp=frame(qa,'X / top-bottom crop',1500,380);place(xp,3100,3500);xp.clipsContent=true;inst(xp,await figma.getNodeByIdAsync('1301:584'),0,-60,1500);
const secs=page.children.filter(n=>n.type==='SECTION');for(const s of secs){if(s.id==='1299:11')continue;s.resizeWithoutConstraints(6200,Math.max(...s.children.map(n=>n.y+n.height))+180);ids.push(s.id);}
let y=1000;for(let j=0;j<secs.length;j+=2){const pair=secs.slice(j,j+2);pair.forEach((s,k)=>{s.x=1000+k*6500;s.y=y});y+=Math.max(...pair.map(s=>s.height))+500;}
return {createdNodeIds:ids,manifest,componentCount:all.length,qa:[tiny.id,mobile.id,desktop.id,fb.id,xp.id]};
