import json

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8') as f:
    data = json.load(f)

# Check latest analysis for first match
m = data['matches'][0]
print(f"Match: {m['home']} vs {m['away']}")
print(f"Analyses count: {len(m.get('analyses', []))}")
print()
last = m['analyses'][-1] if m.get('analyses') else {}
print(f"Last analysis time: {last.get('time', 'N/A')}")
print(f"Keys in last analysis: {list(last.keys())}")
# Check if deepAnalysis exists
if 'deepAnalysis' in last:
    print(f"deepAnalysis: {json.dumps(last['deepAnalysis'], indent=2, ensure_ascii=False)[:500]}")
if 'strategies' in last:
    print(f"strategies: {json.dumps(last['strategies'], indent=2, ensure_ascii=False)[:500]}")
if 'jingcai_all' in last:
    print(f"jingcai_all: {json.dumps(last['jingcai_all'], indent=2, ensure_ascii=False)[:500]}")
if 'fullReport' in last:
    print(f"fullReport length: {len(last['fullReport'])} chars")

# Check the prediction_accuracy at the end
if 'prediction_accuracy' in data:
    print(f"\nprediction_accuracy: {json.dumps(data['prediction_accuracy'], indent=2, ensure_ascii=False)}")
