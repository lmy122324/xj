import json

with open('C:/Users/19916/Desktop/xj-local/worldcup/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Matches count:', len(data.get('matches', [])))
for m in data.get('matches', []):
    r = m.get('result')
    print(f'{m["home"]:>8} vs {m["away"]:<10} | {m["time"]:<14} | result={r} | analyses={len(m.get("analyses",[]))}')

print()
acc = data.get('prediction_accuracy')
if acc:
    print('prediction_accuracy:', json.dumps(acc, indent=2, ensure_ascii=False))
else:
    print('No prediction_accuracy found')

print()
print('Available keys:', list(data.keys()))
