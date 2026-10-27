(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory(require('libphonenumber-js/max'),require('validator'));else root.NHAuth=factory(root.libphonenumber,root.validator)})(typeof globalThis!=='undefined'?globalThis:this,function(phone,email){
  function validate(method,raw,iso='US'){
    const value=String(raw??'').trim();
    if(!value)return {error:method==='email'?'Enter your email address.':'Enter your phone number.'};
    if(method==='email')return email.isEmail(value,{require_tld:true,allow_utf8_local_part:true})?{error:'',value}:{error:'Enter a valid email address.'};
    const normalized=value.replace(/[\uFF10-\uFF19\u0660-\u0669\u06F0-\u06F9]/g,c=>String(c.charCodeAt(0)-(c>='０'?'０'.charCodeAt(0):c>='۰'?'۰'.charCodeAt(0):'٠'.charCodeAt(0))));
    if(!/^\+?[\d\s().-]+$/.test(normalized))return {error:'Use digits and a valid phone number.'};
    try{
      const parsed=phone.parsePhoneNumberFromString(normalized,{defaultCountry:iso,extract:false});
      if(normalized.startsWith('+')&&parsed&&parsed.countryCallingCode!==phone.getCountryCallingCode(iso))return {error:'Select the matching country calling code.'};
      const length=phone.validatePhoneNumberLength(normalized,iso);
      if(length==='TOO_SHORT')return {error:'Enter the remaining phone number digits.'};
      if(length==='TOO_LONG')return {error:'This phone number has too many digits.'};
      return parsed?.isValid()?{error:'',value:parsed.number}:{error:'Enter a valid phone number for this country.'};
    }catch{return {error:'Select a country and enter a valid phone number.'};}
  }
  function mapFailure(status,body={},method='phone',retryAfter=null){
    const details=body?.error?.details;
    const fields=['identifier',method,method==='phone'?'phone_number':'email_address'];
    if(status===422&&['phone','email'].includes(method)&&details&&Object.keys(details).some(k=>fields.some(f=>k===f||k.endsWith('.'+f))))return {kind:'inline',message:method==='email'?'Check your email address and try again.':'Check your phone number and try again.',retry:false};
    if(status===429){const seconds=Number(retryAfter);const date=Date.parse(retryAfter);return {kind:'snackbar',message:'Too many attempts. Please try again later.',retry:false,retryAfter:Math.max(1000,Number.isFinite(seconds)&&seconds>0?seconds*1000:Number.isFinite(date)?date-Date.now():30000)};}
    if(status===0)return {kind:'snackbar',message:'Unable to connect. Check your internet connection.',retry:true};
    if(status===408)return {kind:'snackbar',message:'Request timed out. Please try again.',retry:true};
    return {kind:'snackbar',message:status>=500?'Something went wrong. Please try again.':'Unable to continue. Please try again.',retry:status>=500};
  }
  async function request(payload,transport=fetch,timeout=10000,signal){
    const controller=new AbortController(),abort=()=>controller.abort();
    signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)controller.abort();
    const timer=setTimeout(()=>controller.abort(),timeout);
    try{
      const r=await transport('/mock/auth-flow',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:controller.signal});
      const body=await r.json().catch(()=>({}));
      return r.ok?{kind:'success'}:mapFailure(r.status,body,payload.method,r.headers.get('Retry-After'));
    }catch(e){return signal?.aborted?{kind:'cancelled'}:mapFailure(e.name==='AbortError'?408:0);}
    finally{clearTimeout(timer);signal?.removeEventListener('abort',abort);}
  }
  return {validate,mapFailure,request};
});
