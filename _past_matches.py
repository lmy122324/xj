import json
from datetime import datetime, timezone, timedelta

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])
bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz)

print(f'Beijing now: {now.strftime("%m/%d %H:%M")}')
print()

print('=== PAST MATCHES (no result yet) ===')
for idx, m in enumerate(matches):
    if m.get('result') is not None:
        continue
    # time field like "06/20 06:00"
    time_str = m.get('time', '')
    try:
        match_dt = datetime.strptime(time_str, '%m/%d %H:%M')
        match_dt = match_dt.replace(year=now.year)
        match_dt = match_dt.replace(tzinfo=bj_tz)
        if match_dt < now:
            print(f'#{idx}: {m["time"]} {m["home"]} vs {m["away"]}')
    except Exception as e:
        print(f'Parse error for {time_str}: {e}')
