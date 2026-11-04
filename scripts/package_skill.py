import argparse,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',default='dist/kernelopt-v0.1.0.zip');a=p.parse_args();root=Path(__file__).resolve().parents[1];out=root/a.output;out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for f in root.rglob('*'):
  if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts and f.suffix != '.pyc' and 'dist' not in f.parts:z.write(f,f.relative_to(root))
print(out)
