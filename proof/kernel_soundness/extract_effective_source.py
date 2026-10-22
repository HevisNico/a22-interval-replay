"""Reconstruct textual runtime substitutions without importing/executing A22.
Only literal strings, known source reads, string operations and audited loops
are interpreted. This is an audit view, not an executable replacement engine.
"""
import ast,json,hashlib,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'provenance_audit/source/A22_fresh_launch_v3_3_EN'
OUT=Path(__file__).resolve().parent/'output/effective_source'
LEGACY=ROOT/'kernel/R_cycle_local_A20_2026-10-18'

def source(module,name):
 p=LEGACY/(module+'.py');s=p.read_text();tree=ast.parse(s)
 n=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
 return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])

def main():
 OUT.mkdir(parents=True,exist_ok=True);env={};edits=[]
 def ev(n):
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Name):return env[n.id]
  if isinstance(n,(ast.Tuple,ast.List)):return [ev(x) for x in n.elts]
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return ev(n.left)+ev(n.right)
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):
   a=n.func
   if isinstance(a.value,ast.Name) and a.value.id=='inspect' and a.attr=='getsource':
    target=n.args[0];assert isinstance(target,ast.Attribute) and target.value.id=='b'
    return source('validation_A15',target.attr)
   if isinstance(a.value,ast.Name) and a.value.id=='textwrap' and a.attr=='dedent':return textwrap.dedent(ev(n.args[0]))
   if a.attr=='replace':
    text=ev(a.value);old,new=map(ev,n.args);count=text.count(old);assert count==1,(old,count)
    edits.append({'old':old,'new':new,'occurrences':count});return text.replace(old,new)
  raise ValueError(ast.dump(n))
 tree=ast.parse((ROOT/'affine/engine.py').read_text())
 tracked={'_src','_old','_old_aux','_hook_group_old','_hook_group_new','_hook_single_old','_hook_single_new','_hook_cluster_old','_hook_cluster_new','_coef','_adv','_old_order'}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in tracked:
   env[n.targets[0].id]=ev(n.value)
  elif isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [t.id for t in n.target.elts]==['_o','_n']:
   for old,new in ev(n.iter):
    env['_o'],env['_n']=old,new
    for q in n.body:
     if isinstance(q,ast.Assign) and isinstance(q.targets[0],ast.Name) and q.targets[0].id=='_coef':env['_coef']=ev(q.value)
 for var,name in [('_src','unit'),('_coef','coefficients'),('_adv','advance_inner')]:
  ast.parse(env[var]);(OUT/(name+'.txt')).write_text(env[var])
 lattice=ast.parse((ROOT/'affine/sound_lattice.py').read_text())
 definitions=ast.literal_eval(next(n.value for n in lattice.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EDITS' for t in n.targets)))
 for module,fun,replacements in definitions:
  text=source(module,fun)
  for old,new in replacements:
   assert text.count(old)==1;edits.append({'function':module+'.'+fun,'old':old,'new':new,'occurrences':1});text=text.replace(old,new)
  ast.parse(text);(OUT/(module+'__'+fun+'.txt')).write_text(text)
 report={'method':'AST-based textual reconstruction; no A22 module imported or executed','substitutions':edits,'files':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.glob('*.txt'))],'outer_advance_wrappers_in_order':['avance_causale_A22.advance (FAST relative ordering)','nofire_cover.advance (strict READY fallback)'],'other_adapters':['ready_general_A22.install replaces legacy local READY helpers','port_box_adapter then port_symbols replace settings and per-port evaluations','engine history folding/union/cap adapters remain installed']}
 (OUT.parent/'effective_source_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'files':len(report['files']),'checked_substitutions':len(edits),'original_engine_executed':False}))
if __name__=='__main__':main()
