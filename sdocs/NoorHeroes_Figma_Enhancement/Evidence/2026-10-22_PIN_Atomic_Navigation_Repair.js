
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync("928:2"));figma.skipInvisibleInstanceChildren=false;
const variables=await figma.variables.getLocalVariablesAsync();const vars=variables.filter(v=>v.variableCollectionId==="VariableCollectionId:1650:466");const by=Object.fromEntries(vars.map(v=>[v.name,v.id]));
const id=n=>by[n];const val=(v)=>({type:typeof v==="boolean"?"BOOLEAN":typeof v==="number"?"FLOAT":"STRING",resolvedType:typeof v==="boolean"?"BOOLEAN":typeof v==="number"?"FLOAT":"STRING",value:v});
const ref=(name)=>{const v=variables.find(v=>v.id===id(name));return {type:"VARIABLE_ALIAS",resolvedType:v.resolvedType,value:{type:"VARIABLE_ALIAS",id:v.id}}};
const ext=(id,type)=>({type:"VARIABLE_ALIAS",resolvedType:type,value:{type:"VARIABLE_ALIAS",id}});
const exp=(fn,args,type="BOOLEAN")=>({type:"EXPRESSION",resolvedType:type,value:{expressionFunction:fn,expressionArguments:args}});
const eq=(a,b)=>exp("EQUALS",[a,b]);const and=(...x)=>x.reduce((a,b)=>exp("AND",[a,b]));const not=a=>eq(a,val(false));const truth=a=>eq(a,val(true));
const set=(name,value)=>({type:"SET_VARIABLE",variableId:id(name),variableValue:value&&typeof value==="object"?value:val(value)});
const setid=(id,value)=>({type:"SET_VARIABLE",variableId:id,variableValue:val(value)});
const nav=(destinationId,navigation="NAVIGATE")=>({type:"NODE",destinationId,navigation,transition:{type:"DISSOLVE",duration:.2,easing:{type:"EASE_OUT"}},resetScrollPosition:false,resetInteractiveComponents:false});
const branch=(condition,actions)=>({type:"CONDITIONAL",conditionalBlocks:[{condition,actions}]});
const idle=and(not(ref("Busy")),not(ref("Saved")));
const readySet=and(idle,eq(ref("Stage"),val("set")),exp("GREATER_THAN_OR_EQUAL",[ref("SetCount"),val(4)]),exp("LESS_THAN_OR_EQUAL",[ref("SetCount"),val(6)]));
const readyConfirm=and(idle,eq(ref("Stage"),val("confirm")),eq(ref("ConfirmCount"),ref("Length")));
function masks(){const a=[set("ConfirmationFlow/Idle",not(ref("Busy")))];for(let i=0;i<6;i++){a.push(set("ConfirmationFlow/SetFilled"+i,exp("GREATER_THAN",[ref("SetCount"),val(i)])),set("ConfirmationFlow/ConfirmFilled"+i,exp("GREATER_THAN",[ref("ConfirmCount"),val(i)])),set("ConfirmationFlow/ConfirmVisible"+i,exp("GREATER_THAN",[ref("Length"),val(i)])));}return a;}
const states=()=>[
{type:"CONDITIONAL",conditionalBlocks:[{condition:readySet,actions:[set("ActionState","Default")]},{actions:[set("ActionState","Disabled")]}]},
{type:"CONDITIONAL",conditionalBlocks:[{condition:readyConfirm,actions:[set("ConfirmationFlow/ConfirmState","Default")]},{actions:[set("ConfirmationFlow/ConfirmState","Disabled")]}]}
];
const feedback=[set("ErrorVisible",false),set("Message","")];
const enter=(stage,del=false)=>{const name=stage==="set"?"SetCount":"ConfirmCount";const bound=stage==="set"?val(6):ref("Length");const cond=and(idle,eq(ref("Stage"),val(stage)),exp(del?"GREATER_THAN":"LESS_THAN",[ref(name),del?val(0):bound]));return [branch(cond,[set(name,exp(del?"SUBTRACTION":"ADDITION",[ref(name),val(1)],"FLOAT")),...feedback]),...masks(),...states()];};
const continueActions=[branch(readySet,[set("Length",ref("SetCount")),set("ConfirmCount",0),set("Stage","confirm"),...feedback,set("ConfirmationFlow/ConfirmState","Disabled"),...masks(),nav("1709:675")])];
const save=(navigation="OVERLAY")=>[
{condition:and(readyConfirm,not(ref("Match"))),actions:[set("ConfirmCount",0),set("ErrorVisible",true),set("Message","PINs don’t match. Please try again."),set("ConfirmationFlow/ConfirmState","Disabled"),...masks()]},
{condition:and(readyConfirm,truth(ref("Match"))),actions:[set("Busy",true),set("Phase","Start"),...feedback,set("ConfirmationFlow/Idle",false),set("ActionState","Disabled"),set("ConfirmationFlow/ConfirmState","Disabled"),nav("1650:844",navigation)]}
].map(b=>branch(b.condition,b.actions));
const roots=["1650:502","1709:675"];const allTargets=[["1718:715","1718:717","1718:719","1718:727","1718:729","1718:731","1718:739","1718:741","1718:743","1718:749","1718:751"],["1718:759","1718:761","1718:763","1718:771","1718:773","1718:775","1718:783","1718:785","1718:787","1718:792","1718:794"]];
const mutated=[];const old={};
async function write(n,reactions){old[n.id]=n.reactions;await n.setReactionsAsync(reactions);mutated.push(n.id);}
for(let s=0;s<2;s++){for(let k=0;k<11;k++){const n=await figma.getNodeByIdAsync(allTargets[s][k]);n.fills=[{type:"SOLID",color:{r:1,g:1,b:1},opacity:.001}];await write(n,[{trigger:{type:"ON_CLICK"},actions:enter(s===0?"set":"confirm",k===10)}]);}
const n=await figma.getNodeByIdAsync(roots[s]);const reactions=n.reactions.map(r=>{if(r.trigger?.type!=="ON_KEY_DOWN")return {trigger:r.trigger,actions:r.actions};const k=r.trigger.keyCodes?.[0];if(k>=48&&k<=57||k>=96&&k<=105)return {trigger:r.trigger,actions:enter(s===0?"set":"confirm")};if(k===8||k===46)return {trigger:r.trigger,actions:enter(s===0?"set":"confirm",true)};if(k===13)return {trigger:r.trigger,actions:s===0?continueActions:save()};return {trigger:r.trigger,actions:r.actions};});await write(n,reactions);
}
for(const [nid,acts] of [["1718:803",continueActions],["1718:811",save()],["I1650:847;1420:20",save("SWAP")]]){const n=await figma.getNodeByIdAsync(nid);if(nid.startsWith("1718"))n.fills=[{type:"SOLID",color:{r:1,g:1,b:1},opacity:.001}];await write(n,[{trigger:{type:"ON_CLICK"},actions:acts}]);}
const outcome=(s)=>and(truth(ref("Busy")),eq(ref("Outcome"),val(s)));
const success=[set("Busy",false),set("Saved",true),set("SetCount",0),set("ConfirmCount",0),...feedback,...masks(),set("ActionState","Disabled"),set("ConfirmationFlow/ConfirmState","Disabled"),setid("VariableID:1670:1065",false),setid("VariableID:1670:1064",false),setid("VariableID:1670:1068","offered")];
const error=(m)=>[set("Busy",false),set("Message",m),set("ErrorVisible",false),...masks(),set("ActionState","Disabled"),set("ConfirmationFlow/ConfirmState","Default"),nav("1650:846","SWAP")];
await write(await figma.getNodeByIdAsync("1650:844"),[{trigger:{type:"AFTER_TIMEOUT",timeout:2},actions:[
{condition:and(outcome("success"),truth(ext("VariableID:1670:1063","BOOLEAN"))),actions:[...success,nav("1670:1069","SWAP")]},
{condition:and(outcome("success"),not(ext("VariableID:1670:1063","BOOLEAN"))),actions:[...success,{type:"CLOSE"}]},
{condition:outcome("offline"),actions:error("No internet connection. Reconnect and try again.")},
{condition:outcome("api"),actions:error("Something went wrong. Please try again.")},
{condition:outcome("timeout"),actions:[nav("1650:845","SWAP")]}
].map(b=>branch(b.condition,b.actions))}]);
await write(await figma.getNodeByIdAsync("1650:845"),[{trigger:{type:"AFTER_TIMEOUT",timeout:8},actions:[branch(truth(ref("Busy")),error("Something went wrong. Please try again."))]}]);
return {mutatedNodeIds:mutated,handlerSummary:{continueTopLevel:continueActions.length,saveTopLevel:save().length,keypadTopLevel:enter("set").length},preservedScreens:(await figma.getNodeByIdAsync("1650:465")).children.filter(n=>n.type==="FRAME"&&n.width===390&&n.height===844).map(n=>n.id)};

