import json

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total matches: {len(data["matches"])}')
print()

for m in data['matches']:
    r = m.get('result', None)
    home = m['home']
    away = m['away']
    date = m.get('date', '')
    time = m.get('time', '')
    print(f'{home:>6s} vs {away:<8s} | {date:10s} {time:15s} | result={r}')

print()
print('=== Matches with result=null (potential post-match review needed) ===')
for m in data['matches']:
    r = m.get('result', None)
    if r is None or r == 'null':
        home = m['home']
        away = m['away']
        date = m.get('date', '')
        time = m.get('time', '')
        print(f'{home:>6s} vs {away:<8s} | {date:10s} {time:15s}')
