import json, glob, os, sys, hashlib, datetime
# usage: python3 build_site_data.py <dir with nodes/ and members/> <out data.json>
src, out = sys.argv[1], sys.argv[2]
def load(c):
    d = {}
    for p in glob.glob(os.path.join(src, c, '*.json')):
        d[os.path.basename(p)[:-5]] = json.load(open(p, encoding='utf-8'))
    return d
N, M = load('nodes'), load('members')
def alive(i):
    n, g = N.get(i), 0
    while n is not None and g < 60:
        if n.get('deleted'): return False
        p = n.get('parent') or ''
        if not p: return True
        n, g = N.get(p), g + 1
    return False
keep = {i for i in N if alive(i)}
kids = {}
for i in keep: kids.setdefault(N[i].get('parent') or '', []).append(i)
def has_content(i):
    n = N[i]
    return bool((n.get('title') or '').strip()) or any(has_content(k) for k in kids.get(i, []))
keep = {i for i in keep if has_content(i)}
F = ['act','parent','kind','title','title_en','detail','detail_en','due','status','order','tag','date']
nodes = []
for i in keep:
    n = N[i]; o = {'id': i}
    for f in F: o[f] = n.get(f, '' if f != 'order' else 0)
    for r in ('owners','reviewers','suggested'): o[r] = [m for m in (n.get(r) or []) if m in M]
    nodes.append(o)
nodes.sort(key=lambda o: (o['act'], o['parent'], o['order'] or 0, o['id']))
members = sorted(({'id': k, 'name': v.get('name',''), 'order': v.get('order', 0)} for k, v in M.items()), key=lambda m: (m['order'] or 0, m['name']))
body = {'members': members, 'nodes': nodes}
h = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.') + '%03dZ' % (datetime.datetime.now().microsecond // 1000)
json.dump(dict(generatedAt=now, hash=h, **body), open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(json.dumps({'hash': h, 'generatedAt': now, 'nodes': len(nodes), 'members': len(members), 'dropped': len(N) - len(nodes)}))
