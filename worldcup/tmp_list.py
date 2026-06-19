import json
with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

upcoming = [m for m in data['matches'] if m.get('result') is None]
print(f'未赛比赛数: {len(upcoming)}')
for m in upcoming:
    text = m['analyses'][-1]['text'] if m.get('analyses') else '无'
    print(f"{m['date']} {m['home']} vs {m['away']} | {text[:100]}")
