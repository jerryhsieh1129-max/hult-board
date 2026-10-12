import json, sys
# usage: python3 pub.py <full data.json from build.py> <public.json>
# 公開版只留：事項（有狀態或有負責人的項目）、所屬活動、期限、狀態、負責人；不含任何內容與細節
src, out = sys.argv[1], sys.argv[2]
D = json.load(open(src, encoding='utf-8'))
nodes = D['nodes']
kids = {}
for n in nodes: kids.setdefault(n.get('parent') or '', []).append(n)
for v in kids.values(): v.sort(key=lambda n: (n.get('order') or 0, n['id']))
seq, k = {}, 0
def walk(p):
    global k
    for n in kids.get(p, []):
        seq[n['id']] = k; k += 1; walk(n['id'])
walk('')
acts = [n for n in nodes if n.get('kind') == 'activity']
act_ids = {a['id'] for a in acts}
# 事項＝有狀態或有負責人的項目（沒填狀態的當作未開始）
tasks = [n for n in nodes if n.get('kind') == 'item' and (n.get('status') or n.get('owners')) and n.get('act') in act_ids]
pub = {
    'generatedAt': D.get('generatedAt', ''),
    'members': [{'id': m['id'], 'name': m['name'], 'order': m.get('order', 0)} for m in D['members']],
    'acts': [{'id': a['id'], 'title': a.get('title', ''), 'title_en': a.get('title_en', ''), 'order': a.get('order', 0)} for a in sorted(acts, key=lambda a: (a.get('order') or 0, a['id']))],
    'tasks': [{'id': n['id'], 'act': n['act'], 'title': n.get('title', ''), 'title_en': n.get('title_en', ''), 'due': n.get('due', ''),
               'status': n.get('status', ''), 'owners': n.get('owners', []), 'seq': seq.get(n['id'], 0)} for n in tasks],
}
json.dump(pub, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(json.dumps({'acts': len(pub['acts']), 'tasks': len(pub['tasks']), 'members': len(pub['members'])}))
