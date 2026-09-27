"""Build a local, allow-listed resource index; never modify course materials."""
from pathlib import Path
import hashlib
import json
import re
import logging
from pypdf import PdfReader
logging.getLogger('pypdf').setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parents[1]
COURSES = ['EECS 376', 'EECS 453', 'EECS 492', 'MATH 465']
out = ROOT / 'data'
out.mkdir(exist_ok=True)
cache = ROOT / 'tmp' / 'extracted'
cache.mkdir(parents=True, exist_ok=True)
sources = []
for course in COURSES:
    seen = {}
    for path in sorted((ROOT.parent / course).rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.pdf', '.ipynb', '.tex', '.md'}:
            continue
        if any(p in {'tmp', 'output', '__pycache__'} for p in path.parts):
            continue
        if path.name in {'header.tex', 'qq_defs.tex', 'hw_template.tex'}:
            continue
        relative = path.relative_to(ROOT.parent).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in seen:
            seen[digest]['aliases'].append(relative)
            continue
        rid = hashlib.sha256(relative.encode()).hexdigest()[:16]
        low = relative.lower()
        category = '其他资料'
        if 'lecture' in low: category = '讲义'
        if ('review' in low or 'math resources' in low) and 'lecture2_agents' not in low: category = '基础复习'
        if 'rl-lectures' in low: category = '强化学习补充讲义'
        if any(x in low for x in ['homework', '/hw', '376hw', '465hw', 'worksheet', 'discussion', 'ethics assignment']): category = '练习与讨论'
        if 'references/' in low or 'papers of interest' in low: category = '延伸阅读'
        if 'projects/' in low: category = '项目资料'
        if 'syllabus' in low: category = '课程大纲'
        if any(x in low for x in ['solution', 'completed', 'appendix']): category = '已有解答（未核验）'
        item = dict(id=rid, course=course, name=path.name, path=relative, category=category, aliases=[], pages=0)
        if path.name == '1b200d08-3412-45eb-8d5c-f9ba7b7d82df.pdf':
            item['category'] = '伦理阅读'
            item['title'] = 'Wrestling with Killer Robots — Erik Lin-Greenberg (2021)'
        sources.append(item)
        seen[digest] = item
        if path.suffix.lower() == '.pdf':
            try:
                reader = PdfReader(path)
                item['pages'] = len(reader.pages)
                # Books remain resources; extracting hundreds of pages is unnecessary.
                if category not in {'延伸阅读', '项目资料', '已有解答（未核验）'}:
                    pages = [p.extract_text() or '' for p in reader.pages]
                    (cache / (rid + '.txt')).write_text('\n'.join(f'\n=== PAGE {i+1} ===\n{t}' for i,t in enumerate(pages)), encoding='utf-8')
                    item['pageHeadings'] = [re.sub(r'\s+', ' ', p.strip())[:150] for p in pages]
                    item['needsVisualReview'] = [i+1 for i,p in enumerate(pages) if len(p.strip()) < 30]
            except Exception as exc:
                item['error'] = str(exc)
(out / 'sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
for s in sources:
    if s['category'] in {'讲义', '强化学习补充讲义', '其他资料'} and s['pages']:
        print(json.dumps({k:s[k] for k in ['id','path','pages']}, ensure_ascii=False))
print(f'Indexed {len(sources)} resources. Originals were not modified.')
