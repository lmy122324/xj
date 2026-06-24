# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)

data = json.load(open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8'))
matches = data['matches']

print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M')} CST")
print(f"比赛总数: {len(matches)}\n")

# Check for matches that are past their scheduled time but have no result
past_no_result = []
for m in matches:
    result = m.get('result')
    # Parse match time - format like "06/25 03:00"
    time_str = m.get('time', '')
    if time_str:
        try:
            dt = datetime.strptime(time_str, '%m/%d %H:%M')
            dt = dt.replace(year=now.year, tzinfo=tz)
            if dt < now and result is None:
                past_no_result.append(m)
        except:
            pass
    
    status = "✅" if result else ("⏳" if m.get('time', '') >= now.strftime('%m/%d') else "❌")
    print(f"{status} {m['date']} | {m['home']:>8} vs {m['away']:<8} | result={result or 'null'}")

print(f"\n--- 已结束但未填结果: {len(past_no_result)} 场 ---")
for m in past_no_result:
    print(f"  {m['time']} | {m['home']} vs {m['away']}")
