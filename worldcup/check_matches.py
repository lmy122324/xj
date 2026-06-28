# -*- coding: utf-8 -*-
import json
from datetime import datetime

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8') as f:
    data = json.load(f)

matches = data['matches']
now = datetime(2026, 6, 28, 15, 19)
print('总比赛数:', len(matches))
print('生成时间:', data['generated_at'])
print()

for m in matches:
    t = m['time']
    parts = t.split(' ')
    if len(parts) == 2:
        md, hm = parts[0], parts[1]
        month_day = md.split('/')
        hm_parts = hm.split(':')
        match_dt = datetime(2026, int(month_day[0]), int(month_day[1]), int(hm_parts[0]), int(hm_parts[1]))
        if match_dt < now and m['result'] is None:
            print('🕐 已过比赛, result=null:', m['home'], 'vs', m['away'], '@', t)

print()
print('所有比赛的result状态:')
for m in matches:
    res = m.get('result', 'N/A')
    print(' ', m['home'], 'vs', m['away'], '@', m['time'], '=>', res)

print()
acc = data.get('prediction_accuracy', {})
print('prediction_accuracy:', json.dumps(acc, ensure_ascii=False, indent=2)[:500])
