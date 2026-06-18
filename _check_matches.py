import json

with open('worldcup/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])
print(f'Total matches: {len(matches)}')
print(f'Analysis count: {data.get("analysisCount")}')
print(f'Last update: {data.get("lastUpdate")}')
print()

# Show upcoming/live matches
print('=== UPCOMING / LIVE MATCHES ===')
for m in matches:
    if m['time'] != '已完赛':
        print(f'{m["group"]}: {m["home"]} vs {m["away"]} - {m["date"]} {m["time"]}')
        print(f'  Analyses: {len(m["analyses"])}, Changes: {len(m["changes"])}')
print()

# Show completed
print('=== COMPLETED MATCHES ===')
for m in matches:
    if m['time'] == '已完赛':
        print(f'{m["group"]}: {m["home"]} {m["result"]} {m["away"]} ({m["date"]})')

print()
# Groups overview
print('=== GROUPS ===')
groups = {}
for m in matches:
    g = m['group']
    if g not in groups:
        groups[g] = {}
    groups[g][m['home']] = m['result'] if m['time'] == '已完赛' else '?'
    groups[g][m['away']] = m['result'] if m['time'] == '已完赛' else '?'

for g in sorted(groups.keys()):
    teams = list(groups[g].keys())
    print(f'Group {g}: {", ".join(teams)}')
