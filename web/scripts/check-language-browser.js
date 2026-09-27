async (page) => {
 const ensure=(value,message)=>{if(!value)throw Error(message);};
 const base='http://127.0.0.1:3760/';
 const backup=await page.evaluate(()=>({language:localStorage.getItem('study-desk-language'),progress:localStorage.getItem('study-desk-v1')}));
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const external=[];
 await page.context().route('**/*',route=>{if(!route.request().url().startsWith(base)){external.push(route.request().url());return route.abort();}return route.continue();});
 const routes=await page.evaluate(async()=>{const {courses}=await import('/data/courses.js');return courses.flatMap(c=>c.lessons.map(l=>`#/course/${c.id}/${l.id}`));});
 let checked=0;const untranslated=[];
 async function waitRoute(hash){await page.waitForFunction(h=>document.querySelector('main')?.dataset.route===h,hash);}
 async function toggle(){await page.locator('#language-toggle').click();}
 try{
  await page.evaluate(()=>localStorage.removeItem('study-desk-language'));
  await page.goto(base);await waitRoute('#/');
  ensure(await page.locator('html').getAttribute('lang')==='en','First visit must default to English');
  ensure((await page.locator('h1').innerText()).includes('Connect the ideas'),'Default interface not English');
  await page.setViewportSize({width:1440,height:1000});
  await page.screenshot({path:'output/playwright/language-home-en.png',fullPage:true});
  for(const lang of ['en','zh']){
   if(await page.locator('html').getAttribute('lang')!==(lang==='en'?'en':'zh-CN'))await toggle();
   for(const hash of routes){
    await page.goto(base+hash);await waitRoute(hash);
    const metrics=await page.evaluate(()=>{
     const remaining=[];const walker=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT);let n;
     while(n=walker.nextNode())if(/[\u3400-\u9fff]/.test(n.nodeValue)&&!n.parentElement.closest('[data-preserve-language],.source-link,.math'))remaining.push(n.nodeValue.trim());
     return {examples:document.querySelectorAll('.example').length,quizzes:document.querySelectorAll('.quiz').length,terms:document.querySelectorAll('.terminology dt').length,fallback:document.querySelectorAll('.math-fallback').length,overflow:document.documentElement.scrollWidth>innerWidth+1,remaining};
    });
    ensure(metrics.examples===2&&metrics.quizzes===3&&metrics.terms>=4&&!metrics.fallback&&!metrics.overflow,hash+' '+JSON.stringify(metrics));
    if(lang==='en'&&metrics.remaining.length)untranslated.push({hash,text:metrics.remaining});
    checked++;
   }
  }
  await page.goto(base+'#/course/eecs453/classification');await waitRoute('#/course/eecs453/classification');
  await page.locator('#lesson-status').selectOption('mastered');
  if(await page.locator('[data-save]').getAttribute('aria-pressed')!=='true')await page.locator('[data-save]').click();
  const before=await page.evaluate(()=>localStorage.getItem('study-desk-v1'));
  await toggle();
  ensure(page.url().endsWith('#/course/eecs453/classification'),'Language switch changed chapter');
  ensure(await page.locator('#lesson-status').inputValue()==='mastered','Status lost during switch');
  ensure(await page.locator('[data-save]').getAttribute('aria-pressed')==='true','Bookmark lost during switch');
  ensure(await page.evaluate(()=>localStorage.getItem('study-desk-v1'))===before,'Language switch altered study progress');
  await page.reload();await waitRoute('#/course/eecs453/classification');
  ensure(await page.locator('html').getAttribute('lang')==='en','English preference not retained');
  await page.locator('.answer summary').first().click();
  ensure((await page.locator('.answer p').first().innerText()).includes('1.609'),'English answer not rendered');
  await page.screenshot({path:'output/playwright/language-chapter-en.png',fullPage:true});
  await toggle();await page.reload();await waitRoute('#/course/eecs453/classification');
  ensure(await page.locator('html').getAttribute('lang')==='zh-CN','Chinese preference not retained');
  ensure((await page.locator('#concepts').innerText()).includes('共享协方差'),'Chinese content missing');
  await page.screenshot({path:'output/playwright/language-chapter-zh.png',fullPage:true});
  await toggle();
  await page.locator('#search').fill('动态规划');await page.locator('#search-form button').click();
  await page.waitForSelector('.search-result');ensure(await page.locator('.search-result').count()>0,'Chinese search failed in English mode');
  await page.goto(base+'#/library');await waitRoute('#/library');
  await page.locator('#category-filter').selectOption('伦理阅读');await page.waitForFunction(()=>document.querySelectorAll('.resource-row').length===1);
  await toggle();ensure(await page.locator('#category-filter').inputValue()==='伦理阅读','Translated category lost stable value');
  await toggle();
  await page.setViewportSize({width:390,height:844});
  for(const hash of ['#/','#/course/math465/recurrences','#/formulas','#/library']){
   await page.goto(base+hash);await waitRoute(hash);
   for(let i=0;i<2;i++){
    const dimensions=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,button:document.querySelector('#language-toggle').getBoundingClientRect().right<=innerWidth}));
    ensure(!dimensions.overflow&&dimensions.button,'Mobile layout failed '+hash+JSON.stringify(dimensions));
    await toggle();
   }
  }
  await page.goto(base+'#/course/math465/recurrences');await waitRoute('#/course/math465/recurrences');
  await page.screenshot({path:'output/playwright/language-mobile-en.png',fullPage:true});
  ensure(!untranslated.length,'Untranslated English UI: '+JSON.stringify(untranslated));
  ensure(!errors.length,'Browser errors: '+JSON.stringify(errors));ensure(!external.length,'External requests: '+JSON.stringify(external));
  return {chapterVersions:checked,defaultEnglish:true,languagePersistence:true,progressPreserved:true,answers:true,bilingualSearch:true,stableCategoryValues:true,mobile:true,untranslated,errors,external};
 }finally{
  await page.evaluate(b=>{for(const [key,value] of [['study-desk-language',b.language],['study-desk-v1',b.progress]]){if(value===null)localStorage.removeItem(key);else localStorage.setItem(key,value);}},backup);
  await page.setViewportSize({width:1440,height:1000});await page.goto(base);
 }
}
