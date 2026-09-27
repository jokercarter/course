import http from 'node:http';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readFile,realpath,stat} from 'node:fs/promises';
import {createReadStream} from 'node:fs';

const root=path.dirname(fileURLToPath(import.meta.url));
const materials=path.dirname(root);
const courses=new Set(['EECS 376','EECS 453','EECS 492','MATH 465']);
const sources=JSON.parse(await readFile(path.join(root,'data/sources.json'),'utf8'));
const sourceMap=new Map(sources.map(s=>[s.id,s]));
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf','.pdf':'application/pdf','.tex':'text/plain; charset=utf-8','.md':'text/plain; charset=utf-8','.ipynb':'application/json; charset=utf-8'};
const port=Number(process.env.PORT||3760);
if(!Number.isInteger(port)||port<1||port>65535)throw Error('Invalid PORT');
const inside=(base,file)=>{const r=path.relative(base,file);return r!==''&&!r.startsWith('..'+path.sep)&&r!=='..'&&!path.isAbsolute(r);};
async function serve(req,res){
 res.setHeader('X-Content-Type-Options','nosniff');
 res.setHeader('Referrer-Policy','no-referrer');
 res.setHeader('Cache-Control','no-cache');
 const fail=(code,message)=>{res.writeHead(code,{'Content-Type':'text/plain; charset=utf-8'});res.end(message);};
 if(!['GET','HEAD'].includes(req.method))return fail(405,'Method not allowed');
 if(![`127.0.0.1:${port}`,`localhost:${port}`].includes(req.headers.host))return fail(403,'Local host only');
 let url;
 try{url=new URL(req.url,`http://127.0.0.1:${port}`);}catch{return fail(400,'Invalid URL');}
 if(url.pathname==='/api/health'){res.setHeader('Content-Type',mime['.json']);return res.end(JSON.stringify({app:'course-study-desk',version:1}));}
 let file,base,source;
 try{
  const pathname=decodeURIComponent(url.pathname);
  if(pathname.startsWith('/api/resources/')){
   source=sourceMap.get(pathname.slice('/api/resources/'.length));
   if(!source||!courses.has(source.course))return fail(404,'资料未登记');
   base=await realpath(path.join(materials,source.course));
   file=await realpath(path.resolve(materials,source.path));
   if(!inside(base,file)||!['.pdf','.tex','.md','.ipynb'].includes(path.extname(file)))return fail(403,'Forbidden');
  }else{
   const clean=pathname==='/'?'index.html':pathname.slice(1);
   if(clean.includes('\\')||clean.split('/').some(p=>p==='..'||p.startsWith('.')))return fail(403,'Forbidden');
   const allowed=['index.html','app.js','styles.css','dark.css','assets/favicon.svg'];
   if(clean.startsWith('vendor/katex/')){base=await realpath(path.join(root,'node_modules/katex/dist'));file=await realpath(path.join(base,clean.slice('vendor/katex/'.length)));}
   else if(allowed.includes(clean)||/^data\/[a-z0-9-]+\.(js|json)$/.test(clean)){base=await realpath(root);file=await realpath(path.join(root,clean));}
   else return fail(404,'Not found');
   if(!inside(base,file))return fail(403,'Forbidden');
  }
  const info=await stat(file);
  if(!info.isFile())return fail(404,'Not found');
  const ext=path.extname(file);
  res.setHeader('Content-Type',mime[ext]||'application/octet-stream');
  if(source)res.setHeader('Content-Disposition',`${ext==='.ipynb'?'attachment':'inline'}; filename*=UTF-8''${encodeURIComponent(source.name)}`);
  if(ext==='.html')res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'");
  res.setHeader('Accept-Ranges','bytes');
  let start=0,end=info.size-1,status=200;
  if(req.headers.range){
   const m=/^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
   if(!m||(!m[1]&&!m[2]))return fail(416,'Invalid range');
   if(!m[1])start=Math.max(0,info.size-Number(m[2]));
   else{start=Number(m[1]);if(m[2])end=Math.min(end,Number(m[2]));}
   if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||start>end||start>=info.size){res.setHeader('Content-Range',`bytes */${info.size}`);return fail(416,'Range not satisfiable');}
   res.setHeader('Content-Range',`bytes ${start}-${end}/${info.size}`);status=206;
  }
  res.setHeader('Content-Length',Math.max(0,end-start+1));res.writeHead(status);
  if(req.method==='HEAD'||info.size===0)return res.end();
  const stream=createReadStream(file,{start,end});stream.on('error',()=>res.destroy());res.on('close',()=>stream.destroy());stream.pipe(res);
 }catch(error){if(!res.headersSent)fail(error.code==='ENOENT'?404:400,'文件不可用，请检查原课程文件夹是否仍在原位置。');else res.destroy();}
}
const server=http.createServer((req,res)=>{serve(req,res).catch(()=>{if(!res.headersSent)res.writeHead(500);res.end('Local server error');});});
server.on('error',error=>{console.error(error.code==='EADDRINUSE'?`Port ${port} is already in use. Open http://127.0.0.1:${port} or set PORT.`:error.message);process.exitCode=1;});
server.listen(port,'127.0.0.1',()=>console.log(`Study Desk: http://127.0.0.1:${port}\nLocal only. Press Ctrl+C to stop.`));
