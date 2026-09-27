import assert from 'node:assert/strict';
import {readFile,stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import katex from 'katex';
import {courses} from '../data/courses.js';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const sources=JSON.parse(await readFile(path.join(root,'data/sources.json'),'utf8'));
let examples=0,quiz=0,formulas=0,refs=0;
const ids=new Set();
for(const course of courses){
 assert(course.lessons.length>=7,`${course.code}: insufficient coverage`);
 for(const lesson of course.lessons){
  const key=course.id+'/'+lesson.id;assert(!ids.has(key));ids.add(key);
  assert(lesson.examples.length>=2,key+' missing examples');assert(lesson.quiz.length>=3,key+' missing quizzes');
  assert(lesson.goals.length>=2&&lesson.concepts.length>=3&&lesson.pitfalls.length>=2,key+' missing explanation');
  assert(lesson.proof.length>50&&lesson.prereq.length>0,key+' missing derivation');
  assert(!JSON.stringify(lesson).includes('\ufffd'),key+' encoding problem');
  for(const e of lesson.examples)assert(e.steps.length>=3,key+' missing worked steps');
  for(const q of lesson.quiz)assert(q.q&&q.hint&&q.a,key+' missing self check');
  for(const f of lesson.formulas){katex.renderToString(f.tex,{throwOnError:true,strict:'error',trust:false});formulas++;}
  for(const ref of [...lesson.sources,course.outlineSource]){
   const source=sources.find(s=>s.path===ref.file||s.aliases.includes(ref.file));
   assert(source,key+': unknown source '+ref.file);assert(ref.from>=1&&ref.to>=ref.from&&ref.to<=source.pages,key+': invalid page range');refs++;
  }
  examples+=lesson.examples.length;quiz+=lesson.quiz.length;
 }
}
for(const source of sources){assert(/^[a-f0-9]{16}$/.test(source.id));assert((await stat(path.join(root,'..',source.path))).isFile());}
// Check hand-computed examples independently of UI rendering.
const choose=(n,k)=>{let a=1;for(let i=1;i<=k;i++)a=a*(n-i+1)/i;return a;};
assert.equal(choose(9,2),36);assert.equal(choose(8,4),70);
assert.equal(choose(4,2),6);assert.equal(10**4-9**4,3439);
const countNoAdjacent=n=>Array.from({length:2**n},(_,i)=>i).filter(i=>!(i&(i>>1))).length;
assert.equal(countNoAdjacent(4),8);
assert.equal((5*5*3+1)*6,456);assert.equal((3*3*3+1)*8,224);
assert(Math.abs(2+0.5*(1+0.9*4-2)-3.3)<1e-12);
const H=p=>p===0||p===1?0:-p*Math.log2(p)-(1-p)*Math.log2(1-p);
assert(Math.abs((1-H(.75))-.1887218755)<1e-8);
console.log(`PASS: ${courses.length} courses, ${ids.size} lessons, ${examples} examples, ${quiz} quizzes, ${formulas} formulas, ${refs} source/page checks, ${sources.length} existing resources.`);

if(process.argv.includes('--http')){
 const base='http://127.0.0.1:3760';
 for(const route of ['/','/app.js','/styles.css','/data/courses.js','/vendor/katex/katex.min.css','/vendor/katex/katex.min.js','/vendor/katex/fonts/KaTeX_Main-Regular.woff2']){const r=await fetch(base+route);assert.equal(r.status,200,route);}
 const r=await fetch(base+'/api/resources/'+sources.find(s=>s.name.endsWith('.pdf')).id,{headers:{Range:'bytes=0-7'}});assert.equal(r.status,206);assert((await r.text()).startsWith('%PDF-'));
 for(const route of ['/server.mjs','/package.json','/api/resources/unknown','/data/..%5cserver.mjs','/api/resources/../../server.mjs','/vendor/katex/..%5c..%5cpackage.json']){const r=await fetch(base+route);assert([400,403,404].includes(r.status),route+' should be blocked');}
 assert.equal((await fetch(base+'/',{method:'POST'})).status,405);
 assert.equal((await fetch(base+'/api/resources/'+sources.find(s=>s.pages).id,{headers:{Range:'bytes=99999999999-'}})).status,416);
 console.log('PASS: local HTTP, assets, PDF byte ranges, restricted routes, unsupported methods.');
}
