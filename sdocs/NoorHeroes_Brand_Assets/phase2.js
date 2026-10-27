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

const mark=await figma.getNodeByIdAsync('1300:65');const word=await figma.getNodeByIdAsync('1300:57');const horizontal=await figma.getNodeByIdAsync('1300:86');
function line(parent,w,color='gold',h=3){const r=made(figma.createRectangle());r.name='Tab line / editable';r.resize(w,h);r.fills=paint(color);parent.appendChild(r);return r;}
function stack(parent,name,w,gap){const f=made(figma.createAutoLayout('VERTICAL'));f.name=name;parent.appendChild(f);f.fills=[];f.resize(w,100);f.primaryAxisSizingMode='AUTO';f.counterAxisSizingMode='FIXED';f.itemSpacing=gap;return f;}
async function textprop(c,parent,name,value,size,color,width){const t=await txt(parent,value,size,color,width);t.name=name;const key=c.addComponentProperty(name,'TEXT',value);t.componentPropertyReferences={characters:key};return t;}
function badge(parent,x,y,size){const b=frame(parent,'Artwork on ivory / original colors',size,size,'ivory');b.cornerRadius=size*.12;place(b,x,y);inst(b,mark,size*.19,size*.14,size*.62);return b;}
async function tab(parent,label,width,dark=false,size=14){const s=stack(parent,'Tab + line',width,10);await txt(s,label,size,dark?'ivory':'teal',width);line(s,width);return s;}
const app=await figma.getNodeByIdAsync('1299:8');await title(app,'App banners / tab-line system','Six content families • Two backgrounds • Editable title and supporting copy • 320–640 px widths');
const category=['Featured','Stories & learning','Quran & duas','Missions & habits','Announcements','Section header'];const appVariants=[];
for(let i=0;i<6;i++)for(let j=0;j<2;j++){const bg=j?'ivory':'teal';const c=comp(app,'Category='+category[i]+', Background='+bg,350,i===5?120:228,bg);c.cornerRadius=20;c.clipsContent=true;
const content=stack(c,'Content / Auto Layout',i===5?302:214,14);place(content,24,22);await tab(content,category[i].toUpperCase(),i===5?302:214,!j);await textprop(c,content,'Title',i===5?'[Section title]':'[Approved title]',24,j?'teal':'ivory',i===5?302:214);
if(i!==5){await textprop(c,content,'Description','[Short supporting copy]',14,j?'ink':'ivory',214);badge(c,258,90,72);}
c.description='Reusable mobile banner. Edit Title and Description component properties. Tab-line placement and content use Auto Layout. Placeholder text is not approved religious content.';appVariants.push(c);}
const appSet=made(figma.combineAsVariants(appVariants,app));appSet.name='NH/Banner/Tabline';place(appSet,120,420);appSet.resize(1900,1760);appVariants.forEach((c,i)=>place(c,32+(i%4)*460,32+Math.floor(i/4)*560));
const responsive=frame(app,'Responsive samples / 320 and 640',1500,500);place(responsive,2200,420);
const narrow=inst(responsive,appVariants[0],0,0,350);narrow.resize(320,228);
const wide=inst(responsive,appVariants[1],470,0,350);wide.resize(640,228);
const contentWide=wide.findOne(n=>n.name==='Content / Auto Layout');if(contentWide){contentWide.resize(450,contentWide.height);const tabWide=contentWide.findOne(n=>n.name==='Tab + line');if(tabWide)tabWide.resize(450,tabWide.height);}
const badgeWide=wide.findOne(n=>n.name==='Artwork on ivory / original colors');if(badgeWide)badgeWide.x=528;
const badgeNarrow=narrow.findOne(n=>n.name==='Artwork on ivory / original colors');if(badgeNarrow){badgeNarrow.x=224;badgeNarrow.resize(72,72);}
const contentNarrow=narrow.findOne(n=>n.name==='Content / Auto Layout');if(contentNarrow){contentNarrow.resize(180,contentNarrow.height);for(const t of contentNarrow.findAllWithCriteria({types:['TEXT']})){await figma.loadFontAsync(t.fontName);t.resize(180,t.height);}}
const social=await figma.getNodeByIdAsync('1299:9');await title(social,'Social templates / ready for your story','Editable campaign copy • Original logo artwork • Square, portrait and story canvases');
const specs=[['Square',1080,1080,'teal','[Post headline]'],['Portrait',1080,1350,'ivory','[Featured topic]'],['Story',1080,1920,'teal','[Story headline]'],['Announcement',1080,1080,'ivory','[Announcement]'],['Education',1080,1350,'ivory','[Learning topic]'],['Launch',1080,1920,'teal','[Campaign headline]']];
const socialMasters=[];
for(let i=0;i<specs.length;i++){const [kind,w,h,bg,headline]=specs[i];const dark=bg==='teal';const c=comp(social,'NH/Social/'+kind,w,h,bg);place(c,120+(i%3)*1300,420+Math.floor(i/3)*2180);c.clipsContent=true;
const top=h===1920?280:72;const content=stack(c,'Content / Auto Layout',936,36);place(content,72,top);
const brandplate=frame(content,'Brand plate',490,110,'ivory');brandplate.cornerRadius=14;inst(brandplate,horizontal,25,8,360);
await tab(content,kind.toUpperCase(),936,dark,24);
await textprop(c,content,'Headline',headline,80,dark?'ivory':'teal',900);
await textprop(c,content,'Description','[Add approved supporting copy]',36,dark?'ivory':'ink',900);
if(kind==='Education'){const card=stack(content,'Lesson points / editable',936,28);card.paddingTop=32;for(const value of ['01   [Learning point]','02   [Learning point]','03   [Learning point]'])await txt(card,value,36,'teal',900);}
else{const card=frame(content,'Artwork panel',936,h===1920?500:280,dark?'ivory':'teal');card.cornerRadius=28;inst(card,mark,(936-190)/2,(card.height-211)/2,190);}
const footer=stack(c,'Footer / Auto Layout',936,16);place(footer,72,h-(h===1920?330:125));line(footer,936);await textprop(c,footer,'Footer','[Campaign label]',24,dark?'ivory':'teal',936);
c.description=kind+' editable template. '+w+'x'+h+' PNG. Text placeholders require approved copy. '+(h===1920?'Keep content outside the top 250 and bottom 300 px as a conservative working inset; verify the destination app preview.':'Keep 72 px inner margins.');
socialMasters.push(c);}
for(const [bg,x]of [['teal',4100],['ivory',4620]]){const c=comp(social,'NH/Social/Profile/'+bg,400,400,bg);place(c,x,420);inst(c,mark,92,80,216);const p=frame(social,'Avatar / circle preview '+bg,400,400,bg);place(p,x,1000);p.cornerRadius=200;p.clipsContent=true;inst(p,c,0,0,400);}
const banners=await figma.getNodeByIdAsync('1299:10');await title(banners,'Covers / one brand, distinct canvases','YouTube • Facebook • LinkedIn company • X • Web campaign hero');
const covers=[['YouTube',2560,1440,{x:508,y:509,w:1544,h:422},'teal'],['Facebook',851,315,{x:145,y:40,w:561,h:220},'ivory'],['LinkedIn Company',1512,256,{x:330,y:24,w:1000,h:208},'ivory'],['X',1500,500,{x:360,y:80,w:1080,h:300},'teal'],['Website Hero',1920,640,{x:240,y:90,w:1440,h:460},'ivory']];
const coverIds=[];let yy=420;
for(const [kind,w,h,safe,bg]of covers){const pair=[];
for(let j=0;j<2;j++){const c=comp(banners,'Content='+(j?'Clean':'Editable')+', Platform='+kind,w,h,bg);c.clipsContent=true;const dark=bg==='teal';
const safeContent=stack(c,'Safe content / Auto Layout',safe.w,Math.max(8,safe.h*.035));place(safeContent,safe.x,safe.y+safe.h*.06);safeContent.counterAxisAlignItems='CENTER';
const plate=frame(safeContent,'Brand plate',Math.min(safe.w*.85,1100),safe.h*.56,'ivory');plate.cornerRadius=safe.h*.04;
const mw=Math.min(plate.width*.9,plate.height*3.75);inst(plate,horizontal,(plate.width-mw)/2,(plate.height-mw/3.75)/2,mw);
if(!j){const size=safe.h<230?24:36;await textprop(c,safeContent,'Headline','[Campaign headline]',size,dark?'ivory':'teal',safe.w*.88);}
line(safeContent,safe.w*.6,'gold',Math.max(2,safe.h*.008));
c.description=kind+' '+w+'x'+h+'. Safe content rectangle '+JSON.stringify(safe)+'. '+(kind==='YouTube'?'1544x422 rounded scaled safe region from official minimum.':kind==='X'?'Avoid top/bottom 60px and profile photo at lower left.':kind==='LinkedIn Company'?'1512x256 from live LinkedIn Help, checked 2026-10-15.':kind==='Facebook'?'851x315 provisional; official help was inaccessible. Safe zone is a design inset, not a verified platform guarantee.':'Safe area is a design recommendation.');
pair.push(c);}
const set=made(figma.combineAsVariants(pair,banners));set.name='NH/Cover/'+kind;place(set,120,yy);set.resize(w*2+160,h+80);pair.forEach((c,i)=>place(c,32+i*(w+64),32));yy+=h+190;coverIds.push(...pair.map(c=>c.id));}
banners.resizeWithoutConstraints(6200,yy+100);
return {createdNodeIds:ids,appSet:appSet.id,appVariants:appVariants.map(c=>c.id),social:socialMasters.map(c=>({id:c.id,name:c.name})),covers:coverIds,componentCount:page.findAllWithCriteria({types:['COMPONENT']}).length};

