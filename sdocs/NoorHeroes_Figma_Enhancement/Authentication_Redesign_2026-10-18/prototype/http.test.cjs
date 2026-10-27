const {test}=require('node:test'),assert=require('node:assert/strict');
const {request}=require('./auth-core.cjs');
const transport=(url,options)=>fetch('http://127.0.0.1:8766'+url,options);
test('controlled HTTP server returns expected status and safe UI mapping',async()=>{
  for(const scenario of ['500','503','401','403','422-global']){
    const r=await fetch('http://127.0.0.1:8766/mock/auth-flow',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenario})});
    assert.equal(r.status,scenario==='422-global'?422:Number(scenario));
    const ui=await request({scenario,method:'email'},transport);
    assert.equal(ui.kind,'snackbar');assert.ok(!ui.message.includes('server details'));
  }
  const field=await request({scenario:'422',method:'email'},transport);
  assert.equal(field.kind,'inline');
  const rate=await request({scenario:'429',method:'email'},transport);
  assert.equal(rate.retryAfter,3000);assert.equal(rate.retry,false);
  assert.equal((await request({scenario:'success'},transport)).kind,'success');
  assert.match((await request({scenario:'network'},transport)).message,/Unable to connect/);
  assert.match((await request({scenario:'timeout'},transport,50)).message,/timed out/);
});
