import json
from datetime import datetime, timedelta

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8') as f:
    data = json.load(f)

now = datetime(2026, 6, 21, 0, 37)
three_days = now + timedelta(days=3)

matches = data.get('matches', [])

print(f"当前: {now}")
print(f"未来3天内: {three_days}")
print()

# Check which matches are coming up in 3 days
for m in matches:
    date_str = m.get('date', '')
    time_str = m.get('time', '')
    # Parse date - format is like "06/21"
    try:
        month, day = date_str.split('/')
        match_date = datetime(2026, int(month), int(day))
        
        # For matches today, check if they haven't started yet
        home = m.get('home', '?')
        away = m.get('away', '?')
        
        if match_date <= three_days:
            status = "即将" if match_date >= now else ("已开始/可能已结束" if match_date == now.date() else "已过")
            print(f"📅 {date_str} {time_str} | {home} vs {away} | {status}")
        else:
            print(f"🔮 {date_str} {time_str} | {home} vs {away} | 3天后之外")
    except:
        print(f"⚠️ {date_str} {time_str} | {m.get('home','?')} vs {m.get('away','?')} | 日期解析失败")
