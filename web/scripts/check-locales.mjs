import assert from 'node:assert/strict';
import katex from 'katex';
import {courses} from '../data/courses.js';
import {localizedCourses} from '../data/localization.js';
const english=localizedCourses(courses,'en');
let count=0;
for(let i=0;i<courses.length;i++){
 const zh=courses[i],en=english[i];assert.equal(zh.id,en.id);
 for(let j=0;j<zh.lessons.length;j++){
  const a=zh.lessons[j],b=en.lessons[j];assert.equal(a.id,b.id);assert.equal(a.title.length>0,true);
  for(const field of ['goals','concepts','formulas','examples','quiz','pitfalls'])assert.equal(a[field].length,b[field].length,`${a.id}/${field}`);
  assert.deepEqual(a.sources,b.sources);assert(b.terms.length>=4);
  for(const field of ['title','summary','goals','prereq','concepts','proof','formulas','examples','quiz','pitfalls'])assert(!/[\u3400-\u9fff]/.test(JSON.stringify(b[field])),`${en.id}/${b.id}/${field} not English`);
  for(let k=0;k<a.formulas.length;k++){assert.equal(a.formulas[k].tex.replace('3票多数错','majority error among 3 votes'),b.formulas[k].tex);katex.renderToString(b.formulas[k].tex,{throwOnError:true});}
  count++;
 }
}
console.log(`PASS: ${count} English chapters, matching IDs, source references, formula notation, and exercise counts; technical terminology present throughout.`);
