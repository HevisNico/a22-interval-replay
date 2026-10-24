"""Record the actual interpreter and installed numerical-library native files."""
import hashlib, importlib.util, json, platform, sys
from pathlib import Path
import numpy, scipy

def record(path):
    path=Path(path).resolve()
    return {'path':str(path),'bytes':path.stat().st_size,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    binaries={'python':record(sys.executable)}
    for module in ['_decimal']:
        spec=importlib.util.find_spec(module)
        binaries[module]=({'origin':spec.origin,'note':'Built into recorded interpreter.'}
            if spec.origin=='built-in' else record(spec.origin))
    for package in [numpy,scipy]:
        root=Path(package.__file__).parent
        paths=set(root.rglob('*.so'))
        companion=root.parent/(root.name+'.libs')
        if companion.exists(): paths.update(p for p in companion.iterdir() if p.is_file())
        binaries[package.__name__]=[record(p) for p in sorted(paths)]
    report={'python':sys.version,'platform':platform.platform(),
      'numpy':numpy.__version__,'scipy':scipy.__version__,'binaries':binaries,
      'usage':'Directed certificates use Python standard library only. NumPy and SciPy are used only for exploratory optimization. Native-library hashes record installed files, not a claim that every file was loaded.',
      'A22_native_binaries_used':False,
      'arithmetic':{'bridge_and_forcing_decimal_digits':70,'finite_histories_decimal_digits':130,
        'elementary_functions':'Finite exp/log series with explicit remainder bounds; directed Decimal basic operations.',
        'root_padding':'1e-95 for finite histories; accepted only after strict directed sign checks.'}}
    (Path(__file__).parent/'ENVIRONMENT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__}))

if __name__=='__main__':main()
