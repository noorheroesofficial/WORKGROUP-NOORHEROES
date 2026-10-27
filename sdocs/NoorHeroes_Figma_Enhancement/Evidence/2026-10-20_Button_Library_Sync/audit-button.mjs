export async function audit(figma) {

await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='319:2'));figma.skipInvisibleInstanceChildren=false;
const set=await figma.getNodeByIdAsync('322:99');let assertions=0;const issues=[];function check(ok,name){assertions++;if(!ok)issues.push(name);}
const expected={"type":"GRADIENT_LINEAR","visible":true,"opacity":1,"blendMode":"NORMAL","gradientStops":[{"color":{"r":0.04699999839067459,"g":0.44999998807907104,"b":0.44699999690055847,"a":1},"position":0,"boundVariables":{}},{"color":{"r":0.05999999865889549,"g":0.20000000298023224,"b":0.20000000298023224,"a":1},"position":1,"boundVariables":{}}],"gradientTransform":[[0,1,0],[-1,0,1]]};
check(set.children.length===30,'30existing variants');for(const id of ['Label#322:0','Show icon#322:31','Icon#322:62','Style','Size','State'])check(id in set.componentPropertyDefinitions,'property retained '+id);
let routes=0;for(const n of set.children){const p=n.variantProperties,label=n.findOne(n=>n.type==='TEXT'&&n.name==='Label'),icon=n.findOne(n=>n.type==='INSTANCE'&&n.name==='Icon');
check(n.width===342&&n.height===(p.Size==='Large'?56:48),'dimensions '+n.id);check(n.cornerRadius===18,'radius '+n.id);check(n.itemSpacing===4,'gap '+n.id);check(label.fontName.family==='Poppins'&&label.fontName.style==='SemiBold'&&label.fontSize===14&&label.lineHeight.value===20,'typography '+n.id);check(!!label.componentPropertyReferences.characters,'editable label '+n.id);check(icon.width===18&&icon.height===18,'18px icon '+n.id);
if(p.Style==='Primary'){check(n.fills[0].type==='GRADIENT_LINEAR','primarygradient '+n.id);check(n.fills[0].gradientStops.every((s,i)=>Math.abs(s.color.r-expected.gradientStops[i].color.r)<.00001&&Math.abs(s.color.g-expected.gradientStops[i].color.g)<.00001&&Math.abs(s.color.b-expected.gradientStops[i].color.b)<.00001),'source colors '+n.id);check(!!n.fills[0].gradientStops[0].boundVariables.color,'gradient binding '+n.id);}
if(p.State==='Disabled'){check(Math.abs(n.opacity-.42)<.00001,'disabled42 '+n.id);check(n.reactions.length===0,'disabled noninteractive '+n.id);}if(p.State==='Pressed')check(Math.abs(n.opacity-.88)<.00001,'pressed88 '+n.id);
for(const r of n.reactions)for(const a of r.actions||[])if(a.type==='NODE'){routes++;const dest=await figma.getNodeByIdAsync(a.destinationId);check(!!dest&&dest.parent.id===set.id,'internal state destination '+n.id);check(dest.variantProperties.Style===p.Style&&dest.variantProperties.Size===p.Size,'same style and size '+n.id);}
}
const review=await figma.getNodeByIdAsync('322:142'),instances=review.findAll(n=>n.type==='INSTANCE'&&n.name==='NH/Button');check(instances.length===30,'all30review instances');const clipping=[];
for(const n of instances){const b=n.absoluteBoundingBox,l=n.findOne(x=>x.name==='Label'&&x.type==='TEXT').absoluteBoundingBox;if(l.x<b.x-1||l.y<b.y-1||l.x+l.width>b.x+b.width+1||l.y+l.height>b.y+b.height+1)clipping.push(n.id);}check(!clipping.length,'review label clipping');
return{result:issues.length?'FAIL':'PASS',assertions,issues,publicVariants:set.children.length,reviewInstances:instances.length,stateRoutes:routes,clipping,originalSetID:set.id,propertyIDsPreserved:true,regularHeight:48,largeSize:[342,56]};

}

