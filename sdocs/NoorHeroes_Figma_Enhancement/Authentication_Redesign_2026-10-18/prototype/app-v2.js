const $=s=>document.querySelector(s),all=s=>[...document.querySelectorAll(s)];
const drafts={login:{method:'phone',phone:'',email:'',country:'US'},registration:{method:'phone',phone:'',email:'',country:'US'}};
const state={view:'login',busy:false,scenario:'success',generation:0,cooldown:0,consents:{terms:false,privacy:false,adult:false,child:false},optional:{personalization:false,voice:false,marketing:false}};
const dialog=$('#country-dialog');let lastOperation='identifier',controller,returnFocus,legalCopy;
const feedback=NHFeedback.createSnackbar({render:renderSnackbar});
function renderSnackbar(item,processing){
  const box=$('#snackbar');
  if(!item){if(typeof box.hidePopover==='function'&&box.matches(':popover-open'))box.hidePopover();box.hidden=true;return}
  const host=document.querySelector('dialog[open]')||document.body;
  if(box.parentElement!==host)host.append(box);
  box.dataset.tone=item.tone;box.setAttribute('role',item.tone==='error'?'alert':'status');
  box.setAttribute('aria-live',item.tone==='error'?'assertive':'polite');box.setAttribute('aria-atomic','true');
  $('#snack-text').textContent=item.message;$('#retry').hidden=!item.action;$('#retry').textContent=item.actionLabel;
  $('#retry').disabled=processing;$('#retry').onclick=()=>feedback.activate();$('#snack-close').onclick=()=>feedback.dismiss();
  box.hidden=false;if(typeof box.showPopover==='function'){box.setAttribute('popover','manual');if(!box.matches(':popover-open'))box.showPopover()}
}
for(const sheet of all('dialog'))sheet.addEventListener('close',()=>feedback.refresh());
function snackbarInset(){const v=window.visualViewport;document.documentElement.style.setProperty('--nh-keyboard-inset',Math.max(0,v?innerHeight-v.height-v.offsetTop:0)+'px')}
window.visualViewport?.addEventListener('resize',snackbarInset);window.visualViewport?.addEventListener('scroll',snackbarInset);snackbarInset();
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!$('#snackbar').hidden){event.preventDefault();feedback.dismiss()}});
fetch('approved-copy.json').then(r=>r.json()).then(x=>legalCopy=x);
const draft=()=>drafts[state.view==='registration'?'registration':'login'];
const input=()=>$(draft().method==='phone'?'#phone-input':'#email-input');
const country=()=>COUNTRIES.find(c=>c.iso===draft().country)||COUNTRIES.find(c=>c.iso==='US');
function filteredCountries(q){q=q.trim().toLowerCase();return COUNTRIES.filter(c=>c.name.toLowerCase().includes(q)||c.code.includes(q)||c.iso.toLowerCase()===q)}
function updateCountry(){const c=country();$('#country-flag').src='flags/'+c.iso+'.png';$('#country-code').textContent=c.code;$('#country-open').setAttribute('aria-label','Country code: '+c.name+' '+c.code);state.serverInvalid=false;controls()}
function renderCountries(){const q=$('#country-search').value,rows=filteredCountries(q);$('#search-clear').hidden=!q;$('#result-count').textContent=rows.length+' countries';$('#country-list').replaceChildren();for(const c of rows){const b=document.createElement('button');b.className='country-row';b.type='button';b.setAttribute('role','radio');b.setAttribute('aria-checked',String(c.iso===draft().country));b.dataset.iso=c.iso;const img=new Image();img.src='flags/'+c.iso+'.png';img.alt='';const name=document.createElement('span');name.className='name';name.textContent=c.name;const code=document.createElement('span');code.className='code';code.textContent=c.code;const radio=document.createElement('span');radio.className='radio';radio.textContent=c.iso===draft().country?'✓':'';radio.setAttribute('aria-hidden','true');b.append(img,name,code,radio);b.onclick=()=>{draft().country=c.iso;updateCountry();dialog.close();validate(false)};$('#country-list').append(b)}if(!rows.length){const p=document.createElement('p');p.className='empty';p.textContent='No countries found';$('#country-list').append(p)}}
$('#country-open').onclick=()=>{if(state.busy)return;$('#country-search').value='';renderCountries();dialog.showModal();$('#country-search').focus()};
$('#country-search').oninput=renderCountries;$('#search-clear').onclick=()=>{$('#country-search').value='';renderCountries();$('#country-search').focus()};$('#country-close').onclick=()=>dialog.close();dialog.addEventListener('close',()=>$('#country-open').focus());
$('#country-list').onkeydown=e=>{if(!['ArrowDown','ArrowUp','Home','End'].includes(e.key))return;const rows=all('.country-row'),i=rows.indexOf(document.activeElement);e.preventDefault();rows[e.key==='Home'?0:e.key==='End'?rows.length-1:(i+(e.key==='ArrowDown'?1:-1)+rows.length)%rows.length]?.focus()};
function error(message){$('#validation').textContent=message;$('#validation').hidden=!message;input().setAttribute('aria-invalid',String(!!message));input().closest('.field').classList.toggle('invalid',!!message)}
function validate(show=true){const r=NHAuth.validate(draft().method,input().value,draft().country);if(show||!r.error)error(r.error);return r}
function agreed(){return Object.values(state.consents).every(Boolean)}
function controls(){const blocked=state.busy||Date.now()<state.cooldown;for(const n of all('#auth-form input,#auth-form button,#google,.consent button,.consent input,.optional'))n.disabled=blocked;$('#submit').disabled=blocked||!!NHAuth.validate(draft().method,input().value,draft().country).error||!!state.serverInvalid||(state.view==='registration'&&!agreed());$('#google').disabled=blocked||(state.view==='registration'&&!agreed());$('#consent-check').checked=agreed();for(const b of all('[data-view],.footer-link,.back'))b.disabled=state.busy;$('.back').disabled=state.busy||state.view==='login'}
function busy(on,google=false){state.busy=on;$('#submit').classList.toggle('loading',on&&!google);$('#google').classList.toggle('loading',on&&google);$('#submit').setAttribute('aria-busy',String(on&&!google));$('#google').setAttribute('aria-busy',String(on&&google));$('#processing-status').textContent=on?'Processing…':'';controls()}
function snack(result){const operation=lastOperation;feedback.show({message:result.message,tone:result.tone||'error',key:operation+'|'+result.message,actionLabel:result.retry?'Retry':'',action:result.retry?()=>run(operation):null})}
function view(name){if(state.busy)return;state.view=name;$('#login').hidden=name==='language';$('#language').hidden=name!=='language';feedback.clear();if(name==='language')return;const reg=name==='registration';$('#login-title').textContent=reg?'Create your account':'Welcome back';$('.panel header p').textContent=reg?'Join as a parent to set up your family':'Continue with your parent account';$('#submit .button-label').textContent=reg?'Create Account':'Send code';$('.consent').hidden=!reg;$('#account-copy').textContent=reg?'Already have an account?':"Don't have an account?";$('#account-link').textContent=reg?'Log in':'Create an account?';$('#phone-input').value=draft().phone;$('#email-input').value=draft().email;method(draft().method);controls()}
function method(m){draft().method=m;state.serverInvalid=false;all('[data-method]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.method===m)));$('#phone-group').hidden=m!=='phone';$('#email-group').hidden=m!=='email';all('#auth-form input').forEach(i=>{i.setAttribute('aria-invalid','false');i.closest('.field')?.classList.remove('invalid')});$('#validation').hidden=true;updateCountry();controls()}
all('[data-method]').forEach(b=>b.onclick=()=>{if(!state.busy)method(b.dataset.method)});
for(const i of all('#phone-input,#email-input')){i.oninput=()=>{state.serverInvalid=false;draft()[i.id==='phone-input'?'phone':'email']=i.value;validate(true);controls()};i.onblur=()=>{const r=validate(true);if(!r.error&&draft().method==='email'){i.value=r.value;draft().email=r.value}controls()};i.onfocus=()=>i.scrollIntoView({block:'nearest',behavior:'auto'})}
async function run(operation='identifier'){
  if(state.busy||Date.now()<state.cooldown)return;
  if(state.view==='registration'&&!agreed()){openLegal('terms');return}
  const valid=operation==='google'?{value:''}:validate(true);if(valid.error){input().focus();return}
  lastOperation=operation;const generation=++state.generation;controller=new AbortController();feedback.clear();busy(true,operation==='google');
  const result=await NHAuth.request({method:operation==='google'?'google':draft().method,value:valid.value,country:draft().country,scenario:state.scenario,consents:{...state.consents},optional:{...state.optional}},fetch,3000,controller.signal);
  if(generation!==state.generation)return;busy(false);
  if(result.kind==='inline'){state.serverInvalid=true;error(result.message);controls();input().focus()}
  else if(result.kind==='snackbar'){if(result.retryAfter){state.cooldown=Date.now()+result.retryAfter;controls()}snack(result)}
  else if(result.kind==='success')$('#review-result').textContent='Mock request succeeded. OTP destination is pending approval.';
}
$('#auth-form').onsubmit=e=>{e.preventDefault();run()};$('#google').onclick=()=>run('google');$('#account-link').onclick=()=>view(state.view==='registration'?'login':'registration');
all('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));$('.back').onclick=()=>{if(state.view==='registration')view('login')};
$('#scenario').onchange=e=>{state.scenario=e.target.value;$('#review-result').textContent='Controlled mock: '+state.scenario};
setInterval(()=>{if(state.cooldown&&Date.now()>=state.cooldown){state.cooldown=0;controls();$('#review-result').textContent='Rate limit expired; you may retry.'}},200);
window.addEventListener('pagehide',()=>{controller?.abort();state.generation++});
window.addEventListener('pageshow',e=>{if(e.persisted)busy(false)});
window.addEventListener('offline',()=>snack(NHAuth.mapFailure(0)));
const legal=$('#legal-dialog');let stage='terms';
function row(label,key,group){const el=document.createElement('label');el.className='check-row';const c=document.createElement('input');c.type='checkbox';c.checked=state[group][key];c.onchange=()=>{state[group][key]=c.checked;$('#legal-agree').disabled=stage==='terms'?!state.consents.adult:stage==='privacy'?!state.consents.child:false};el.append(c,document.createTextNode(label));return el}
function openLegal(next){if(state.busy)return;stage=next;returnFocus=document.activeElement;$('#legal-title').textContent=next==='terms'?'Terms and Conditions':next==='privacy'?'Privacy Policy':'Optional preferences';const body=$('#legal-content');body.replaceChildren();if(next==='optional'){for(const [key,label]of [['personalization','Personalization/AI consent'],['voice','Voice-feature consent'],['marketing','Marketing consent']])body.append(row(label,key,'optional'))}else{const note=document.createElement('p');note.textContent='Draft prototype content · requires legal review before production.';body.append(note);const source=legalCopy?.find(x=>x.id===(next==='terms'?'1513:363':'1513:401'));for(const item of source?.text||[]){const p=document.createElement(/^\d\./.test(item.text)?'h3':'p');p.textContent=item.text;body.append(p)}body.append(next==='terms'?row('I confirm I am 18 years or older','adult','consents'):row('Child-data-processing consent','child','consents'))}$('#legal-agree').textContent=next==='terms'?'I Agree & Continue':next==='privacy'?'Acknowledge & Continue':'Done';$('#legal-agree').disabled=next==='terms'?!state.consents.adult:next==='privacy'?!state.consents.child:false;if(!legal.open)legal.showModal();body.scrollTop=0}
$('#legal-agree').onclick=()=>{if(stage==='terms'){state.consents.terms=true;legal.close();requestAnimationFrame(()=>openLegal('privacy'))}else{if(stage==='privacy')state.consents.privacy=true;legal.close();controls()}};
$('#legal-close').onclick=()=>legal.close();legal.addEventListener('close',()=>{controls();returnFocus?.focus()});
$('#consent-check').onclick=e=>{e.preventDefault();if(agreed()){state.consents={terms:false,privacy:false,adult:false,child:false};controls()}else openLegal('terms')};$('#terms-open').onclick=()=>openLegal('terms');$('#privacy-open').onclick=()=>openLegal(state.consents.terms?'privacy':'terms');$('.optional').onclick=()=>openLegal('optional');
const langs=[['en','English','English','GB'],['hi','Hindi','हिंदी','IN'],['ar','Arabic','العربية','SA'],['ur','Urdu','اردو','PK']];
let language=localStorage.getItem('nh-language')||'en';
function renderLanguages(){const box=$('#languages');box.setAttribute('role','radiogroup');box.setAttribute('aria-label','Language');box.replaceChildren();for(const [id,name,native,flag]of langs){const b=document.createElement('button');b.className='language-row';b.setAttribute('role','radio');b.setAttribute('aria-checked',String(language===id));b.innerHTML='<img src="flags/'+flag+'.png" alt=""><span>'+name+'<small lang="'+id+'" dir="auto">'+native+'</small></span>'+(language===id?'<i class="language-check" aria-hidden="true">✓</i>':'');b.onclick=()=>{language=id;localStorage.setItem('nh-language',id);renderLanguages()};box.append(b)}}
$('#language-continue').onclick=()=>{const b=$('#language-continue');if(b.disabled)return;b.disabled=true;b.classList.add('loading');b.innerHTML='<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>';setTimeout(()=>{location.href='https://www.figma.com/proto/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?page-id=928%3A2&node-id=1215-34'},1800)};
$('#text-scale').onchange=e=>{document.documentElement.style.fontSize=e.target.value+'px';document.documentElement.dataset.scale=e.target.value};
$('#direction').onclick=e=>{const on=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(on));document.body.dir=on?'rtl':'ltr'};
$('#reduce-motion').onclick=e=>{const on=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(on));document.documentElement.dataset.motion=on?'reduced':'full'};
window.NHReview={state,drafts,filteredCountries,run,view,validate};view('login');renderLanguages();

