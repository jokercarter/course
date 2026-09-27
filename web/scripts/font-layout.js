async page=>{
 await page.setViewportSize({width:390,height:844});
 await page.goto('http://127.0.0.1:3760/#/formulas');
 await page.waitForSelector('.formula-card');
 await page.locator('#language-toggle').click();
 return await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:innerWidth,items:Array.from(document.querySelectorAll('body *')).filter(e=>e.getBoundingClientRect().right>innerWidth&&!e.closest('.math')).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,60),width:e.getBoundingClientRect().width})).slice(0,20)}));
}
