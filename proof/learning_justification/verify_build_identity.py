"""Passive hash reconstruction; never imports A22 or loads a native library."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
PRE = '426eefc40a4c77e8649827b06e3d3cb6e40832b3f678f48c146535c24c60d944'
POST = 'ae1b515af494ef604526dbe8e651c325512b997f6e93f1d3aefb646b96e13256'
NATIVE = ('affine/_rounding_native.cpython-312-x86_64-linux-gnu.so',
          'kernel/native/_a22_native.cpython-312-x86_64-linux-gnu.so')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def selected(name):
    p = PurePosixPath(name)
    return (name in ('run.py', 'build_native.py', 'build_all_native.py',
                     'launch_fresh.py', 'reference/full_model_reference.md')
            or (p.parts[0] in ('affine', 'kernel') and '__pycache__' not in p.parts
                and p.suffix in ('.py', '.c', '.h', '.so', '.pyd', '.dll', '.dylib')))


def identity(files):
    h = hashlib.sha256()
    names = sorted(n for n in files if selected(n))
    for n in names:
        h.update(n.encode()+b'\0')
        h.update(files[n])
    return h.hexdigest(), names


def main():
    if not __debug__:
        raise RuntimeError('Run without -O; assertions are required.')
    source = (Path(sys.argv[1]) if len(sys.argv)>1 else
              HERE.parent/'provenance_audit/source/A22_fresh_launch_v3_3_EN')
    files = {p.relative_to(source).as_posix(): p.read_bytes()
             for p in source.rglob('*') if p.is_file() and selected(p.relative_to(source).as_posix())}
    before, before_names = identity({n:b for n,b in files.items() if n not in NATIVE})
    after, after_names = identity(files)
    assert before == PRE, ('pre-build identity mismatch', before)
    assert after == POST, ('post-build identity mismatch', after)
    reference = json.loads((HERE/'output/native_extensions_provenance.json').read_text())
    for record in reference['extensions']:
        data = files[record['path']]
        assert len(data) == record['bytes'] and sha(data) == record['sha256']
    campaign = json.loads((HERE/'output/campaign_identity_reference.json').read_text())
    assert sha(files[NATIVE[0]]) == campaign['environment']['native_sha256']
    kernel_data = {'sources':after, 'environment':campaign['environment'],
                   'precision':160, 'symbols':256}
    kernel_id = sha(json.dumps(kernel_data,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
    assert kernel_id == campaign['kernel_id']
    print(json.dumps({'status':'PASS', 'pre_build_source_identity':before,
                      'post_build_source_identity':after,
                      'pre_build_identity_files':len(before_names),
                      'post_build_identity_files':len(after_names),
                      'kernel_id':kernel_id, 'native_libraries_loaded':False,
                      'a22_imported_or_executed':False}))


if __name__ == '__main__':
    main()
