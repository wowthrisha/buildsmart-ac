import os, glob

targets = ['payments','projects','documents','meetings','compliance','client','activity','plot','settings','notifications']
bases = ['Cursor','Windsurf','Code']
dest = '/Users/thrisha/BS_APP/buildsmart/app/routes'

print('Recovering...')
found = set()

for base in bases:
    hdir = f'/Users/thrisha/Library/Application Support/{base}/User/History'
    if not os.path.isdir(hdir): continue
    
    # Sort files by modification time descending to grab the LATEST version!
    all_files = []
    for root, dirs, files in os.walk(hdir):
        for f in files:
            if f == 'entries.json': continue
            path = os.path.join(root, f)
            all_files.append((path, os.path.getmtime(path)))
    
    all_files.sort(key=lambda x: x[1], reverse=True)
    
    for path, mtime in all_files:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            for t in targets:
                if t not in found and f"Blueprint('{t}'" in text:
                    with open(os.path.join(dest, f'{t}.py'), 'w', encoding='utf-8') as out:
                        out.write(text)
                    found.add(t)
                    print(f'Restored {t}.py from {base} History')
        except Exception as e:
            pass

# __init__.py is basically empty
with open(os.path.join(dest, '__init__.py'),'w') as f:
    f.write('')

print('Done. Discovered:', len(found), '/', len(targets))
