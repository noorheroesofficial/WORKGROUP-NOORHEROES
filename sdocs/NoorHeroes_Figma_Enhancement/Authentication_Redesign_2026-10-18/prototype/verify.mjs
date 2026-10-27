import fs from 'node:fs';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const base=new URL('./',import.meta.url);
const read=name=>fs.readFileSync(new URL(name,base),'utf8');
const countries=JSON.parse(read('countries.json'));
const metadata=JSON.parse(read('metadata.min.json'));
assert.equal(countries.length,Object.keys(metadata.countries).length);
assert.equal(new Set(countries.map(c=>c.iso)).size,countries.length);
for(const c of countries){
  assert.equal(c.code,'+'+metadata.countries[c.iso][0]);
  assert.ok(c.name.length>0);
  const flag=fs.readFileSync(new URL('flags/'+c.iso+'.png',base));
  assert.equal(flag.subarray(1,4).toString(),'PNG');
  assert.equal(flag.readUInt32BE(16),84);
  assert.equal(flag.readUInt32BE(20),63);
}
const assets=['logo.png','monogram.png','Poppins-Regular.ttf','Poppins-SemiBold.ttf'].map(file=>({file,bytes:fs.statSync(new URL(file,base)).size}));
assert.ok(assets.every(a=>a.bytes>0));
const result={result:'PASS',countries:countries.length,uniqueISO:countries.length,dialCodesMatchPinnedMetadata:true,flagAssets:countries.length,flagResolution:'84x63',assets};
fs.writeFileSync(new URL('../evidence/data-validation.json',base),JSON.stringify(result,null,2));
console.log(JSON.stringify(result));
