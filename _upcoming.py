import json
from datetime import datetime, timezone, timedelta

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])
bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz)

print('=== UPCOMING MATCHES (next 3 days, up to 06/23) ===')
for idx, m in enumerate(matches):
    if m.get('result') is not None:
        continue
    time_str = m.get('time', '')
    try:
        match_dt = datetime.strptime(time_str, '%m/%d %H:%M')
        match_dt = match_dt.replace(year=now.year)
        match_dt = match_dt.replace(tzinfo=bj_tz)
        if match_dt >= now:
            three_days = now + timedelta(days=3)
            if match_dt <= three_days:
                print(f'#{idx}: {m["time"]} {m["home"]} vs {m["away"]}')
    except:
        pass
