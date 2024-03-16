filenames = open('corpus_files.txt').readlines()
from pathlib import Path
from knowt.constants import DATA_DIR, CORPUS_DIR
base_dir = (CORPUS_DIR / 'corpus_runestone_rst')
base_dir.mkdir()
DATA_DIR = Path('/home/hobs/code/tangibleai/community/knowt/data')
base_dir = (DATA_DIR / 'corpus_runestone_rst')
base_dir.mkdir()
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f)
    if not p.parent.is_dir():
        p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p)
        with p.open() as fin:
            with (base_dir / p).open('w') as fout:
                fout.writelines(fin.readlines())
filenames
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    if not p.parent.is_dir():
        p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p)
        with p.open() as fin:
            with (base_dir / p).open('w') as fout:
                fout.writelines(fin.readlines())
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if not dest.parent.is_dir():
        print(f'mkdir {dest}')
        p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p)
        with p.open() as fin:
            with (base_dir / p).open('w') as fout:
                fout.writelines(fin.readlines())
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
ls -hal /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/InstructorGuide/_sources/Video/
ls -hal /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/InstructorGuide/_sources/
ls -hal /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/
p
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        dest.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
rm /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/InstructorGuide/_sources/Video/youtube.rst
rm -r /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/InstructorGuide/_sources/Video/youtube.rst
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        dest.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if dest.is_dir():
        dest.unlink()
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        dest.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
dest
dest.is_dir()
dest.unlink?
dest.rmdir()
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if dest.is_dir():
        dest.rmdir()
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        dest.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
find /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/ -type d -name '*.rst'
find /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/ -type=d -name='*.rst'
!find /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/ -type d -name '*.rst'
rm -r /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/InstructorGuide/_sources/Assessments/shortanswer.rst
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if dest.is_dir():
        dest.rmdir()
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        dest.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
!find /home/hobs/code/tangibleai/community/knowt/data/corpus_runestone_rst/ -type d -name '*.rst'
filenames = open('corpus_files.txt').readlines()
for f in filenames:
    p = Path(f.strip().lstrip('.').lstrip('/'))
    dest = base_dir / p
    if dest.is_dir():
        dest.rmdir()
    if not dest.parent.is_dir():
        print(f'mkdir {dest.parent}')
        dest.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == '.rst':
        print(p, dest)
        with p.open() as fin:
            with dest.open('w') as fout:
                fout.writelines(fin.readlines())
pwd
hist -f ../../community/knowt/scripts/clone_runestone_books_and_copy_rst.py
