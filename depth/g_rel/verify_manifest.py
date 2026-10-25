"""Read-only verification of the v4.3 release directory."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    d=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
    for name,item in d['files'].items():
        p=ROOT/name
        if not p.is_file() or p.stat().st_size!=item['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise RuntimeError('manifest mismatch: '+name)
    print('PASS_RELEASE_MANIFEST',len(d['files']))
if __name__=='__main__':main()
