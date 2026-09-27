async page => {
 await page.setViewportSize({width:1440,height:1000});
 await page.screenshot({path:'output/playwright/dark-home.png'});
 await page.goto('http://127.0.0.1:3760/#/course/eecs453/classification');
 await page.waitForSelector('.katex');
 const contrast=await page.evaluate(()=>{
  const rgb=s=>(s.match(/[\d.]+/g)||[]).slice(0,3).map(Number);
  const luminance=c=>c.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
  return ['.concept p','.reader-deck','.formula-card>p','.math','.steps li','.quiz summary','.terminology dd','.toc a','#language-toggle','.button.primary'].flatMap(selector=>{
   const el=document.querySelector(selector);if(!el)return [];
   let parent=el,bg;
   while(parent){bg=getComputedStyle(parent).backgroundColor;if(bg!=='rgba(0, 0, 0, 0)'&&bg!=='transparent')break;parent=parent.parentElement;}
   const a=luminance(rgb(getComputedStyle(el).color)),b=luminance(rgb(bg));
   return [{selector,ratio:Math.round((Math.max(a,b)+.05)/(Math.min(a,b)+.05)*100)/100}];
  });
 });
 await page.screenshot({path:'output/playwright/dark-chapter.png'});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:'output/playwright/dark-mobile.png'});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 if(contrast.some(x=>x.ratio<4.5)||overflow)throw Error(JSON.stringify({contrast,overflow}));
 await page.emulateMedia({media:'print'});
 const paper=await page.evaluate(()=>getComputedStyle(document.body).backgroundColor);
 await page.emulateMedia({media:'screen'});
 return {contrast,mobileOverflow:overflow,printBackground:paper};
}
