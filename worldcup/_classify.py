import json
from datetime import datetime

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])
now = datetime(2026, 6, 21, 0, 37)

today_matches = []
upcoming_matches = []

for m in matches:
    date_str = m.get('date', '')
    # date field is like "06/21"
    try:
        parts = date_str.split('/')
        md = datetime(2026, int(parts[0]), int(parts[1]))
        diff = (md - now).days
        if diff < 0:
            # Past - check if result is null (needs result lookup)
            if m.get('result') is None:
                today_matches.append(m)
        elif diff <= 3:
            upcoming_matches.append(m)
    except:
        pass

print(f"Today's matches (may need results): {len(today_matches)}")
print(f"Upcoming matches (next 3 days): {len(upcoming_matches)}")
print()

# Show today's matches that need results
for m in today_matches:
    print(f"  ⏰ {m['date']} {m.get('time','?')} | {m['home']} vs {m['away']}")

print()
print("=== Upcoming matches ===")
for m in upcoming_matches:
    print(f"  📅 {m['date']} {m.get('time','?')} | {m['home']} vs {m['away']}")
