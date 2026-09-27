# 知序 · 四门课程复习工作台

双击本文件夹中的 **start.cmd**，网站会在浏览器打开：

http://127.0.0.1:3760

已包含本地数学排版资源。正常运行无需网络、账号或数据库。需要 Node.js 18 或以上；这台电脑已安装 Node.js 22。

## 中英文切换

首次打开默认使用 **English**。顶部搜索栏旁的 **中文 / English** 按钮切换界面与全部章节正文，包括学习目标、推导、公式说明、例题、提示和自测解析。选择会在本浏览器中记住，下次打开继续使用所选语言。

每章附中英专业术语对照；英文正文使用标准课程术语。原始 PDF 文件保持原语言。两种语言共用同一套章节 ID、收藏和掌握状态，切换不会丢失进度；搜索支持中文和英文关键词。

## 已整理内容

- EECS 376：Lecture 01–07，7 个单元。
- EECS 453：Lecture 1–5、数学基础及 RL 1–3，9 个单元。
- EECS 492：Lecture 1–6，含数学复习和 CNN，7 个单元。
- MATH 465：Lecture 1–7，7 个单元。

共 30 个复习单元、60 道逐步例题、90 道附提示和解析的自测。每章有学习目标、概念讲解、公式条件、推导、易错点和 PDF 页码来源。后续大纲内容只标为待补充，不当作已下载讲义。

点击章节中的「收藏本章」「复习状态」即可保存记录。记录保存在当前浏览器、当前网站地址下；清除浏览器数据会清除这些记录，换浏览器或换端口不会自动同步。自测使用自编练习，不自动判分。

资料目录是 `web` 的同级文件夹：`EECS 376`、`EECS 453`、`EECS 492`、`MATH 465`。原始文件没有被移动或修改。资料链接按白名单提供，PDF 页码是文件中的物理页码，可能与幻灯片页脚不同。内容相同的文件按 SHA-256 合并，Long / Short 等不同版本保留。

未命名的 EECS 492 PDF 是《Wrestling with Killer Robots》伦理阅读，不是缺失的讲义。453 强化学习单元来自补充讲义，其存在不代表已确认本学期考试范围。已有个人解答单独标注为未核验，未作为正确性依据。

## 启动与停止

`start.cmd` 在后台启动仅监听 `127.0.0.1` 的 Node 服务；重复运行会打开已有网站。日志为 `server.log` 和 `server-error.log`。

也可在本文件夹终端运行 `npm start`，用 Ctrl+C 停止。若已由脚本后台启动，先在任务管理器中根据命令行 `...\web\server.mjs` 找到对应 Node 进程并结束，不要结束其他项目的 Node 进程。

若 3760 端口已被其他程序占用，查看日志，或在 PowerShell 中运行 `$env:PORT=3761` 后执行 `node server.mjs`，访问相应端口。双击启动脚本固定使用 3760。

## 后续维护

课程正文在 `data/eecs376.js`、`data/eecs453.js`、`data/eecs492.js`、`data/math465.js`；统一内容结构含 `concepts`、`formulas`、`proof`、`examples`、`quiz`、`sources`。

英文正文分别位于 `data/english376.js`、`data/english453.js`、`data/english492.js`、`data/english465.js`。术语位于 `data/terminology.js`，界面语言与课程元数据位于 `data/localization.js`。新增或修改章节时，请同步维护两种语言；运行 `node scripts/check-locales.mjs` 验证章节 ID、练习数量、公式和来源一致。

添加新资料后可运行 `python scripts/index_sources.py` 更新索引（需要 pypdf），再人工编写或更新对应章节，并重启本地服务以加载新的资料白名单。索引脚本不会自动生成新讲义的复习正文。生成的提取文本位于 `tmp/extracted`，不通过网站提供。

本地验证：`npm run check`。网站运行后：`node scripts/check.mjs --http`。

如果移到另一台电脑时没有带上 `node_modules`，先运行一次 `npm install` 恢复固定版本的 KaTeX 依赖，之后可离线使用。KaTeX 许可证位于 `node_modules/katex/LICENSE`。
