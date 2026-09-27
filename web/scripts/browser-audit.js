// Pass this callback to `playwright-cli run-code` against the running local site.
async (page) => {
  const base = 'http://127.0.0.1:3760';
  const errors = [];
  const external = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.context().unrouteAll({behavior:'ignoreErrors'});
  await page.context().route('**/*', route => {
    if (!route.request().url().startsWith(base+'/')) {
      external.push(route.request().url()); return route.abort();
    }
    return route.continue();
  });
  const saved = await page.evaluate(() => localStorage.getItem('study-desk-v1'));
  const routes = await page.evaluate(async () => {
    const {courses} = await import('/data/courses.js');
    return courses.flatMap(c => c.lessons.map(l => ({route:`/course/${c.id}/${l.id}`,title:l.title})));
  });
  const checked = [];
  try {
    for (const entry of routes) {
      await page.goto(base + '/#' + entry.route);
      await page.waitForFunction(title => document.querySelector('h1')?.textContent === title, entry.title);
      const result = await page.evaluate(() => ({
        title:document.querySelector('h1').textContent,
        examples:document.querySelectorAll('.example').length,
        quiz:document.querySelectorAll('.quiz').length,
        formulas:document.querySelectorAll('.katex').length,
        fallback:document.querySelectorAll('.math-fallback,.katex-error').length,
        sources:document.querySelectorAll('#sources .source-link').length,
        overflow:document.documentElement.scrollWidth>innerWidth+1
      }));
      if(result.examples<2||result.quiz<3||!result.formulas||result.fallback||!result.sources||result.overflow) throw Error(JSON.stringify(result));
      checked.push(result.title);
    }
    await page.goto(base+'/#/course/eecs453/classification');
    await page.waitForSelector('.katex');
    await page.screenshot({path:'output/playwright/reading-desktop.png',fullPage:true});
    await page.setViewportSize({width:390,height:844});
    for(const route of ['/#/','/#/course/math465','/#/course/math465/recurrences','/#/formulas','/#/library?course=eecs492','/#/search?q=Bayes']){
      await page.goto(base+route);
      await page.waitForFunction(hash=>document.querySelector('main')?.dataset.route===hash,route.slice(1));
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
      if(overflow)throw Error('Mobile overflow: '+route);
    }
    await page.goto(base+'/#/course/math465/recurrences');
    await page.waitForFunction(()=>document.querySelector('main')?.dataset.route==='#/course/math465/recurrences');
    await page.screenshot({path:'output/playwright/reading-mobile.png',fullPage:true});
    await page.emulateMedia({media:'print'});
    const print = await page.evaluate(()=>({
      sidebar:getComputedStyle(document.querySelector('.sidebar')).display,
      answerHeight:document.querySelector('.answer p').getBoundingClientRect().height
    }));
    if(print.sidebar!=='none'||print.answerHeight===0)throw Error('Print layout hides answers: '+JSON.stringify(print));
    await page.emulateMedia({media:'screen'});
    if(errors.length||external.length)throw Error(JSON.stringify({errors,external}));
    return {lessons:checked.length,mobileRoutes:6,print,errors,external,offline:'All non-local requests blocked throughout audit'};
  } finally {
    await page.evaluate(saved=>{if(saved===null)localStorage.removeItem('study-desk-v1');else localStorage.setItem('study-desk-v1',saved);},saved);
    await page.emulateMedia({media:'screen'});
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base+'/#/');
  }
}
