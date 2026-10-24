"""Read only exact records from the previously delivered authenticated archive."""
import hashlib,json,io
from pathlib import Path
from zipfile import ZipFile
from directed import require
ARCHIVE=Path(__file__).parent/'dependencies/A22_point_4_modes_and_tail_budget_EN.zip'
EXPECTED='17b7d37da9a87b2db89ac478df279d89a6b9513f58137ee7a7605b48a3059fd0'

def baseline(suffix):
    data=ARCHIVE.read_bytes();require(hashlib.sha256(data).hexdigest()==EXPECTED,'previous deliverable hash')
    found=[]
    def walk(data,route):
        with ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                if name.endswith('/'+suffix):found.append((json.loads(z.read(name)),route+[name]))
            if found:return
            for name in z.namelist():
                if name.endswith('.zip'):
                    walk(z.read(name),route+[name])
                    if found:return
    walk(data,[ARCHIVE.name]);require(len(found)==1,'one baseline record found')
    return found[0]
