// Loopback-only controlled prototype. Never proxies requests to production.
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=__dirname;
const mime={'.html':'text/html','.js':'text/javascript','.cjs':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.ttf':'font/ttf'};
const server=http.createServer(async(req,res)=>{
  if(req.url==='/mock/auth-flow'&&req.method==='POST'){
    let raw='';for await(const chunk of req){raw+=chunk;if(raw.length>8192){res.writeHead(413).end();return;}}
    let p;try{p=JSON.parse(raw);}catch{res.writeHead(400).end();return;}
    if(p.scenario==='network'){req.socket.destroy();return;}
    if(p.scenario==='timeout'){const t=setTimeout(()=>res.writeHead(408).end('{}'),15000);res.on('close',()=>clearTimeout(t));return;}
    const statuses={success:200,'500':500,'503':503,'429':429,'422':422,'422-global':422,'401':401,'403':403};
    const status=statuses[p.scenario]??500;
    const t=setTimeout(()=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store',...(status===429?{'Retry-After':'3'}:{})});res.end(JSON.stringify(status===200?{mock:true}:{error:{code:'CONTROLLED_MOCK',message:'Never show raw server details',requestId:'fictional-review',details:p.scenario==='422'?{identifier:'Controlled field failure'}:p.scenario==='422-global'?{consent:'Controlled failure'}:null}}));},700);
    res.on('close',()=>clearTimeout(t));return;
  }
  if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405).end();return;}
  let file;try{file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));}catch{res.writeHead(400).end();return;}
  if(file===root)file=path.join(root,'index.html');
  if(!file.startsWith(root+path.sep)||file.includes(path.sep+'node_modules'+path.sep)||file.endsWith('server.cjs')){res.writeHead(403).end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404).end();return;}res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});res.end(req.method==='HEAD'?undefined:data);});
});
server.listen(Number(process.env.NH_REVIEW_PORT||8766),'127.0.0.1',()=>console.log('NoorHeroes controlled review: http://127.0.0.1:'+server.address().port));
