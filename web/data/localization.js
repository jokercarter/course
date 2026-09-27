import en376 from './english376.js';
import en453 from './english453.js';
import en492 from './english492.js';
import en465 from './english465.js';

const content={eecs376:en376,eecs453:en453,eecs492:en492,math465:en465};
const metadata={
 eecs376:{description:'Explain why algorithms are correct and efficient, and turn proofs into problem-solving methods.',coverage:'Lecture 01–07 · Algorithm design and analysis',pending:['Computability theory — lecture materials pending','Computational complexity — lecture materials pending','Randomized algorithms — lecture materials pending','Cryptography — lecture materials pending'],related:'Use Discussions 1–2, Worksheets 1–2, and HW 1–3 for related problems. Organize algorithm solutions as definitions, algorithm, correctness proof, and complexity analysis.'},
 eecs453:{description:'Connect statistical modeling with optimization: risk, estimation, regularization, and learning algorithms.',coverage:'Lectures 1–5 · Mathematical review · Supplementary RL lectures 1–3',pending:['SVMs and kernel methods — standalone lectures pending; optimization examples are covered','Deep neural networks — main-course lectures pending','Clustering, EM, and PCA — main-course lectures pending','Representation learning, matrix factorization, autoencoders, and generative models — lectures pending'],related:'The library preserves Long and Short slide versions and project guidelines. RL notes are supplementary materials, not a confirmed statement of current exam coverage. Reference books are further reading, not additional required chapters.'},
 eecs492:{description:'From rational agents to learning systems: perception, prediction, and decision-making.',coverage:'Lectures 1–6 · Mathematical review and CNNs',pending:['Lecture 7 and later — not found locally; their topics are not inferred','Search and problem solving — later lectures pending','Reasoning and decision-making under uncertainty — later lectures pending'],related:'Homework 1 relates to agents, decision trees, regression, and neural networks. The unnamed PDF is Erik Lin-Greenberg’s Wrestling with Killer Robots (2021), an ethics case study, not a missing lecture.'},
 math465:{description:'Build counting arguments with bijections, generating functions, and recurrence relations.',coverage:'Lectures 1–7 · Counting, generating functions, Stirling numbers, and recurrences',pending:['Further enumerative combinatorics — detailed lecture sequence pending','Graph theory and related topics — second part, lecture materials pending'],related:'Use Homework 1–4 to identify related counting, bijection, generating-function, and recurrence problems. Attempt them independently and review the original practice examples in these notes.'}
};
export function localizedCourses(original,language){
 if(language!=='en')return original;
 return original.map(course=>({...course,...metadata[course.id],name:course.english,lessons:course.lessons.map(l=>{
  const t=content[course.id][l.id];
  if(!t)throw Error(`Missing English content: ${course.id}/${l.id}`);
  if(t.formulas.length!==l.formulas.length)throw Error(`Formula translation mismatch: ${l.id}`);
  return {...l,...t,title:l.english,lecture:l.lecture.replace('基础复习','Mathematical review').replace('无约束','Unconstrained optimization').replace('约束','Constrained optimization').replace('数学部分','Mathematical review').replace('前半','Part I').replace('后半','Part II').replace('补充','Supplementary'),concepts:t.concepts.map(([title,body])=>({title,body})),formulas:l.formulas.map((f,i)=>({...f,tex:f.tex.replace('3票多数错','majority error among 3 votes'),label:t.formulas[i][0],note:t.formulas[i][1]})),examples:t.examples.map(([q,...steps])=>({q,steps})),quiz:t.quiz.map(([q,hint,a])=>({q,hint,a}))};
 })}));
}

const ui={
 '学习工作台':'Workspace','学习总览':'Overview','我的收藏':'Bookmarks','公式速查':'Formula reference','课程资料库':'Source library','我的课程':'My courses','个人复习空间':'Personal study space',
 '一点一点，建立理解':'Build understanding, one step at a time','读懂概念 → 手算例题':'Understand → Work examples','独立自测 → 回看薄弱点':'Self-test → Review gaps','个人课程复习站':'Personal course review',
 '把知识串起来，':'Connect the ideas.','让复习':'Make your learning ','有迹可循。':'count.','四门课程，一张清晰的学习地图。':'Four courses. One clear learning map.','从概念、推导到例题，把每一个「懂了」变成真正的掌握。':'Move from concepts and derivations to independent problem solving.',
 '继续上次复习':'Continue studying','从第一章开始':'Start the first chapter','理解概念':'Understand the concepts','推导与例题':'Derive and apply','自测与回顾':'Test and review','理解是积累，不是一次完成。':'Understanding grows through practice.',
 '正在整理的课程':'Courses in your workspace','有内容的复习单元':'Available study units','附解析的自测题':'Self-checks with explanations','已标记掌握的单元':'Units marked as mastered','跟随原始讲义，按自己的节奏复习':'Follow the source lectures at your own pace',
 '资料覆盖说明':'Coverage notes','只展开已有资料中的知识':'Based on available course materials','当前讲义详解、公式与自编练习均可直接阅读。后续课程依大纲保留目录，缺少的讲次明确标注「待补充」。资料页保留原文入口与重复版本信息。':'Read explanations, formulas, and original practice exercises for the available lectures. Later syllabus topics remain marked as pending. The library links to original files and identifies duplicate versions.',
 '一个有效的复习顺序':'A practical study routine','先试着讲清楚，再打开答案。':'Explain it before revealing the answer.','读完一节后，合上讲义做三道自测。能解释每一步为什么成立，再把它标记为「已掌握」。':'Close the notes and attempt the three self-checks. Mark a unit as mastered when you can justify each step.',
 '打开公式速查':'Open formula reference','查看全部课程资料':'Browse course resources','复习目录':'Study units','每章含概念、推导、例题与自测':'Concepts, derivations, examples, and self-checks',
 '后续学习地图':'Upcoming topics','等待新资料，继续补全':'More materials to come','以下仅保留已有大纲能支持的范围，不计入当前复习完成率。':'Only syllabus-supported topics are listed below. Pending material is excluded from completion statistics.','查看课程范围依据':'View the source for course scope','待补充':'Pending',
 '课程目录':'Course contents','收藏本章':'Bookmark chapter','已收藏':'Bookmarked','复习状态':'Study status','正在复习':'In progress','已掌握':'Mastered','尚未复习':'Not started','打印本章':'Print chapter',
 '依据讲义编写的中文复习讲解 · 例题与自测为自编练习 · 页码按 PDF 文件计数':'Study notes based on the lectures · Original practice exercises · References use physical PDF page numbers',
 '学习目标与先修':'Learning objectives and prerequisites','先修知识':'Prerequisites','概念讲解':'Concepts','公式与适用条件':'Formulas and assumptions','关键推导 / 证明':'Key derivation / proof','逐步例题':'Worked examples','先自己列出思路，再逐步对照。':'Outline your own approach first, then compare each step.',
 '易错点检查':'Common pitfalls','独立自测':'Self-checks','先在纸上回答；需要时打开提示，再核对解析。开放题由你自行核对，不自动判分。':'Work on paper first, reveal a hint if needed, then compare your reasoning with the explanation. These open-ended questions are self-assessed, not automatically graded.',
 '给我一点提示':'Show hint','查看答案与解析':'Show answer and explanation','现在，能独立解释了吗？':'Can you explain it independently?','能复述概念、重做例题，再更新掌握状态。':'Restate the concepts and redo the examples before updating your status.','标记为已掌握':'Mark as mastered','回到原始资料':'Return to the sources','查看资料库':'View source library','上一单元':'Previous unit','下一单元':'Next unit','本课程最后一个单元':'Last available unit in this course','返回课程目录':'Back to course contents','本章导航':'On this page','学习目标':'Objectives','公式与条件':'Formulas and assumptions','推导与证明':'Derivations and proofs','易错点':'Pitfalls','原始资料':'Source materials','先理解，再记忆。':'Understand before memorizing.',
 '全部课程':'All courses','课程':'Course','记住公式，也记住它成立的条件。点击章节名可回看推导与例题。':'Remember the assumptions, not only the formula. Open a chapter to review its derivations and examples.','没有找到这门课程。':'Course not found.',
 '直接打开本地原始文件。内容相同的副本已合并，长短版本与未核验解答分别标注。':'Open original local files. Identical copies are grouped; Long and Short versions and unverified solutions remain labelled.','全部类型':'All categories','类型':'Category','此筛选下没有资料。':'No resources match this filter.','资料只在你的电脑上提供。若移动了原文件夹，链接将不可用；课程资料不会被上传。项目文档和参考书只作为查阅入口。':'Resources are served only from this computer. Moving the original folders breaks their links. Materials are not uploaded; project documents and textbooks are reference links.',
 '讲义':'Lecture slides','基础复习':'Mathematical review','强化学习补充讲义':'Supplementary RL lectures','练习与讨论':'Exercises and discussions','延伸阅读':'Further reading','项目资料':'Project materials','课程大纲':'Syllabus','已有解答（未核验）':'Existing solutions (unverified)','伦理阅读':'Ethics readings','其他资料':'Other resources',
 '搜索知识点':'Search topics','想复习什么？':'What would you like to review?','在顶部输入关键词，例如：动态规划、Bayes、Stirling、正则化。':'Search for a concept such as dynamic programming, Bayes, Stirling, or regularization.','没有找到匹配的章节':'No matching chapters','把问题变成一个关键词':'Start with a keyword','试试更短的词，或切换中英文术语。未下载的后续讲义不包含详解。':'Try a shorter query or its Chinese or English equivalent. Missing lectures do not have detailed notes.','例如「递推」「gradient」「决策树」':'Try “recurrence”, “gradient”, or “decision tree”.',
 '把需要反复理解的章节留在这里。收藏和掌握状态保存在当前浏览器。':'Keep chapters you want to revisit here. Bookmarks and study progress are stored in this browser.','取消收藏':'Remove bookmark','留个位置，给需要再看一遍的知识。':'Keep useful chapters close.','在章节页点击「收藏本章」，它就会出现在这里。':'Select “Bookmark chapter” while reading to add it here.','去看看课程':'Explore the courses',
 '页面未找到':'Page not found','这页暂时不存在':'This page does not exist','回到学习总览':'Back to overview','已取消收藏':'Bookmark removed','已收藏本章':'Chapter bookmarked','已记录掌握状态':'Mastery status saved','复习状态已保存':'Study status saved',
 '浏览器无法保存进度，本次更改仅在当前页面有效。':'Browser storage is unavailable. Changes will last only for this page session.','浏览器存储不可用或记录损坏；本次可正常阅读，但进度可能无法保存。':'Browser storage is unavailable or damaged. Reading works, but progress may not persist.',
 '跳到正文':'Skip to content','主导航':'Main navigation','展开导航':'Toggle navigation','你的学习空间':'Your study space','总览':'Overview','搜索所有课程':'Search all courses','搜索知识点、公式、英文术语…':'Search concepts, formulas, and terminology…','搜索':'Search','本地 · 离线可用':'Local · Offline ready','正在打开你的复习工作台…':'Opening your study workspace…','学习笔记依据本地资料整理 · 原始资料保留在课程文件夹':'Notes based on local materials · Original files remain in their course folders','复习方法':'Study method','学习统计':'Study statistics','数学公式；较长时可横向滚动':'Mathematical formula; scroll horizontally if needed',
 '资料索引暂时无法读取':'Unable to load the source index','请通过文件夹中的 start.cmd 启动网站，再访问本地地址。':'Run start.cmd in the website folder, then open the local address.','重试':'Retry','开始学习':'Start studying'
};
const sorted=Object.entries(ui).sort((a,b)=>b[0].length-a[0].length);
export function translateUI(text){
 if(!/[\u3400-\u9fff]/.test(text))return text;
 const exact=ui[text.trim()];if(exact)return text.replace(text.trim(),exact);
 let result=text
 .replace(/搜索「(.*?)」/g,'Search: “$1”')
 .replace(/(\d+) 个复习单元匹配。支持中文、英文术语与公式名称。/g,'$1 matching study units. Search Chinese or English terminology and formula names.')
 .replace(/浏览 (\d+) 项已登记资料/g,'Browse $1 indexed resources')
 .replace(/另有 (\d+) 个相同内容副本/g,'$1 additional identical copies')
 .replace(/PDF 第 ([\d–]+) 页/g,'PDF pp. $1')
 .replace(/(\d+) 个复习单元/g,'$1 study units').replace(/(\d+) 道例题/g,'$1 examples').replace(/(\d+) 道自测/g,'$1 self-checks').replace(/(\d+) 处来源/g,'$1 sources').replace(/(\d+) 项资料/g,'$1 resources').replace(/(\d+) 页/g,'$1 pages').replace(/单元已掌握/g,'units mastered').replace(/单元 (\d+)/g,'Unit $1').replace(/([A-Za-z]+) 版/g,'$1 version');
 for(const [zh,en] of sorted)result=result.split(zh).join(en);
 return result;
}

// Keep original UI text to restore persistent header/footer nodes on language changes.
const originals=new WeakMap();
const attributes=new WeakMap();
export function localizeDOM(root,language){
 const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let node;
 while((node=walker.nextNode())){
  if(node.parentElement?.closest('.math,script,style,[data-preserve-language],#language-toggle'))continue;
  const old=originals.get(node);
  if(old&&node.nodeValue===old.rendered){node.nodeValue=language==='en'?translateUI(old.source):old.source;old.rendered=node.nodeValue;}
  else{const source=node.nodeValue;node.nodeValue=language==='en'?translateUI(source):source;originals.set(node,{source,rendered:node.nodeValue});}
 }
 root.querySelectorAll('[aria-label],[placeholder]').forEach(el=>{
  if(el.id==='language-toggle')return;
  let values=attributes.get(el);if(!values){values={};attributes.set(el,values);}
  for(const attr of ['aria-label','placeholder'])if(el.hasAttribute(attr)){if(!(attr in values))values[attr]=el.getAttribute(attr);el.setAttribute(attr,language==='en'?translateUI(values[attr]):values[attr]);}
 });
}
