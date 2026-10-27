const {test}=require('node:test');
const assert=require('node:assert/strict');
const {validate,mapFailure,request}=require('./auth-core.cjs');
test('required, trimmed email, correction and invalid email',()=>{
  assert.equal(validate('email','  ').error,'Enter your email address.');
  assert.ok(validate('email','a@').error);
  assert.equal(validate('email','  parent@example.com  ').value,'parent@example.com');
});
test('country-aware national and international numbers',()=>{
  for(const [iso,value] of [['US','2015550123'],['GB','07911123456'],['IN','9876543210'],['AU','0412345678'],['US','+1 416 555 0123']]) assert.equal(validate('phone',value,iso).error,'',iso);
  for(const value of ['','123','12345678901234567890','201CALL1234','++12015550123']) assert.ok(validate('phone',value,'US').error,value);
  assert.ok(validate('phone','+44 7911 123456','US').error);
  assert.equal(validate('phone','２０１５５５０１２３','US').value,'+12015550123');
});
test('only identified field errors inline; raw messages never exposed',()=>{
  const body={error:{message:'SECRET stack',details:{identifier:'SECRET invalid'}}};
  assert.equal(mapFailure(422,body,'phone').kind,'inline');
  assert.equal(mapFailure(422,body,'google').kind,'snackbar');
  assert.equal(mapFailure(422,{error:{details:{consent:'invalid'}}},'phone').kind,'snackbar');
  for(const status of [401,403,409,500,503]) assert.ok(!mapFailure(status,body,'email').message.includes('SECRET'));
  assert.equal(mapFailure(429,{},'email','15').retryAfter,15000);
  assert.equal(mapFailure(429,{},'email').retry,false);
});
test('actual HTTP response mapping and network/timeout recovery',async()=>{
  const response=await request({method:'email',value:'parent@example.com',scenario:'500'},async()=>new Response(JSON.stringify({error:{message:'SECRET'}}),{status:500}));
  assert.equal(response.kind,'snackbar');
  assert.match((await request({},async()=>{throw new TypeError('failed')})).message,/Unable to connect/);
  assert.match((await request({},(_,o)=>new Promise((resolve,reject)=>o.signal.addEventListener('abort',()=>reject(new DOMException('timeout','AbortError')))),10)).message,/timed out/);
  assert.equal((await request({},async()=>new Response('{}',{status:200}))).kind,'success');
});
