import json, copy
from datetime import datetime, timezone, timedelta

DATA_PATH = r'C:\Users\19916\Desktop\xj-local\worldcup\data.json'
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data['matches']
bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz)

# ============ Step 1: Check past matches ============
past_no_result = []
for idx, m in enumerate(matches):
    if m.get('result') is not None:
        continue
    time_str = m.get('time', '')
    try:
        match_dt = datetime.strptime(time_str, '%m/%d %H:%M').replace(year=now.year, tzinfo=bj_tz)
        if match_dt < now:
            past_no_result.append((idx, m))
    except:
        pass

print('=== Past matches without result ===')
for idx, m in past_no_result:
    print(f'#{idx}: {m["time"]} {m["home"]} vs {m["away"]}')

# ============ Step 2: Update match #0 (Scotland vs Morocco) ============
# Confirmed: Morocco 1-0 Scotland
if len(past_no_result) > 0:
    match_idx = past_no_result[0][0]
    old = matches[match_idx]
    print(f'\nUpdating match #{match_idx}: {old["home"]} vs {old["away"]}')
    print(f'Result: 摩洛哥胜 (Morocco 1-0 Scotland)')
    
    matches[match_idx]['result'] = '摩洛哥胜'
    
    # Check the latest analysis prediction
    analyses = old.get('analyses', [])
    if analyses:
        latest = analyses[-1]
        predicted = latest.get('strategies', {}).get('conservative', {}).get('pick', '')
        predicted2 = latest.get('text', '')
        print(f'Predicted: {predicted} / {predicted2}')
        print(f'Actual: 摩洛哥胜')
else:
    print('No past matches to update.')

# ============ Step 3: Count all result-bearing matches for accuracy ============
print('\n=== All matches with results ===')
verified_count = 0
correct_h2h = data.get('prediction_accuracy', {}).get('correct_h2h', 0)
total_matches = data.get('prediction_accuracy', {}).get('total_matches', 0)

for idx, m in enumerate(matches):
    res = m.get('result')
    if res is not None:
        verified = m.get('verified', False)
        analyses = m.get('analyses', [])
        if analyses:
            latest = analyses[-1]
            predicted_pick = latest.get('strategies', {}).get('conservative', {}).get('pick', '')
            print(f'#{idx}: {m["home"]} vs {m["away"]} -> {res} (predicted: {predicted_pick}) verified={verified}')
        else:
            print(f'#{idx}: {m["home"]} vs {m["away"]} -> {res} (no analysis) verified={verified}')

# Save
if len(past_no_result) > 0:
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('\n✅ data.json updated')
else:
    print('\n⏭️ No changes needed')
