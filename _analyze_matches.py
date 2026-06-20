import json
from datetime import datetime, timezone, timedelta

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])
print(f'Total matches: {len(matches)}')
print(f'Generated at: {data.get("generated_at", "N/A")}')
print()

# Check matches with results
has_result = [m for m in matches if m.get('result')]
no_result = [m for m in matches if m.get('result') is None]
print(f'Matches with result: {len(has_result)}')
print(f'Matches without result: {len(no_result)}')
print()

# Beijing time now
bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz)
today_str = now.strftime('%m/%d')
print(f'Beijing time now: {now}')
print(f'Today: {today_str}')
print()

# Identify past matches without results
print('=== PAST MATCHES (no result yet) ===')
past_no_result = []
for m in matches:
    res = m.get('result')
    if res is not None:
        continue
    # Parse match time - matches may have format like "06/20 06:00"
    time_str = m.get('time', '')
    # Parse date
    date_str = m.get('date', '')
    if '/' in date_str and ':' in time_str:
        parts = time_str.split(' ')
        if len(parts) >= 2:
            dt_str = parts[0] + ' ' + parts[1]
        else:
            dt_str = date_str + ' ' + time_str.split()[-1]
    elif '/' in date_str:
        dt_str = date_str + ' 23:59'
    else:
        continue
    
    try:
        match_dt = datetime.strptime(dt_str, '%m/%d %H:%M')
        match_dt = match_dt.replace(year=now.year)
        match_dt = bj_tz.localize(match_dt)
        
        if match_dt < now:
            past_no_result.append(m)
            print(f'{m["time"]} {m["home"]} vs {m["away"]}')
    except:
        pass

print(f'\nPast matches without result: {len(past_no_result)}')
print()

# Show all matches with results (for verification)
print('=== MATCHES WITH RESULTS ===')
for m in has_result:
    print(f'{m["time"]} {m["home"]} vs {m["away"]} -> {m["result"]}')

print()
print('=== PREDICTION ACCURACY ===')
acc = data.get('prediction_accuracy', {})
print(json.dumps(acc, indent=2, ensure_ascii=False))
