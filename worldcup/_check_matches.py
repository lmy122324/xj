import json

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])
print(f'Total matches: {len(matches)}')
print(f'Prediction accuracy: {json.dumps(data.get("prediction_accuracy", {}), indent=2, ensure_ascii=False)[:800]}')
print()

# Check for matches with result=null but past their play time
print('=== 所有比赛 ===')
for m in matches:
    result = m.get('result', None)
    date = m.get('date', '?')
    time = m.get('time', '?')
    home = m.get('home', '?')
    away = m.get('away', '?')
    verified = m.get('verified', False)
    analyses = m.get('analyses', [])
    last_analysis = analyses[-1] if analyses else {}
    predicted = last_analysis.get('deepAnalysis', {}).get('predictedResult', 'N/A') if 'deepAnalysis' in last_analysis else 'N/A'
    print(f'{date} {time} | {home} vs {away} | result={result} | verified={verified} |预测={predicted}')
