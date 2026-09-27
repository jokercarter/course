from pathlib import Path
import ast
import contextlib
import io
import json
import numpy as np
import sympy as sp

root = Path(__file__).resolve().parent
nb = json.loads((root / 'q4_starter.ipynb').read_text(encoding='utf-8'))
nb['cells'][3]['source'] = '''def row_l1_norms(A):
    return np.abs(A).sum(axis=1)
'''.splitlines(keepends=True)
nb['cells'][6]['source'] = '''def closest_tower(A, B):
    a2 = (A**2).sum(axis=1)[None, :]
    b2 = (B**2).sum(axis=1)[:, None]
    sq_dists = b2 + a2 - 2 * B @ A.T
    return np.argmin(sq_dists, axis=1)
'''.splitlines(keepends=True)
namespace = {}
count = 0
appendix = [r'\section*{附录：完成后的 notebook}',
            '以下按原顺序列出全部代码单元及运行输出。原题的检查单元包含参考循环，仅用于验证，不属于答案函数。']
for index, cell in enumerate(nb['cells']):
    cell.setdefault('id', f'cell-{index}')
    if cell['cell_type'] != 'code':
        continue
    count += 1
    source = ''.join(cell['source'])
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        exec(compile(source, f'cell-{index}', 'exec'), namespace)
    output = stream.getvalue()
    cell['execution_count'] = count
    cell['outputs'] = ([{'output_type': 'stream', 'name': 'stdout', 'text': output.splitlines(keepends=True)}]
                       if output else [])
    if count == 4:
        appendix.append(r'\newpage')
    appendix += [rf'\subsection*{{In [{count}]}}', r'\begin{lstlisting}[language=Python]', source.rstrip(), r'\end{lstlisting}']
    if output:
        appendix += [r'\textbf{实际输出}', r'\begin{lstlisting}', output.rstrip(), r'\end{lstlisting}']
    print(f'Cell {count}: OK {output.strip()}')
(root / 'q4_completed.ipynb').write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
(root / 'q4_notebook_appendix.tex').write_text('\n'.join(appendix), encoding='utf-8')

# Verify constraints on answer functions, independently of reference cells.
for index, limit in [(3, 1), (6, 4)]:
    tree = ast.parse(''.join(nb['cells'][index]['source']))
    assert len(tree.body[0].body) <= limit
    assert not any(isinstance(node, (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)) for node in ast.walk(tree))
closest = namespace['closest_tower']
rng = np.random.default_rng(74)
for m, n, d in [(1, 5, 1), (7, 11, 3), (4, 0, 2), (30, 60, 8)]:
    a, b = rng.normal(size=(m, d)), rng.normal(size=(n, d))
    expected = np.argmin(np.sum((b[:, None, :] - a[None, :, :])**2, axis=2), axis=1)
    np.testing.assert_array_equal(closest(a, b), expected)
np.testing.assert_array_equal(closest(np.array([[-1., 0.], [1., 0.]]), np.array([[0., 0.]])), [0])
w = sp.symbols('w')
x, y = w**2 - 3*w, w**4 - 3*w**2 + w
assert sp.expand(sp.diff(x*x-y*y+2*x*y, w) - (-8*w**7+48*w**5-40*w**4-56*w**3+60*w**2+4*w)) == 0
print('Symbolic derivative, answer constraints, and extra NumPy checks: PASS')
